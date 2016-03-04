import tweepy
import mysql.connector

db = mysql.connector.connect(host="localhost",user="root",password="",database="tweetmapy")
cursor = db.cursor()

consumer_key = "DUrj1zOO3DvpCZ7jGEpfvYUqp"
consumer_secret = "6uLgyG0iD9uvukZYUHOaYCteZF3DyxsBRamBytaPdksflg0ZbS"

access_token = 	"293078152-Ev9SvJ6k77VObLBByUlAzeDxP54qvK75MzUGDTmf"
access_token_secret = "FRfs5pOaETAmrncX4icB7i3cNLkhGQkFz2LpELHnPXxKe"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

search_string = "testtest112233testtest"

tweets = api.search(q=search_string,count=5)

for tweet in tweets:

	tweet_id = tweet.id
	coordinates = api.get_status(tweet_id).place.bounding_box.coordinates[0]

	latitude = (coordinates[0][0] + coordinates[2][0])/2
	longitute = (coordinates[0][1] + coordinates[2][1])/2
	
	sql_query = "INSERT INTO twitterdata values('%d','%f','%f','%s')" % (tweet_id,latitude,longitute,search_string)
	
	try:
	   cursor.execute(sql_query)
	   db.commit()
	except:
	   db.rollback()
