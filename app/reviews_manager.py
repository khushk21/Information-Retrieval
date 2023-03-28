# Sample query
#User search: very good hammer
#query = 'review:"very good hammer"'
#
#Filter by category
#query = 'category: "DIY_Tools"'

import pysolr


class CombinedReviewQueryManager:
    # Create a client instance. The timeout and authentication options are not required.
    solr = pysolr.Solr('http://localhost:8983/solr/Combined_reviews', always_commit=True)

    @staticmethod
    def healthCheck():
        CombinedReviewQueryManager.solr.ping()

    @staticmethod
    def search(query):
        try:
            results = CombinedReviewQueryManager.solr.search(query, rows = 100)
        except:
            print("Error")
            return []
        response = list(map(lambda x: x, results))
        return response

    @staticmethod
    def search(query,numOfResults):
        try:
            results = CombinedReviewQueryManager.solr.search(query, rows = numOfResults)
        except:
            print("Error")
            return []
        response = list(map(lambda x: x, results))
        return response

    @staticmethod
    def byTopic(query, topic):
        try:
            results = CombinedReviewQueryManager.solr.search(query, fq=f"topic:{topic}", rows=100)
        except:
            print("Error")
            return []
        response = list(map(lambda x: x, results))
        return response

    @staticmethod
    def byPID(PID):
        try:
            results = CombinedReviewQueryManager.solr.search(f"product_id:{PID}", rows=100)
        except:
            print("Error")
            return []
        response = list(map(lambda x: x, results))
        return response