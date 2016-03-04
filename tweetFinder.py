import tweepy
import mysql.connector
import time

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

search_string = "donald trump"


start_time = time.time()

loop_run = 0
place_found = 0
db_new_data = 0
db_old_data = 0


while (db_new_data < 2000) :
	
	loop_run += 1
	print "loop_run %d" % loop_run

	try:
		tweets = api.search(q=search_string,count=100)

		for tweet in tweets:

			tweet_id = tweet.id
			date = tweet.created_at

			if tweet._json.get('place'):
				place_found += 1
				coordinates = tweet.place.bounding_box.coordinates[0]
				longitute = (coordinates[0][0] + coordinates[2][0])/2
				latitude = (coordinates[0][1] + coordinates[2][1])/2
				
				sql_query = "INSERT INTO twitterdata values('%d','%s','%f','%f','%s')" % (tweet_id,date,latitude,longitute,search_string)
				
				try:
				   cursor.execute(sql_query)
				   db.commit()
				   db_new_data += 1
				except:
				   db.rollback()
				   db_old_data += 1

	except:
		time.sleep(15*60) # 15 mins
		continue


print "*******************"
print "loop_run %d" % loop_run
print "place_found %d" % place_found
print "db_new_data %d" % db_new_data
print "db_old_data %d" % db_old_data
print "*******************"