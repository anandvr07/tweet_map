import requests
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

import mysql.connector
import json


db = mysql.connector.connect(host="localhost",user="root",password="",database="tweetmapy")
cursor = db.cursor()

host = 'search-tweetmapy-57ul44asdc75otokgszjvdy7uq.us-east-1.es.amazonaws.com'
endpoint = 'http://%s' % host

AWS_ACCESS_KEY = "YOUR AWS_ACCESS_KEY"
AWS_SECRET_KEY = "YOUR AWS_SECRET_KEY"
REGION = "us-east-1"

awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION, 'es')

# response = requests.get(endpoint, auth=awsauth)
# print response.text

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
# # print(es.info())



# es.indices.delete(index="twitterdata")


sql_query = "SELECT tweet_id, date, latitude, longitude, search_key FROM twitterdata"
cursor.execute(sql_query)
data = cursor.fetchall()
for row in data :
	#print row[0], row[1], row[2], row[3], row[4]
	tweet_id = row[0]
	date = row[1]
	latitude = row[2]
	longitude = row[3]
	search_key = row[4]
	es.index(index="twitterdata", doc_type="twitter_doc", id=tweet_id, body={"date": date, "latitude": latitude, "longitude": longitude, "search_key": search_key})


# result_list = []

# search_key = "india"
# query_string = "search_key:%s"% search_key

# res = es.search(index="twitterdata", q=query_string, size=2000)
# hits = res['hits']['hits']
# if hits:
# 	for hit in hits:
# 		latitude = hit['_source']['latitude']
# 		longitude = hit['_source']['longitude']
# 		result_list.append(dict(latitude=latitude, longitude=longitude))


# result_json = json.dumps(result_list)

# with open('data.txt', 'w') as outfile:
#     outfile.write(result_json)




