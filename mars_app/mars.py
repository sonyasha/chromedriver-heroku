from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import os

MONGO_URL = os.environ.get('MONGODB_URI')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/mars"

mars = Flask(__name__)

mars.config["MONGO_URI"] = MONGO_URL
mongo = PyMongo(mars)

@mars.route('/')
def home():

    mars_info = list(mongo.db.marsdata.find())
    print(mars_info[-1])
    
    return render_template("index.html", mars_info = mars_info[-1])

@mars.route('/scrape')
def scrape():

    from mars_app.scrape_mars import scrape_mars
    scraped_data = scrape_mars()

    mongo.db.marsdata.insert_one(scraped_data)
    print('data is inserted into mongo')

    return redirect("/", code=302)

if __name__ == "__main__":
    mars.run()

