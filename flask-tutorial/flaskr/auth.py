# Blueprint for authentication functions 

####### IMPORTS #######
import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Set up code to be loaded into HTML template of /auth/register URL
@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None

		# Finding user errors
		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
		elif db.execute(
			'SELECT id FROM user WHERE username = ?', (username,)
		).fetchone() is not None:
			error = 'User {} is already registered.'.format(username)

		if error is None:
			db.execute(
				'INSERT INTO user (username, password) VALUES (?, ?)',
				(username, generate_password_hash(password))
			)
			# Since above query modifies data, need to save changes
			db.commit()

			# Redirect user to login view based on name
			# It's the good old url_for() method generating a url
			return redirect(url_for('auth.login'))

		# Stores failure messages taht can be retrieve 
		flash(error)

	return render_template('auth/register.html')