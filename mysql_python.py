import mysql.connector

# > mysql
# create database twittmapy;
# use twittmapy;
# create table twitterdata (
# twitt_id INT NOT NULL UNIQUE,
# latitude FLOAT,
# longitude FLOAT,
# search_key VARCHAR(20)
# );

db = mysql.connector.connect(host="localhost",user="root",password="",database="twittmapy")
cursor = db.cursor()
sql_query = "INSERT INTO twitterdata values(1,1.1,-2.6,'hello')"

try:
   cursor.execute(sql_query)
   db.commit()
except:
   db.rollback()

db.close()
