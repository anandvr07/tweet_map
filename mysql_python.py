import mysql.connector

# > mysql
# create database tweetmapy;
# use tweetmapy;
# create table twitterdata (
# tweet_id INT NOT NULL UNIQUE,
# latitude FLOAT,
# longitude FLOAT,
# search_key VARCHAR(20)
# );

db = mysql.connector.connect(host="localhost",user="root",password="",database="tweetmapy")
cursor = db.cursor()

sql_query = "INSERT INTO twitterdata values(4,1.1,-2.6,'hello')"
try:
   cursor.execute(sql_query)
   db.commit()
except:
   db.rollback()


sql_query = "SELECT * FROM twitterdata"
try:
   cursor.execute(sql_query)
   
   results = cursor.fetchall()
   for row in results:
      tweet_id = row[0]
      latitude = row[1]
      longitude = row[2]
      search_key = row[3]
      
      res_dict = dict(tweet_id=tweet_id, latitude=latitude, longitude=longitude, search_key=search_key)

      print res_dict
except:
   print "Error: unable to fecth data"


db.close()
