import requests
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection


import json

host = 'search-tweetmapy-57ul44asdc75otokgszjvdy7uq.us-east-1.es.amazonaws.com'
endpoint = 'http://%s' % host

AWS_ACCESS_KEY = "AKIAJU5RAWBXOYXIRDWA"
AWS_SECRET_KEY = "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"
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
# print(es.info())

print


# es.indices.delete(index="twitterdata")

# tweet_id = 704802275215208448
# date = "2016-03-01 22:55:31"
latitude = 38.407928
longitude = 27.006512 
# search_key = "messi"

# es.index(index="twitterdata", doc_type="twitter_doc", id=tweet_id, body={"date": date, "latitude": latitude, "longitude": longitude, "search_key": search_key})
# es.index(index="twitterdata", doc_type="twitter_doc", id=tweet_id+1, body={"date": date, "latitude": latitude, "longitude": longitude, "search_key": search_key})

# res = es.search(index="twitterdata", q='search_key:"messi"')
# print res
# hits = res['hits']['hits']
# if not hits:
#     print "No matches found"
# else:
# 	for hit in hits:
# 		print hit
# 		latitude = hit['_source']['latitude']
# 		longitude = hit['_source']['longitude']
# 		print latitude
# 		print longitude

result_list = []

res_dict1 = dict(latitude=latitude, longitude=longitude)
res_dict2 = dict(latitude=latitude, longitude=longitude)
res_dict3 = dict(latitude=latitude, longitude=longitude)

result_list.append(res_dict1)
result_list.append(res_dict2)
result_list.append(res_dict3)


result_json = json.dumps(result_list)


print result_json




