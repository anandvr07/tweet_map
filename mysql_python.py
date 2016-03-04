import mysql.connector

# > mysql
# create database tweetmapy;
# use tweetmapy;
# create table twitterdata (
# tweet_id BIGINT NOT NULL UNIQUE,
# date DATETIME,
# latitude FLOAT(10,6),
# longitude FLOAT(10,6),
# search_key VARCHAR(50)
# );

db = mysql.connector.connect(host="localhost",user="root",password="",database="tweetmapy")
cursor = db.cursor()

sql_query = "INSERT INTO twitterdata values('705675654323429376','-73.948775','40.655138','testtest112233testtest')"
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
      date = row[1]
      latitude = row[2]
      longitude = row[3]
      search_key = row[4]
      
      res_dict = dict(tweet_id=tweet_id, latitude=latitude, longitude=longitude, search_key=search_key)

      print res_dict
except:
   print "Error: unable to fecth data"


db.close()
