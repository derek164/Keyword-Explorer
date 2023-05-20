import pandas as pd

import database as db


class KeywordAPI:
    def __init__(self, database):
        self.database = database
        self.gds = db.gds.Client(database=database)
        self.mysql = db.mysql.Client(database=database)
        self.mongo = db.mongo.Client(database=database)
        self.neo4j = db.neo4j.Client(database=database)
        self.prepared = db.prepared.Client(database=database)

    def get_keywords(self):
        return [
            keyword["name"]
            for keyword in self.mysql.execute(query=self.mysql.get_keywords)
        ]

    def get_keyword_usage(self, **kwargs):
        return pd.DataFrame(
            self.mongo.execute(query=self.mongo.get_keyword_usage, **kwargs)
        )

    def get_similar_keywords(self, **kwargs):
        return [
            match["keyword2"]
            for match in self.neo4j.execute(
                query=self.neo4j.get_similar_keywords, **kwargs
            )
        ]

    def project_pub_keyword_subgraph(self):
        self.gds.project_if_not_exists(
            "keyword-label-pub",
            {
                "nodes": ["PUBLICATION", "KEYWORD"],
                "relationships": {
                    "LABEL_BY": {"properties": "score", "orientation": "REVERSE"}
                },
            },
        )

    def get_most_relevant_publications(self, **kwargs):
        return [
            publication["title"]
            for publication in self.neo4j.execute(
                query=self.neo4j.get_most_relevant_publications, **kwargs
            )
        ]

    def get_most_relevant_university(self, **kwargs):
        return [
            institute["institute"]
            for institute in self.neo4j.execute(
                query=self.neo4j.get_most_relevant_universities, **kwargs
            )
        ]

    def get_most_relevant_university_publications(self, **kwargs):
        return [
            publication["title"]
            for publication in self.neo4j.execute(
                query=self.neo4j.get_most_relevant_university_publications, **kwargs
            )
        ]

    def get_most_relevant_faculty(self, **kwargs):
        return [
            faculty["faculty"]
            for faculty in self.neo4j.execute(
                query=self.neo4j.get_most_relevant_faculty, **kwargs
            )
        ]

    def get_most_relevant_faculty_publications(self, **kwargs):
        return [
            publication["title"]
            for publication in self.neo4j.execute(
                query=self.neo4j.get_most_relevant_faculty_publications, **kwargs
            )
        ]

    def create_tables(self):
        self.prepared.execute(query=self.prepared.create_favorites_table)
        self.prepared.execute(query=self.prepared.create_crossref_table)

    def get_favorites(self):
        return [
            favorite["title"]
            for favorite in self.prepared.execute(query=self.prepared.get_favorites)
        ]

    def insert_favorite(self, title):
        print("Adding favorite: " + title)
        self.prepared.execute(query=self.prepared.insert_favorite, tuple=(title,))

    def remove_favorite(self, title):
        print("Removing favorite: " + title)
        self.prepared.execute(query=self.prepared.remove_favorite, tuple=(title,))

    def get_crossref_count(self):
        return self.prepared.execute(query=self.prepared.get_crossref_count)[0]["count"]

    def insert_crossref(self, row):
        self.prepared.execute(query=self.prepared.insert_crossref, tuple=row)

    def publication_is_linked(self, publication):
        response = self.prepared.execute(
            query=self.prepared.publication_is_linked, tuple=(publication,)
        )
        return True if len(response) > 0 else False

    def get_crossref_url(self, publication):
        try:
            return self.prepared.execute(
                query=self.prepared.get_crossref_url,
                tuple=(publication,),
            )[0]["url"]
        except:
            return f'https://scholar.google.com/scholar?hl=en&q="{publication}"'

    def get_publication_keywords(self, publication):
        try:
            return self.neo4j.execute(
                query=self.neo4j.get_publication_keywords,
                publication=publication,
            )[0]["keywords"]
        except:
            return []
