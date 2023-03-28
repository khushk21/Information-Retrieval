import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from reviews_manager import CombinedReviewQueryManager

categories = {'DIY_Tools': 'DIY & Tools', 'Office Products': 'Office Products', 'Sports Apparel_Equipment': 'Sports Apparel & Equipment', "Womens Fashion": "Women's Fashion", "Kitchen & Dining": "Kitchen & Dining" }
sentiment = {1: "Negative", 2: "Negative", 3: "Neutral", 4: "Positive", 5: "Positive"}

def clean_search_result(results, query=None, sort_filter=None):
    products = []
    for result in results:
        product = dict()
        raw_reviews = CombinedReviewQueryManager.byPID(PID=result['product_id'][0])
        cleaned_reviews = clean_reviews(raw_reviews)
        if len(cleaned_reviews)>0:
            product['reviews'] = cleaned_reviews
        product['PID'] = result['product_id'][0]
        if 'image_url' in result:
            product['image_url'] = result['image_url'][0]
        else:
            product['image_url']= 'https://via.placeholder.com/150x150'
        product['price'] = result['price'][0]
        if 'rating' in result:
            product['rating'] = int(round(result['rating'][0],0))
            product['sentiment'] = sentiment[product['rating']]
        else:
            product['rating'] = 'Not Rated Yet'
            product['sentiment'] = 'No sentiment available'
        if 'title' in result:
            product['title'] = result['title'][0]
        else:
            product['title'] = 'No title available'
        if 'full_prod_description' in result:
            product['full_prod_description'] = result['full_prod_description'][0]
        else:
            product['full_prod_description'] = 'Descripton Unavailable'
        if 'product_link' in result:
            product['product_link'] = result['product_link'][0]
        else:
            product['product_link'] = "https://amazon.sg"

        product['category'] = categories[result['category'][0]]
        products.append(product)
    
    if sort_filter == "1":
        products = sorted(products, key=lambda x: x['price'])
    elif sort_filter == "2":
        products = sorted(products, key=lambda x: x['price'], reverse=True)
    elif sort_filter == '3':
        products = rank_products(query=query, products=products) 
    
    return products


def clean_reviews(reviews):
    cleaned_reviews = []
    for review in reviews:
        temp_review = dict()
        if 'review_url' in review:
            temp_review['review_url'] = review['review_url'][0]
        else:
            temp_review['review_url'] = 'https://amazon.sg'
        if 'date_country' in review:
            temp_review['date_country'] = review['date_country'][0]
        else:
            temp_review['date_country'] = 'Date Unavailable'
        if 'review_title' in review:
            temp_review['review_title'] = review['review_title'][0]
        else:
            temp_review['review_title'] = 'No Title'
        if 'review_rating' in review:
            temp_review['review_rating'] = int(review['review_rating'][0])
        else:
            temp_review['review_rating'] = 'No rating found'
        temp_review['review_content'] = review['review_content'][0]
        cleaned_reviews.append(temp_review)
    
    return cleaned_reviews

def rank_products(query, products):
    try:
        product_description = [product['full_prod_description'] for product in products]
        vectorizer = TfidfVectorizer()
        description = product_description.copy()
        description.insert(0, query)
        vectors = vectorizer.fit_transform(description)
        feature_names = vectorizer.get_feature_names()
        dense = vectors.todense().tolist()
        query_tfidf = pd.DataFrame([dense[0]], columns=feature_names)
        document_tfidf = pd.DataFrame(dense[1:], columns=feature_names)
        all_scores = list(document_tfidf.dot(query_tfidf.iloc[0]))
        for i in range(len(all_scores)):
            all_scores[i] = [i, all_scores[i]]
        
        all_scores = np.array(all_scores)
        all_scores = all_scores[all_scores[:, 1].argsort(axis=0)][::-1]

        ranked_products = []
        print("scores", all_scores)
        for score in all_scores:
            product = products[int(score[0])]
            ranked_products.append(product)
        
        return ranked_products
    
    except Exception as e:
        print("Error")
        return products



