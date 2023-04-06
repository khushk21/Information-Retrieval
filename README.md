# Information-Retrieval

CZ4034 - Information Retrieval

Search Engine for Amazon Products

This project contains 3 main sections
1. Crawling

    We utilized BeautifulSoup to crawl Amazon Products and Reviews and collected data regarding products from the categories- Women's Fashion, DIY & Tools, Sports Apparel & Equipment, Kitchen & Dining and Office Products.
    The Crawled data had the following columns:
    | Field Name | Description |
    | ---------- | ----------- |
    | product_id   | Unique ASIN number of Amazon Product|
    | product_link | The url to the Amazon product page|
    | title       | Contains the title of the product|
    | rating    | The average rating of the product, based on the total reviews|
    | image_url |The url of the image displayed on the product page|
    | prod_desc| The descriptions about the product, which could include the qualities or functions or usage instruction|
    | review_title  | Contains the title of the review |
    | review_content  | The main content of the review left by the user |
    | review_rating  | Rating given by user for the review, ranging from a minimum of 0 to a maximum of 5 |
    | review_date  | Date where review is submitted, in dd/month/yyyy format eg. “1 July 2021” |
    | total_review | The number of review count for the specific Amazon product that the reviewer is submitting the review for|
    | country | Location of reviewer when he/she left the review |
<br/>

2. Indexing and Querying
    
    Indexing is a way to optimize the performance of a database by minimizing the number of disk accesses required when a query is processed.  We created an inverted index using Solr to optimize the search process. Inverted index helps optimizing the search process and allows fast full text search, at a cost of increased processing when a document is added. We also incorporated the spell check feature into our system which was implemented with the help of the n-grams algorithm.

3. Sentiment Analysis

    Model Performance:
    | Model | F1 Score | Accuracy | Precision | Recall |
    | ----- | -------- | -------- | --------- | ------ |
    | Ensemble Model (BERT, RoBERTa and XLNet)  | 0.813  | 0.887  | 0.848   | 0.825 |
    
   
<br/>

## Quickstart

To start solr:

```bash
cd solr
./bin/solr start
```

To start the flask app:

```bash
cd app
python app.py
```
