# TEST HYPOTHETICAL HTML WEBSERVER PAGE
# Do I really need this to build the html interaction?

############# IMPORTS#############
# LIBRARIES
from flask import Flask, render_template, request
from sqlalchemy import create_engine

############# GLOBAL VARIABLES #############
# CONNECT TO DATABASE

############# METHODS #############

############# PAGES #############
app = Flask(__name__)

# landing page
@app.route('/')
def home():
    page = landing.main()
    return page

###############################
app.run(host='0.0.0.0', port=5000, debug=True)