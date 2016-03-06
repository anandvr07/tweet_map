from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def index():
    
    #return 'Hello World'
    #return app.send_static_file('TweetMap.html')
    #return url_for('static', filename='TweetMap.html')

    return render_template('TweetMap.html', name="name")    

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)