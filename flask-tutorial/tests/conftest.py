# Calls factory and passes test_config to set up application and database for testing instead of local development configuration 
# SIDENOTE: test account navi_test -> develop (or development?)

####### IMPORTS #######
import os
import tempfile
import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
	_data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
	# creates and opens temporary file, returns file object and path
	db_fd, db_path = tempfile.mkstemp()

	app = create_app({
		'TESTING': True, # Flask knows in test mode
		'DATABASE': db_path, # override path so go to temp path instead of instance folder 
	})

	with app.app_context():
		init_db()
		get_db().executescript(_data_sql)

	yield app

	os.close(db_fd)
	os.unlink(db_path)

@pytest.fixture
def client(app):
	# can use client to make requests to application without running the server
	return app.test_client()

@pytest.fixture
def runner(app):
	# creates runner that can call Click commands registered with app
	return app.test_cli_runner()