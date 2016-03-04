from flask import Flask
app = Flask(__name__)

# json structure : { twitt_type, latitude, longitude }

import json

resList = []

nycList = []
dict1 = dict(twitt_type="nyc", latitude="40", longitude="-74")
nycList.append(dict1);

dict2 = dict(twitt_type="nyc", latitude="35", longitude="-87")
nycList.append(dict2);

trumpList = []
dict3 = dict(twitt_type="trump", latitude="41", longitude="-70")
trumpList.append(dict3);

resList.append(dict(nyc=nycList));
resList.append(dict(trump=trumpList));

print resList

@app.route('/')
def index():
	return json.dumps(resList)

if __name__ == '__main__':
    app.run()
