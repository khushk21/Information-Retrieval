from flask import Flask, render_template, request, send_file, send_from_directory
from product_manager import CombinedQueryManager
import os
# from utils import filter

BASE_DIR = os.getcwd()

application = Flask(__name__)

PORT = os.getenv('PORT', 8000)


@application.route("/")
def index():
    return render_template('pages/index.html')


@application.route("/search")
def search():
    return render_template('pages/search.html')


@application.route("/searchResults")
def search_results():
    query = dict()
    title = request.args.get("search")
    description = request.args.get("description")
    category = request.args.get("category")
    rating = request.args.get("rating")
    # query["title"] = title if title else ""
    query = "title: "+  title
    # query['full_prod_description'] = description if description else ""
    # query['category'] = category if category else ""
    # query['rating'] = rating if rating else ""
    print("query", query)
    result = CombinedQueryManager.search(query=query,numOfResults=50)
    print("result", result)

    # if search_query:
    #     tweets, suggestions = filter(search_query, ranking, countries)
    #     countries = "&".join([f"country{i}="+request.args.get(f"country{i}") for i in range(1, 11) if request.args.get(f"country{i}") != None])

    #     if len(suggestions) == 0:
    #         suggestions = []
    #     if len(tweets) == 0:
    #         return render_template('pages/search.html', search_query = search_query, error = "No tweets Found", tweets = None, suggestions=suggestions, countries=countries)
    #     return render_template('pages/search.html', search_query = search_query, error= None, tweets = tweets, suggestions=suggestions, countries=countries)

    # return render_template('pages/search.html')


# @application.route("/map")
# def geospatial_search():
#     return render_template("pages/map.html")


@application.route("/plotly")
def plotly():
    filename = request.args.get('filename')
    return send_from_directory(f"{BASE_DIR}/static/js", filename=filename)


if __name__ == "__main__":
    application.run(debug=True, port=PORT)
