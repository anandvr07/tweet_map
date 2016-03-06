import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import mysql.connector
import json
import random

consumer_key = "DUrj1zOO3DvpCZ7jGEpfvYUqp"
consumer_secret = "6uLgyG0iD9uvukZYUHOaYCteZF3DyxsBRamBytaPdksflg0ZbS"
access_token =  "293078152-Ev9SvJ6k77VObLBByUlAzeDxP54qvK75MzUGDTmf"
access_token_secret = "FRfs5pOaETAmrncX4icB7i3cNLkhGQkFz2LpELHnPXxKe"

db = mysql.connector.connect(host="localhost",user="root",password="",database="tweetmapy")
cursor = db.cursor()


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        #print data
        
        tweet = json.loads(data)

        tweet_id = tweet['id']

        date = tweet['created_at']

        # if tweet['geo'] :
        #     coordinates = tweet['geo']['coordinates']
        #     latitude = coordinates[0]
        #     longitute = coordinates[1]

        if tweet['coordinates'] :
            coordinates = tweet['coordinates']['coordinates']
            longitute = coordinates[0]
            latitude = coordinates[1]

        elif tweet['place'] :
            coordinates = tweet['place']['bounding_box']['coordinates'][0]
            longitute = (coordinates[0][0] + coordinates[2][0])/2
            latitude = (coordinates[0][1] + coordinates[2][1])/2

        print longitute
        print latitude

        # elif tweet['location'] :
        #     print "tweet - location"
        #     print tweet['location'] 
        #     coordinates = tweet['location']['geo']['coordinates'][0]
        #     print coordinates
        #     longitute = (coordinates[0][0] + coordinates[2][0])/2
        #     latitude = (coordinates[0][1] + coordinates[2][1])/2
        #     print longitute
        #     print latitude

        else :
            return True

        return True

    def on_error(self, status):
        print status

def main():
    #This handles Twitter authetification and the connection to Twitter Streaming API
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    while True:
        try:
            # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
            # stream.filter(locations=[-125,25,-65,48], async=False)
            stream.filter(track=["donald trump"])
            break
        except tweepy.TweepError:
            nsecs=random.randint(60,63)
            time.sleep(nsecs)   


if __name__ == '__main__':
    main()