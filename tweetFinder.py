import tweepy
import time
import datetime
import random
import mysql.connector

search_key_array = ["donald trump", "barack obama", "india", "america", "ronaldo", "messi", "twitter", "facebook", "house of cards", "super bowl"]
search_key_array_edit = ["donald trump", "barack OR obama", "india", "america OR usa", "ronaldo", "messi", "twitter", "facebook", "houseofcards OR 'house of cards'", "super bowl"]


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

access_index = 1

length = len(search_key_array)

while (access_index < length) :
	search_key = search_key_array[access_index]
	search_key_edit = search_key_array_edit[access_index]
	access_index += 1

	# start_date = "2016-03-01"
	# end_date = "2016-03-02"
	# search_string = "%s since:%s until:%s" % (search_key_edit,start_date,end_date)

	#search_string = "india OR ronaldo OR messi OR facebook since:%s until:%s" % (start_date,end_date)

	search_string = search_key_edit

	print search_string

	loop_run = 0
	place_found = 0
	db_new_data = 0
	db_old_data = 0

	cur_max_id = 704460048181944321				 

	while (db_new_data < 350) :	
		loop_run += 1
		print "loop_run %d" % loop_run

		try:
			tweets = api.search(q=search_string, count=100, max_id=cur_max_id-1)
			
			for tweet in tweets:

				tweet_id = tweet.id
				date = tweet.created_at
				#print "%s %s" % (date, tweet_id)
				cur_max_id = tweet_id

				if tweet._json.get('coordinates'):
					place_found += 1
					coordinates = tweet.coordinates.get('coordinates')
					longitute = coordinates[0]
					latitude = coordinates[1]

				elif tweet._json.get('place'):
					place_found += 1
					coordinates = tweet.place.bounding_box.coordinates[0]
					longitute = (coordinates[0][0] + coordinates[2][0])/2
					latitude = (coordinates[0][1] + coordinates[2][1])/2

				else:
					continue
				
				#print tweet.text

				# if "india" in tweet.text.lower() or "india" in str(tweet).lower():
				# 	search_key = "india"
				# elif "ronaldo" in tweet.text.lower() or "ronaldo" in str(tweet).lower():
				# 	search_key = "ronaldo"
				# elif "messi" in tweet.text.lower() or "messi" in str(tweet).lower() :
				# 	search_key = "messi"
				# elif "facebook" in tweet.text.lower() or "facebook" in str(tweet).lower():
				# 	search_key = "facebook"
				# else :
				# 	continue

				#print search_key

				sql_query = "INSERT INTO twitterdata values('%d','%s','%f','%f','%s')" % (tweet_id,date,latitude,longitute,search_key)
				
				#print sql_query

				try:
				   cursor.execute(sql_query)
				   db.commit()
				   db_new_data += 1
				   print db_new_data
				   print "** new entry for '%s' with id '%d'" % (search_key,tweet_id)
				except:
				   db.rollback()
				   db_old_data += 1
				   print "** old entry for '%s' with id '%d'" % (search_key,tweet_id)

				#time.sleep(1) # to avoid twitter considering our request as a DDOS attack
		
		# except tweepy.TweepError as e:
		# 	print "error"
		# 	if e.message[0]['code']==88 :  #RateLimitError
		# 		print "** Sleeping for 15mins from %s **" % datetime.datetime.now()
		# 		time.sleep(15*60)
		# 	else :
		# 		print e

		except tweepy.TweepError:
			# print "** Sleeping for 15mins from %s **" % datetime.datetime.now()
			# time.sleep(15*60)
			print "~~ sleep state : %s ~~ " % datetime.datetime.now()
			nsecs=random.randint(60,63)
			time.sleep(nsecs)


	print "*******************"
	print "loop_run %d" % loop_run
	print "place_found %d" % place_found
	print "db_new_data %d" % db_new_data
	print "db_old_data %d" % db_old_data
	print "*******************"