class Query:
    @staticmethod
    def get_university_faculty(institute):
        return """
        MATCH (f:FACULTY)-[:AFFILIATION_WITH]->(i:INSTITUTE)
        WHERE i.name CONTAINS $institute
        RETURN f.name AS faculty, i.name AS institute
        ORDER BY faculty
        LIMIT 10;
        """

    @staticmethod
    def get_similar_keywords(keyword):
        return """
        MATCH (keyword:KEYWORD) where keyword.name = $keyword
        CALL gds.alpha.nodeSimilarity.filtered.stream(
            'keyword-label-pub',
            { 
                degreeCutoff: 1,
                topK: 5,
                relationshipWeightProperty: "score",
                sourceNodeFilter: keyword,
                targetNodeFilter: 'KEYWORD'
            }
        )
        YIELD node1, node2, similarity
        RETURN gds.util.asNode(node1).name AS keyword1,
            gds.util.asNode(node2).name AS keyword2,
            similarity
        ORDER BY similarity DESCENDING
        """

    @staticmethod
    def get_most_relevant_universities(keyword, start_year, end_year):
        return """
        MATCH (i:INSTITUTE)<-[:AFFILIATION_WITH]-(f:FACULTY)-[:PUBLISH]->(p:PUBLICATION)-[l:LABEL_BY]->(k:KEYWORD)
        WHERE k.name = $keyword
            AND p.year >= $start_year
            AND p.year <= $end_year
        WITH i.name AS institute, p.numCitations * l.score AS KRC
        RETURN institute, sum(KRC) AS KRC
        ORDER BY KRC DESC
        LIMIT 10
        """
    
    @staticmethod
    def get_university_publications(university, keyword, start_year, end_year):
        return """
        MATCH (i:INSTITUTE)<-[:AFFILIATION_WITH]-(f:FACULTY)-[:PUBLISH]->(p:PUBLICATION)-[l:LABEL_BY]->(k:KEYWORD)
        WHERE k.name = $keyword
            AND i.name = $university
            AND p.year >= $start_year
            AND p.year <= $end_year
        WITH p.title AS title, p.year AS year, p.numCitations * l.score AS KRC
        RETURN title, year, sum(KRC) AS KRC
        ORDER BY KRC DESC
        LIMIT 10
        """
    
    @staticmethod
    def get_most_relevant_faculty(keyword, start_year, end_year):
        return """
        MATCH (i:INSTITUTE)<-[:AFFILIATION_WITH]-(f:FACULTY)-[:PUBLISH]->(p:PUBLICATION)-[l:LABEL_BY]->(k:KEYWORD)
        WHERE k.name = $keyword
            AND p.year >= $start_year
            AND p.year <= $end_year
        WITH f.name AS faculty, p.numCitations * l.score AS KRC
        RETURN faculty, sum(KRC) AS KRC
        ORDER BY KRC DESC
        LIMIT 10
        """
    
    @staticmethod
    def get_faculty_publications(faculty, keyword, start_year, end_year):
        return """
        MATCH (i:INSTITUTE)<-[:AFFILIATION_WITH]-(f:FACULTY)-[:PUBLISH]->(p:PUBLICATION)-[l:LABEL_BY]->(k:KEYWORD)
        WHERE k.name = $keyword
            AND f.name = $faculty
            AND p.year >= $start_year
            AND p.year <= $end_year
        WITH p.title AS title, p.year AS year, p.numCitations * l.score AS KRC
        RETURN title, year, sum(KRC) AS KRC
        ORDER BY KRC DESC
        LIMIT 10
        """


""" TESTING
# Project Reverse :LABEL_BY Graph
CALL gds.graph.project(
    'keyword-label-pub',                     
    ['PUBLICATION', 'KEYWORD'],                       
    {                                         
        LABEL_BY: { properties: "score", orientation: "REVERSE" }   
    }
)

# Weighted Jaccard Similarity
MATCH (keyword:KEYWORD) where keyword.name = 'internet'
CALL gds.alpha.nodeSimilarity.filtered.stream(
    'keyword-label-pub',
    { 
        degreeCutoff: 1,
        topK: 5,
        relationshipWeightProperty: "score",
        sourceNodeFilter: keyword,
        targetNodeFilter: 'KEYWORD'
    }
)
YIELD node1, node2, similarity
RETURN gds.util.asNode(node1).name AS keyword1,
    gds.util.asNode(node2).name AS keyword2,
    similarity
ORDER BY similarity DESCENDING

# List All GDS Graphs
CALL gds.graph.list()
YIELD graphName, nodeCount, relationshipCount
RETURN graphName, nodeCount, relationshipCount
ORDER BY graphName ASC
"""
