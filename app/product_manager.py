#Sample query:
#User search: hammer tools
#query = 'title:"hammer tools"'
#
#User search: 6 inch hammer tools
#query = 'title: "6 inch hammer tool" AND full_prod_description: "6 inch hammer tools"'
#
#Filter by category
#query = 'category: "DIY_Tools"'


import pysolr

class CombinedQueryManager:
    # Create a client instance. The timeout and authentication options are not required.
    solr = pysolr.Solr('http://localhost:8983/solr/Combined', always_commit=True)

    @staticmethod
    def healthCheck():
        CombinedQueryManager.solr.ping()


    @staticmethod
    def search(query):
        try:
            results = CombinedQueryManager.solr.search(query, rows = 100)
        except:
            print("Error")
            return []
        response = list(map(lambda x: x, results))
        return response

    @staticmethod
    def search(query,numOfResults):
        try:
            results = CombinedQueryManager.solr.search(query, rows = numOfResults)
        except:
            print("Error")
            return []
        response = list(map(lambda x: x, results))
        return response

    @staticmethod
    def byTopic(query, topic):
        try:
            results = CombinedQueryManager.solr.search(query, fq=f"topic:{topic}", rows=100)
        except:
            print("Error")
            return []
        response = list(map(lambda x: x, results))
        return response

    @staticmethod
    def byPID(PID):
        try:
            results = CombinedQueryManager.solr.search(f"product_id:{PID}", rows=100)
        except:
            print("Error")
            return []
        response = list(map(lambda x: x, results))
        return response