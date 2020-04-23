# Creating SQLite database to connect to

####### IMPORTS #######
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

####### METHODS #######
def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row

	# returning database connection
	return g.db

def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()
	# end of method

# Runs SQL commands 
def init_db():
	db = get_db()

	# open_resource() opens file relative to flaskr package
	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))
	# end of method

# defines command line command that calls init_db()
@click.command('init-db')
@with_appcontext
def init_db_command():
	"""Clear the existing data and create new tables."""
	init_db()
	click.echo('Initialized the database.')
	# end of method

# registuring close_db() and init_db() with application instance
def init_app(app):
	# call function when cleaning up after retun response
	app.teardown_appcontext(close_db)
	# adds new command that can be called with flask command
	app.cli.add_command(init_db_command)
	# end of method