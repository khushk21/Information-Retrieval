#Sample query:
#User search: hammer tools
#query = 'title:"hammer tools"'
#
#User search: 6 inch hammer tools
#query = 'title: "6 inch hammer tool" AND full_prod_description: "6 inch hammer tools"'
#
#Filter by category
#query = 'category: "DIY_Tools"'


from unicodedata import category
import pysolr
import requests

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
    def search(query,numOfResults, fq):
        try:
            results = CombinedQueryManager.solr.search(query,fq=fq, rows = numOfResults)
        except:
            print("Error")
            return []
        response = list(map(lambda x: x, results))
        return response

    @staticmethod
    def byCategory(query, category, numOfResults):
        try:
            results = CombinedQueryManager.solr.search(query, fq=f"category:{category}", rows=numOfResults)
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
    
    @staticmethod
    def spell_check(query):
        try:
            url = f"http://localhost:8983/solr/Combined/spell?spellcheck.q={query}&spellcheck=true"
            response = requests.get(url)
            suggestions = response.json()["spellcheck"]["suggestions"][1]["suggestion"]
            if len(suggestions)>0:
                suggestions = sorted(suggestions, key=lambda x: x['freq'], reverse=True)
            print("s", suggestions)
        
        except:
           print("Error in getting spell check suggestions")
           return []
        
        return suggestions