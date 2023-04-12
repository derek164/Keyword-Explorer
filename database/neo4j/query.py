class Query:
    def format_output(query):
        def wrap(tx, **kwargs):
            return [dict(record) for record in tx.run(query(**kwargs), **kwargs)]

        return wrap

    @staticmethod
    @format_output
    def get_university_faculty(institute):
        return """
        MATCH (f:FACULTY)-[:AFFILIATION_WITH]->(i:INSTITUTE)
        WHERE i.name CONTAINS $institute
        RETURN f.name AS faculty, i.name AS institute
        ORDER BY faculty
        LIMIT 10;
        """