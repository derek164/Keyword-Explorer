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