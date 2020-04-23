# This will create the application factory and tell Python to treat flaskr as a package
# An application factory creates a Flask instance within a function instead of globally 

####### IMPORTS #######
import os
from flask import Flask

####### METHODS #######
def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
	)
	# SECRET_KEY SHOULD BE REPLACED WITH SOMETHING RANDOM WHEN DEPLOYED

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# a simple page that says hello
	@app.route('/hello')
	def hello():
		return 'Hello, World!'

	# call db init function from db.py
	from . import db
	db.init_app(app)

	# import and registure authorization blueprints
	from . import auth
	app.register_blueprint(auth.bp)

	# set up blog blueprint
	from . import blog
	app.register_blueprint(blog.bp)
	# does not have url_prefix - main feature 
	app.add_url_rule('/', endpoint='index')
	# associating endpoint with '/' - set url_for('index') and url_for('blog.index') to both work (makes same / URL)

	return app