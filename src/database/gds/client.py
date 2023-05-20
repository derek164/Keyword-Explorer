from graphdatascience import GraphDataScience
from graphdatascience.graph.graph_object import Graph

from database.neo4j.query import Query

# from query import Query


class Client(Query):
    def __init__(self, database):
        self.gds = self._get_gds()
        self.database = database

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self.gds.set_database(database)
        self._database = database

    def _get_gds(self):
        user, password = "neo4j", "test_root"
        uri = "{scheme}://{host_name}:{port}".format(
            scheme="neo4j", host_name="localhost", port=7687
        )
        return GraphDataScience(endpoint=uri, auth=(user, password))

    def exists(self, graph_name):
        return self.gds.graph.exists(graph_name)["exists"]

    def graph(self, graph_name) -> Graph:
        return self.gds.graph.get(graph_name)

    def drop(self, graph: Graph):
        return self.gds.graph.drop(graph)

    def project(self, graph_name, nodes, relationships):
        return self.gds.graph.project(
            graph_name,  #  Graph name
            nodes,  #  Node projection
            relationships,  #  Relationship projection
        )

    def project_if_not_exists(self, graph_name, configuration: dict):
        if not self.exists(graph_name):
            print(f"Projecting {graph_name}...", end="")
            return self.project(graph_name, **configuration)


if __name__ == "__main__":
    gds = Client(database="academicworld")
    # graph = gds.graph("keyword-label-pub")
    # print(gds.drop(graph))
    result = gds.project_if_not_exists(
        "keyword-label-pub",
        {
            "nodes": ["PUBLICATION", "KEYWORD"],
            "relationships": {
                "LABEL_BY": {"properties": "score", "orientation": "REVERSE"}
            },
        },
    )
    print(result)
    print(type(result))
