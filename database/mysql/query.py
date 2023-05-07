class Query:    
    @staticmethod
    def get_university_faculty(institute):
        return f"""
        SELECT faculty.name AS faculty
            , university.name AS institute
        FROM university, faculty
        WHERE faculty.university_id = university.id
            AND university.name like "%{institute}%"
        ORDER BY faculty.name
        LIMIT 10
        """
    
    @staticmethod
    def get_faculty_publications(faculty, keyword, start_year, end_year):
        return f"""
        SELECT publication.title
            , publication.year
            , publication.num_citations * publication_keyword.score AS KRC
        FROM faculty
        JOIN faculty_publication ON faculty_publication.faculty_id = faculty.id
        JOIN publication ON publication.id = faculty_publication.publication_id
        JOIN publication_keyword ON publication_keyword.publication_id = publication.id
        JOIN keyword ON keyword.id = publication_keyword.keyword_id
        WHERE keyword.name = "{keyword}" 
            AND faculty.name LIKE "{faculty}"
            AND publication.year >= {start_year}
            AND publication.year <= {end_year}
        ORDER BY KRC DESC
        LIMIT 10;
        """
    
    @staticmethod
    def get_most_relevant_publications(keyword, start_year, end_year):
        return f"""
        SELECT publication.title
            , publication.year
            , publication.num_citations * publication_keyword.score AS KRC
        FROM publication
        JOIN publication_keyword ON publication_keyword.publication_id = publication.id
        JOIN keyword ON keyword.id = publication_keyword.keyword_id
        WHERE keyword.name = "{keyword}"
            AND publication.year >= {start_year}
            AND publication.year <= {end_year}
        ORDER BY KRC DESC
        LIMIT 10;
        """
    
    @staticmethod
    def get_keywords():
        return """
        SELECT name FROM keyword ORDER BY name;
        """
    
    @staticmethod
    def get_favorites():
        return """
        SELECT * FROM favorites;
        """

    @staticmethod
    def get_faculty_top_scores():
        return f"""
        SELECT DISTINCT f.name faculty_name, 
        k.name keyword_name,
        score
        FROM faculty_keyword fk
        INNER JOIN faculty f
            ON fk.faculty_id = f.id
        INNER JOIN keyword k
            ON fk.keyword_id = k.id
        ORDER BY score DESC
        LIMIT 15;
        """
        