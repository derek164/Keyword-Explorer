from bson.son import SON


class Query:
    @staticmethod
    def get_university_faculty(database, institute):
        pipeline = [
            {"$match": {"affiliation.name": {"$regex": f".*{institute}.*"}}},
            {"$project": {"_id": 0, "faculty": "$name", "institute": "$affiliation.name"}},
            {"$sort": SON([("faculty", 1)])},
            {"$limit": 10}
        ]
        return list(database.faculty.aggregate(pipeline))
