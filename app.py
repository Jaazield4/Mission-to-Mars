 # Import Dependencies
# Use Flask to render a template, redirecting to another url, and creating a url
from flask import Flask, render_template, redirect, url_for
# Use PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo
# Use the scraping code, we'll convert from Jupyter Notebook to Python
import scraping

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# Tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# The URI we'll use to connect our app to Mongo. Setting database name to "mars_app"
mongo = PyMongo(app)

# Setting up routes
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

# Setting up the scrape route
@app.route("/scrape")
def scrape():
    # Assign a new variable that points to our Mongo database
    mars = mongo.db.mars
    # New variable to hold newly scrped data
    mars_data = scraping.scrape_all() # scrape_all fuction from the scraping.py
    # '{}' adds an empty JSON object 
    # 'mars_data' uses the data we already have stored
    # 'upsert=True' indicated to Mongo to create a new document if one doesn't already exist, and new data will be saved
    mars.update({}, mars_data, upsert=True)
    # Redirect to '/' (home page) after scraping the data
    return redirect('/', code = 302)

# Run flask
if __name__ == "__main__":
    app.run(debug = True)