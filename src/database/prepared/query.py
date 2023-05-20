class Query:
    @staticmethod
    def get_university_faculty():
        return f"""
        SELECT faculty.name AS faculty
            , university.name AS institute
        FROM university, faculty
        WHERE faculty.university_id = university.id
            AND university.name = ?
        ORDER BY faculty.name
        LIMIT 10
        """

    @staticmethod
    def create_favorites_table():
        return """
        CREATE TABLE IF NOT EXISTS favorites(  
            title VARCHAR(200) NOT NULL,
            PRIMARY KEY (title)
        );
        """

    @staticmethod
    def drop_favorites_table():
        return """
        DROP TABLE IF EXISTS favorites;
        """

    @staticmethod
    def insert_favorite():
        return """
        INSERT INTO favorites (title) VALUES (?);
        """

    @staticmethod
    def remove_favorite():
        return """
        DELETE FROM favorites WHERE title = ?;
        """

    @staticmethod
    def get_favorites():
        return """
        SELECT * FROM favorites;
        """

    @staticmethod
    def create_crossref_table():
        return """
        CREATE TABLE IF NOT EXISTS crossref(  
            status VARCHAR(50) NOT NULL,
            publication VARCHAR(500) NOT NULL,
            url VARCHAR(1000) NOT NULL,
            PRIMARY KEY (publication)
        );
        """

    @staticmethod
    def insert_crossref():
        return """
        INSERT INTO crossref (status, publication, url) 
            VALUES (?, ?, ?) AS new_row
        ON DUPLICATE KEY UPDATE
            status = new_row.status,
            url = new_row.url;
        """

    @staticmethod
    def get_crossref_url():
        return """
        SELECT url FROM crossref WHERE publication = ?;
        """

    @staticmethod
    def get_crossref_count():
        return """
        SELECT COUNT(*) AS count FROM crossref;
        """

    @staticmethod
    def publication_is_linked():
        return """
        SELECT publication FROM crossref
        WHERE status = "high_match"
        AND publication = ?;
        """
