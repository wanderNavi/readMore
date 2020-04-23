# Creating blog blueprint

####### IMPORTS #######
from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

####### METHODS #######
bp = Blueprint('blog', __name__)

# fetching post by id to check if author matches logged in user
def get_post(id, check_author=True):
	post = get_db().execute(
		'SELECT p.id, title, body, created, author_id, username FROM post p JOIN user u ON p.author_id = u.id WHERE p.id = ?', (id,)
	).fetchone()

	if post is None:
		# abort raises a special exception that returns an HTTP status code with an option message
		# 404 - "Not found"
		abort(404, "Post id {0} doesn't exist.".format(id))

	# check_author written in way that allows anyone to still get the post to view, though can't edit if not author
		# ex. show individual post on page where user doesn't matter since not modifying post
	if check_author and post['author_id'] != g.user['id']:
		# 403 - "Forbidden"
		abort(403)

	# 401 - "Unauthorized," we already taking care of by redirecting user to login page 
	return post

####### ROUTES #######
@bp.route('/')
def index():
	db = get_db()
	posts = db.execute(
		'SELECT p.id, title, body, created, author_id, username FROM post p JOIN user u ON p.author_id = u.id ORDER BY created DESC'
	).fetchall()
	return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		error = None

		if not title:
			error = 'Title is required.'

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)', (title, body, g.user['id'])
			)
			db.commit()
			return redirect(url_for('blog.index'))

	return render_template('blog/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required