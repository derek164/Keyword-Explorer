import database as db


mysql = db.mysql.Client(database="academicworld")
result = mysql.execute_read(
    query=mysql.get_university_faculty, institute="University of illinois"
)
print("\n[test] mysql.get_university_faculty")
print(result)

mongo = db.mongo.Client(database="academicworld")
result = mongo.execute_read(
    query=mongo.get_university_faculty, institute="University of illinois"
)
print("\n[test] mongo.get_university_faculty")
print(result)

neo4j = db.neo4j.Client(database="academicworld")
result = neo4j.execute_read(
    query=neo4j.get_university_faculty, institute="University of illinois"
)
print("\n[test] neo4j.get_university_faculty")
print(result)

result = neo4j.execute_read(
    query=neo4j.get_most_relevant_universities,
    keyword="internet",
    start_year=1903,
    end_year=2021,
)
print("\n[7a] neo4j.get_most_relevant_universities")
print(result)

result = neo4j.execute_read(
    query=neo4j.get_university_publications,
    university="University of illinois at Urbana Champaign",
    keyword="internet"
)
print("\n[7b] neo4j.get_university_publications")
print(result)

result = neo4j.execute_read(
    query=neo4j.get_most_relevant_faculty,
    keyword="internet",
    start_year=1903,
    end_year=2021,
)
print("\n[6a] neo4j.get_most_relevant_faculty")
print(result)

result = mysql.execute_read(
    query=mysql.get_faculty_publications,
    faculty="Peter Druschel ",
    keyword="internet"
)
print("\n[6b] mysql.get_faculty_publications")
print(result)

result = mysql.execute_read(
    query=mysql.get_most_relevant_publications,
    keyword="internet",
    start_year=1903,
    end_year=2021,
)
print("\n[5] mysql.get_most_relevant_publications")
print(result)

result = mongo.execute_read(
    query=mongo.get_publications_by_year,
    keyword="internet",
    start_year=1903,
    end_year=2021,
)
print("\n[3] mongo.get_publications_by_year")
print(result)

result = mongo.execute_read(
    query=mongo.get_citations_and_relevance_by_year,
    keyword="internet",
    start_year=1903,
    end_year=2021,
)
print("\n[4] mongo.get_citations_and_relevance_by_year")
print(result)

gds = db.gds.Client(database="academicworld")
gds.project_if_not_exists(
    "keyword-label-pub",
    {
        "nodes": ["PUBLICATION", "KEYWORD"],
        "relationships": {
            "LABEL_BY": {"properties": "score", "orientation": "REVERSE"}
        },
    },
)
result = neo4j.execute_read(query=neo4j.get_similar_keywords, keyword="internet")
print("\n[2] neo4j.get_similar_keywords")
print(result)
