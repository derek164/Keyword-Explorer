import json
import re
import time
import timeit
import uuid
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path

import backoff
import pandas as pd
import requests
from requests.exceptions import JSONDecodeError, ProxyError, RequestException
from requests.utils import requote_uri
from urllib3.exceptions import HTTPError, NewConnectionError

import database as db
from proxy import ProxyPool

retry_on_exception = (
    KeyError,
    TypeError,
    HTTPError,
    IndexError,
    ProxyError,
    JSONDecodeError,
    RequestException,
    NewConnectionError,
    ConnectionResetError,
    ConnectionRefusedError,
)


expansion = Path(__file__).resolve().parent.joinpath("expansion")
pub_crossref_metrics = expansion.joinpath("pub_crossref_metrics.jsonl")
pub_crossref_jsonl = expansion.joinpath("pub_crossref_urls.jsonl")
pub_crossref_urls = expansion.joinpath("pub_crossref_urls")


def generate_pub_search_extract():
    def query_pub_search_extract():
        return """
        MATCH (f:FACULTY)-[:PUBLISH]->(p:PUBLICATION)
        RETURN p.title AS publication
            , max(f.name) AS faculty
        """

    neo4j = db.neo4j.Client(database="academicworld")
    expansion.parent.mkdir(parents=True, exist_ok=True)

    pub_search_extract = pd.DataFrame(neo4j.execute(query=query_pub_search_extract))
    pub_search_extract.to_csv(expansion.joinpath("pub_search_extract.csv"), index=False)

    with pd.option_context("display.max_rows", None, "display.max_colwidth", 80):
        print(pub_search_extract.head(10))
        print(pub_search_extract.shape)


def get_pub_search_extract(override=False):
    pub_search_extract = expansion.joinpath("pub_search_extract.csv")
    if not pub_search_extract.exists() or override:
        generate_pub_search_extract()

    pub_search_extract = pd.read_csv(pub_search_extract)
    pub_search_extract["faculty"] = pub_search_extract["faculty"].apply(
        lambda x: " ".join(filter(None, re.split("[, ]", x))).lower()
    )

    with pd.option_context("display.max_rows", None, "display.max_colwidth", 80):
        print(pub_search_extract.head(10))
        print(pub_search_extract.shape)

    return pub_search_extract


class ThreadResults:
    def __init__(self, results_path, metrics_path, batch_size, total_size, init_size=0):
        print(init_size)
        self.batch_start = timeit.default_timer()
        self.total_size = total_size + init_size
        self.batch_size = batch_size
        self.total_index = init_size
        self.results = results_path
        self.metrics = metrics_path
        self.batch_index = 0
        self.batch = []

    def save(self, row):
        self.batch_index += 1
        self.batch.append(row)
        with open(
            self.results.joinpath("{hex}.jsonl".format(hex=uuid.uuid4().hex)), "w+"
        ) as f:
            f.write(json.dumps(row))

        print((self.batch_index, self.batch_size))
        if self.batch_index >= self.batch_size:
            self.batch_index = 0  # immediately signal new batch
            duration = timeit.default_timer() - self.batch_start
            self.batch_start = timeit.default_timer()
            self.total_index += self.batch_size
            self.summarize_batch(
                batch=pd.DataFrame(self.batch),
                duration=duration,
            )
            self.batch = []

    def summarize_batch(self, batch, duration):
        print(batch.head(10))
        summary = {
            "timestamp": (datetime.utcnow() - timedelta(hours=7)),
            "metrics": {
                k[0]: v
                for k, v in batch.value_counts(subset=["status"]).to_dict().items()
            },
            "duration": round(duration, 2),
            "progress": round(100 * self.total_index / self.total_size, 4),
            "completed": self.total_index,
            "total": self.total_size,
        }

        with open(self.metrics, "a+") as f:
            f.write(json.dumps(summary, default=str) + "\n")


@backoff.on_exception(backoff.expo, retry_on_exception, max_time=30)
def get_crossref_url(results, proxy_pool, publication, faculty):
    proxy_url = proxy_pool.get()
    row = {
        "status": "api_error",
        "publication": publication,
        "url": requote_uri(
            f'https://scholar.google.com/scholar?hl=en&q="{publication}"'
        ),
    }

    try:
        response = requests.get(
            "http://api.crossref.org/works",
            proxies={"http": proxy_url},
            timeout=5,
            params={
                "rows": 1,
                "select": "URL,score",
                "query.author": faculty,
                "query.bibliographic": publication,
                # "mailto": "derekz3@illinois.edu",
            },
        )

        work_item = response.json()["message"]["items"][0]
        score, url = work_item["score"], work_item["URL"]

        if score >= 50:
            row["status"] = "high_match"
            row["url"] = url
        else:
            row["status"] = "low_match"

    except retry_on_exception:
        raise

    if row["status"] == "api_error":
        proxy_pool.remove(proxy_url)
    else:
        proxy_pool.put(proxy_url)

    results.save(row)


def merge_jsonl(in_path: Path, out_file: Path):
    with open(out_file, "a+") as outfile:
        for file in in_path.glob("*.jsonl"):
            with open(file) as infile:
                for line in infile:
                    outfile.write(line + "\n")
            file.unlink()
    df = pd.read_json(pub_crossref_jsonl, lines=True)
    jsonl_zip = pub_crossref_jsonl.with_suffix(".jsonl.zip")
    df.to_json(jsonl_zip, lines=True, orient="records", compression={"method": "zip"})


def generate_crossref_urls(
    pub_search_extract, n_samples=None, batch_size=100, max_workers=1000
):
    if pub_crossref_jsonl.exists():
        processed = pd.read_json(pub_crossref_jsonl, lines=True)
        metrics = {
            k[0]: v
            for k, v in processed.value_counts(subset=["status"]).to_dict().items()
        }
        print(f"[Resuming Process] ===> {metrics}")
        pub_search_extract = pub_search_extract[
            ~pub_search_extract["publication"].isin(processed["publication"].tolist())
        ]
    else:
        metrics = defaultdict(lambda: 0)

    pub_search_tuples = list(pub_search_extract.itertuples(index=False, name=None))

    if n_samples:
        pub_search_tuples = pub_search_tuples[:n_samples]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        proxy_pool = ProxyPool(timeout=2)
        results = ThreadResults(
            batch_size=batch_size,
            init_size=sum(metrics.values()),
            total_size=len(pub_search_tuples),
            metrics_path=pub_crossref_metrics,
            results_path=pub_crossref_urls,
        )

        [
            executor.submit(get_crossref_url, results, proxy_pool, *pub_search_tuple)
            for pub_search_tuple in pub_search_tuples
        ]

    merge_jsonl(
        in_path=pub_crossref_urls,
        out_file=pub_crossref_jsonl,
    )
    return pd.read_json(pub_crossref_jsonl, lines=True)


if __name__ == "__main__":
    if pub_crossref_urls.exists():
        merge_jsonl(
            in_path=pub_crossref_urls,
            out_file=pub_crossref_jsonl,
        )
    pub_crossref_urls.mkdir(parents=True, exist_ok=True)
    pub_search_extract = get_pub_search_extract(override=False)
    pub_crossref_urls = generate_crossref_urls(pub_search_extract, n_samples=None)
    with pd.option_context("display.max_rows", None, "display.max_colwidth", 80):
        print(pub_crossref_urls.head(10))
        print(pub_crossref_urls.shape)
