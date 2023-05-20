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
            # cursorclass=pymysql.cursors.DictCursor,
        )

    def execute(self, query, **kwargs):
        with self.database.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query(**kwargs))
            return cursor.fetchall()


if __name__ == "__main__":
    mysql = Client(database="academicworld")
    result = mysql.execute(
        query=mysql.get_university, institute="University of illinois"
    )
    print(result)
