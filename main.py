import database as db


mysql = db.mysql.Client(database="academicworld")
result = mysql.execute_read(
    query=mysql.get_university_faculty, institute="University of illinois"
)
print(result)

mongo = db.mongo.Client(database="academicworld")
result = mongo.execute_read(
    query=mongo.get_university_faculty, institute="University of illinois"
)
print(result)

neo4j = db.neo4j.Client(database="academicworld")
result = neo4j.execute_read(
    query=neo4j.get_university_faculty, institute="University of illinois"
)
print(result)

result = neo4j.execute_read(
    query=neo4j.get_similar_keywords, keyword="internet"
)
print(result)
