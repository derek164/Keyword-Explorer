import database as db


gds = db.gds.Client(database="academicworld")
mysql = db.mysql.Client(database="academicworld")
mongo = db.mongo.Client(database="academicworld")
neo4j = db.neo4j.Client(database="academicworld")
prepared = db.prepared.Client(database="academicworld")


result = mysql.execute(
    query=mysql.get_university_faculty, institute="University of illinois"
)
print("\n[test] mysql.get_university_faculty")
print(result)

result = mongo.execute(
    query=mongo.get_university_faculty, institute="University of illinois"
)
print("\n[test] mongo.get_university_faculty")
print(result)

result = neo4j.execute(
    query=neo4j.get_university_faculty, institute="University of illinois"
)
print("\n[test] neo4j.get_university_faculty")
print(result)

result = neo4j.execute(
    query=neo4j.get_most_relevant_universities,
    keyword="internet",
    start_year=1903,
    end_year=2021,
)
print("\n[7a] neo4j.get_most_relevant_universities")
print(result)

result = neo4j.execute(
    query=neo4j.get_university_publications,
    university="University of illinois at Urbana Champaign",
    keyword="internet"
)
print("\n[7b] neo4j.get_university_publications")
print(result)

result = neo4j.execute(
    query=neo4j.get_most_relevant_faculty,
    keyword="internet",
    start_year=1903,
    end_year=2021,
)
print("\n[6a] neo4j.get_most_relevant_faculty")
print(result)

result = mysql.execute(
    query=mysql.get_faculty_publications,
    faculty="Peter Druschel ",
    keyword="internet"
)
print("\n[6b] mysql.get_faculty_publications")
print(result)

result = mysql.execute(
    query=mysql.get_most_relevant_publications,
    keyword="internet",
    start_year=1903,
    end_year=2021,
)
print("\n[5] mysql.get_most_relevant_publications")
print(result)

result = mongo.execute(
    query=mongo.get_publications_by_year,
    keyword="internet",
    start_year=1903,
    end_year=2021,
)
print("\n[3] mongo.get_publications_by_year")
print(result)

result = mongo.execute(
    query=mongo.get_citations_and_relevance_by_year,
    keyword="internet",
    start_year=1903,
    end_year=2021,
)
print("\n[4] mongo.get_citations_and_relevance_by_year")
print(result)

gds.project_if_not_exists(
    "keyword-label-pub",
    {
        "nodes": ["PUBLICATION", "KEYWORD"],
        "relationships": {
            "LABEL_BY": {"properties": "score", "orientation": "REVERSE"}
        },
    },
)
result = neo4j.execute(query=neo4j.get_similar_keywords, keyword="internet")
print("\n[2] neo4j.get_similar_keywords")
print(result)

result = prepared.execute(
    query=prepared.create_favorites_table
)
print("\n[test] prepared.create_favorites_table")
print(result)

result = prepared.execute(
    query=prepared.remove_favorite,
    tuple=("IoT Data Prefetching in Indoor Navigation SOAs",),
)
print("\n[test] prepared.remove_favorite")
print(result)

result = prepared.execute(
    query=prepared.insert_favorite,
    tuple=("IoT Data Prefetching in Indoor Navigation SOAs",),
)
print("\n[test] prepared.insert_favorite")
print(result)

result = prepared.execute(query=prepared.get_favorites)
print("\n[test] prepared.get_favorites")
print(result)

# result = prepared.execute(
#     query=prepared.drop_favorites_table
# )
# print("\n[test] prepared.drop_favorites_table")
# print(result)
