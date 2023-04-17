import pymysql
from database.mysql.query import Query

# from query import Query


class Client(Query):
    def __init__(self, database):
        self.database = database

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="test_root",
            database=database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

    def execute_read(self, query, **kwargs):
        with self.database.cursor() as cursor:
            cursor.execute(query(**kwargs))
            return cursor.fetchall()


if __name__ == "__main__":
    mysql = Client(database="academicworld")
    result = mysql.execute_read(
        query=mysql.get_university, institute="University of illinois"
    )
    print(result)
