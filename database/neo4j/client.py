from neo4j import GraphDatabase
from database.neo4j.query import Query

# from query import Query


class Client(Query):
    def __init__(self, database):
        self.driver = self._get_driver()
        self.database = database

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    def _get_driver(self):
        user, password = "neo4j", "test_root"
        uri = "{scheme}://{host_name}:{port}".format(
            scheme="neo4j", host_name="localhost", port=7687
        )
        return GraphDatabase.driver(uri=uri, auth=(user, password))

    def execute_read(self, query, **kwargs):
        def format_output(query):
            def wrap(tx, **kwargs):
                return [dict(record) for record in tx.run(query(**kwargs), **kwargs)]

            return wrap

        with self.driver.session(database=self.database) as session:
            return session.execute_read(format_output(query), **kwargs)


if __name__ == "__main__":
    neo4j = Client(database="academicworld")
    result = neo4j.execute_read(
        query=neo4j.get_university_faculty, institute="University of illinois"
    )
    print(result)
    result = neo4j.execute_read(query=neo4j.get_similar_keywords, keyword="internet")
    print(result)
