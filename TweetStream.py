import json
import random
import tweepy
import datetime

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import requests
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection


consumer_key = "DUrj1zOO3DvpCZ7jGEpfvYUqp"
consumer_secret = "6uLgyG0iD9uvukZYUHOaYCteZF3DyxsBRamBytaPdksflg0ZbS"

access_token =  "293078152-Ev9SvJ6k77VObLBByUlAzeDxP54qvK75MzUGDTmf"
access_token_secret = "FRfs5pOaETAmrncX4icB7i3cNLkhGQkFz2LpELHnPXxKe"

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

search_key_array = ["donald trump", "barack obama", "india", "america", "ronaldo", "messi", "twitter", "facebook", "house of cards", "super bowl"]

track_string = search_key_array[0]
for index in range(len(search_key_array)-1):
    track_string += " , %s" % search_key_array[index+1]


class StdOutListener(StreamListener):
    def on_data(self, data):
        
        tweet = json.loads(data)

        search_key = ""
        for key in search_key_array:
            if key in str(tweet).lower():
                search_key = key
                break

        try:

            if tweet.has_key('id'):
                tweet_id = tweet['id']

            if tweet['coordinates']:
                coordinates = tweet['coordinates']['coordinates']
                longitude = coordinates[0]
                latitude = coordinates[1]
                
            elif tweet['place'] and tweet['place']['bounding_box'] and tweet['place']['bounding_box']['coordinates']:
                coordinates = tweet['place']['bounding_box']['coordinates'][0]
                longitude = (coordinates[0][0] + coordinates[2][0])/2
                latitude = (coordinates[0][1] + coordinates[2][1])/2

            else :
                return True

        except:
            return True

        # print search_key, tweet_id, latitude, longitude
        es.index(index="twitterdata", doc_type="twitter_doc", id=tweet_id, body={"latitude": latitude, "longitude": longitude, "search_key": search_key})

        return True

    def on_error(self, status):
        print status
        return True

def main():
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    while True:
        try:
            stream.filter(track=[track_string])
            break
        except tweepy.TweepError:
            nsecs=random.randint(60,63)
            time.sleep(nsecs)   


if __name__ == '__main__':
    main()
