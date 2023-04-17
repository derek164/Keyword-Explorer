import mysql.connector
from database.prepared.query import Query

# from query import Query


class Client(Query):
    def __init__(self, database):
        self.database = database

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="test_root",
            database=database,
            charset="utf8mb4",
        )

    def execute(self, query, tuple=()):
        with self.database.cursor(prepared=True) as cursor:
            cursor.execute(query(), tuple)
            results = [dict(zip(cursor.column_names, row)) for row in cursor.fetchall()]
            self.database.commit()
            return results


if __name__ == "__main__":
    prepared = Client(database="academicworld")
    result = prepared.execute(
        query=prepared.get_university_faculty,
        tuple=("University of illinois at Urbana Champaign",),
    )
    print(result)
