from pymongo import MongoClient
from database.mongo.query import Query
# from query import Query


class Client(Query):
    def __init__(self, database):
        self.database = database

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        host, port = "localhost", 27017
        self._database = MongoClient(host, port)[database]

    def execute_read(self, query, **kwargs):
        return query(database=self.database, **kwargs)
    
if __name__ == "__main__":
    mongo = Client(database="academicworld")
    result = mongo.execute_read(
        query=mongo.get_university_faculty, institute="University of illinois"
    )
    print(result)
