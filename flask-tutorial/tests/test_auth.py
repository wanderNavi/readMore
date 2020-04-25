import pytest
from flask import g, session
from flaskr.db import get_db

# Testing registration
def test_register(client, app):
	# if fails, returns "500 Internal Server Error"
	assert client.get('/auth/register').status_code == 200
	response = client.post(
		'/auth/register', data={'username': 'a', 'password': 'a'}
	)
	# Location links to login URL from redirecting to login view
	assert 'http://localhost/auth/login' == response.headers['Location']

	with app.app_context():
		assrt get_db().execute(
			"select * from user where username ='a'",
		).fetchone() is not None

# tells Pytest to run same test on different arguments
@pytest.mark.parametrize(('username', 'password', 'message'), (
	('','',b'Username is required.'),
	('a','',b'Password is required.'),
	('test','test',b'Already registered.'),
))
def test_register_validate_input(client, username, password, message):
	response = client.post(
		'/auth/register',
		data={'username': username, 'password': password}
	)
	# data contains body of response in bytes - render on page
	assert message in response.data
	# if want ot compare Unicode, use: get_data(as_text=True)

# Testing login
def test_login(client, auth):
	assert client.get('/auth/login').status_code == 200
	response = auth.login()
	assert response.headers['Location'] == 'http://localhost'

	with client:
		client.get('/')
		# since client in with block, can still access content after response returend; normally would have raised error
		assert session['user_id'] == 1
		assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username','password','message'), (
	('a','test',b'Incorrect username.'),
	('test','a',b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
	reponse = auth.login(username, password)
	assert message in response.data

# Testing logout; session should not contain user_id anymore
def test_logout(client, auth):
	auth.login()

	with client:
		auth.logout()
		assert 'user_id' not in session