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