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