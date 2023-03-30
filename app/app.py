from flask import Flask, render_template, request
from product_manager import CombinedQueryManager
from utils import clean_search_result
import time
import os

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
    query = ""
    title = request.args.get("search")
    description = request.args.get("description")
    category = request.args.get("category")
    rating = request.args.get("rating")
    numOfResults = request.args.get("length")
    sort_filter = request.args.get("price")
    query = "title: "+  title
    fq = []
    if description:
        query += " full_prod_description: " + description
    if rating:
        fq.append(f'rating_rounded:{rating}')
    if category:
        fq.append(f'category:{category}')
    
    print("query", query, fq)

    start_time = time.time()
    results = CombinedQueryManager.search(query=query,numOfResults=numOfResults, fq=fq)
    if sort_filter:
        products = clean_search_result(results=results,query={"title": title, "description":description}, sort_filter=sort_filter)
    else:
        products = clean_search_result(results=results)
    
    end_time = time.time()
    total_time = end_time - start_time
    if len(products)>0:
        return render_template('pages/search.html', products=products, suggestions=[], error=None, search=title, length=numOfResults, total_time=round(total_time, 2), description=description, category=category, rating=rating, price=sort_filter)
    
    elif len(products) == 0:
        suggestions = CombinedQueryManager.spell_check(query=title + " " + description)
        return render_template('pages/search.html', products=products, suggestions=suggestions, error="No Products Found", search=title, length=numOfResults, total_time=round(total_time, 2), description=description, category=category, rating=rating, price=sort_filter)

    return render_template('pages/search.html')

@application.route("/categories")
def categories():
    return render_template('pages/categories.html')

@application.route("/categoriesResult")
def categoriesResults():
    category = request.args.get("category")
    numOfResults = request.args.get("length")

    start_time = time.time()
    results = CombinedQueryManager.search(query=("category: "+category), fq=[], numOfResults=numOfResults)
    products = clean_search_result(results=results)
    end_time = time.time()
    total_time = end_time - start_time
    if len(products)>0:
        return render_template('pages/categories.html', products=products, suggestions=None, error=None, total_time=round(total_time, 2), category=category, length=numOfResults)
    elif len(products) == 0:
        return render_template('pages/categories.html', products=products, suggestions=None, error="No Products exist in this category", total_time=round(total_time, 2), category=category, length=numOfResults)
    
    return render_template('pages/categories.html')


if __name__ == "__main__":
    application.run(debug=True, port=PORT)
