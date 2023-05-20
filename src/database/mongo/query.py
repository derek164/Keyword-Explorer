from bson.son import SON


class Query:
    @staticmethod
    def get_university_faculty(database, institute):
        pipeline = [
            {"$match": {"affiliation.name": {"$regex": f".*{institute}.*"}}},
            {
                "$project": {
                    "_id": 0,
                    "faculty": "$name",
                    "institute": "$affiliation.name",
                }
            },
            {"$sort": SON([("faculty", 1)])},
            {"$limit": 10},
        ]
        return list(database.faculty.aggregate(pipeline))

    @staticmethod
    def get_publications_by_year(database, keyword, start_year, end_year):
        """
        db.publications.aggregate(
            { $unwind: "$keywords" },
            { $match: { $and: [ { "keywords.name": "internet" }, { "year": { $gte: 2012 } }, { "year": { $lte: 2021 } } ] } },
            { $group: { "_id": "$year", "pub_cnt": { $count: {} } } },
            { $sort: { _id: 1 } }
        )
        """

        pipeline = [
            {"$unwind": "$keywords"},
            {
                "$match": {
                    "$and": [
                        {"keywords.name": keyword},
                        {"year": {"$gte": start_year}},
                        {"year": {"$lte": end_year}},
                    ]
                }
            },
            {"$group": {"_id": "$year", "publications": {"$count": {}}}},
            {
                "$project": {
                    "_id": 0,
                    "year": "$_id",
                    "publications": "$publications",
                }
            },
            {"$sort": {"year": 1}},
        ]
        return list(database.publications.aggregate(pipeline))

    @staticmethod
    def get_citations_by_year(database, keyword, start_year, end_year):
        """
        db.publications.aggregate(
            { $unwind: "$keywords" },
            { $match: { $and: [ { "keywords.name": "internet" }, { "year": { $gte: 2012 } }, { "year": { $lte: 2021 } } ] } },
            { $group: { "_id": "$year", "cit_cnt": { $sum: "$numCitations" } } },
            { $sort: { _id: 1 } }
        )
        """

        pipeline = [
            {"$unwind": "$keywords"},
            {
                "$match": {
                    "$and": [
                        {"keywords.name": keyword},
                        {"year": {"$gte": start_year}},
                        {"year": {"$lte": end_year}},
                    ]
                }
            },
            {"$group": {"_id": "$year", "citations": {"$sum": "$numCitations"}}},
            {
                "$project": {
                    "_id": 0,
                    "year": "$_id",
                    "citations": "$citations",
                }
            },
            {"$sort": {"year": 1}},
        ]
        return list(database.publications.aggregate(pipeline))

    @staticmethod
    def get_citations_and_relevance_by_year(database, keyword, start_year, end_year):
        """
        db.publications.aggregate(
            { $unwind: "$keywords" },
            { $match: { $and: [ { "keywords.name": "internet" }, { "year": { $gte: 2012 } }, { "year": { $lte: 2021 } } ] } },
            { $addFields: { "KRC": { $multiply: [ "$numCitations", "$keywords.score" ] } } },
            { $group: { "_id": "$year", "cit_cnt": { $sum: "$numCitations" }, "KRC": { $sum: "$KRC" } } },
            { $sort: { _id: 1 } }
        )
        """

        pipeline = [
            {"$unwind": "$keywords"},
            {
                "$match": {
                    "$and": [
                        {"keywords.name": keyword},
                        {"year": {"$gte": start_year}},
                        {"year": {"$lte": end_year}},
                    ]
                }
            },
            {
                "$addFields": {
                    "KRC": {"$multiply": ["$numCitations", "$keywords.score"]}
                }
            },
            {
                "$group": {
                    "_id": "$year",
                    "citations": {"$sum": "$numCitations"},
                    "relevance": {"$sum": "$KRC"},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "year": "$_id",
                    "citations": "$citations",
                    "relevance": "$relevance",
                }
            },
            {"$sort": {"year": 1}},
        ]
        return list(database.publications.aggregate(pipeline))

    @staticmethod
    def get_keyword_usage(database, keyword, start_year, end_year):
        pipeline = [
            {"$unwind": "$keywords"},
            {
                "$match": {
                    "$and": [
                        {"keywords.name": keyword},
                        {"year": {"$gte": start_year}},
                        {"year": {"$lte": end_year}},
                    ]
                }
            },
            {
                "$addFields": {
                    "KRC": {"$multiply": ["$numCitations", "$keywords.score"]}
                }
            },
            {
                "$group": {
                    "_id": "$year",
                    "citations": {"$sum": "$numCitations"},
                    "relevance": {"$sum": "$KRC"},
                    "publications": {"$count": {}},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "year": "$_id",
                    "citations": "$citations",
                    "relevance": "$relevance",
                    "publications": "$publications",
                }
            },
            {"$sort": {"year": 1}},
        ]
        return list(database.publications.aggregate(pipeline))
