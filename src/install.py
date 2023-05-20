from pathlib import Path

import pandas as pd
from tqdm import tqdm

from api import KeywordAPI


class KeywordInstaller:
    def __init__(self, directory):
        self.directory = directory
        self.client = KeywordAPI(database="academicworld")

    def run(self):
        self.cache_keywords()
        self.cache_linked_publications()
        self.client.project_pub_keyword_subgraph()
        self.client.create_tables()
        self.load_crossref_table()

    def cache_keywords(self):
        keywords_cache = self.directory.joinpath("keywords.txt")
        if not keywords_cache.exists():
            keywords = self.client.get_keywords()
            with open(keywords_cache, "w+") as f:
                [f.write(keyword + "\n") for keyword in keywords]

    def load_crossref_table(self):
        pub_crossref_jsonl_zip = self.directory.joinpath("pub_crossref_urls.jsonl.zip")
        pub_crossref_urls = pd.read_json(pub_crossref_jsonl_zip, lines=True)

        if self.client.get_crossref_count() < 400000:
            rows = list(pub_crossref_urls.itertuples(index=False, name=None))
            print(pub_crossref_urls.head(10))

            for row in tqdm(rows, desc="Loading..."):
                self.client.insert_crossref(row)


if __name__ == "__main__":
    expansion = Path(__file__).resolve().parent.joinpath("expansion")
    KeywordInstaller(directory=expansion).run()
