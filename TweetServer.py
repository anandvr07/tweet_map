from __future__ import print_function
import sys

import json
import tweepy
import requests

from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

from flask import Flask, request, render_template
app = Flask(__name__)

host = 'search-tweetmapy-57ul44asdc75otokgszjvdy7uq.us-east-1.es.amazonaws.com'

AWS_ACCESS_KEY = "YOUR AWS_ACCESS_KEY"
AWS_SECRET_KEY = "YOUR AWS_SECRET_KEY"
REGION = "us-east-1"

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION, 'es')

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

@app.route('/')
def index():
	return render_template('TweetMap.html', name="TweetMap")


@app.route('/search', methods=['POST'])
def search():
	search_key = request.form['search_key']
	
	search_key = search_key.lower()
	#print(search_key, file=sys.stderr)

	query_string = "search_key:%s"% search_key
	result_list = []

	res = es.search(index="twitterdata", q=query_string, size=2000)
	hits = res['hits']['hits']
	if hits:
		for hit in hits:
			latitude = hit['_source']['latitude']
			longitude = hit['_source']['longitude']
			result_list.append(dict(latitude=latitude, longitude=longitude))

	result_json = json.dumps(result_list)
	return result_json


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
