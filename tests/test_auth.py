# Test login route
from flask import session
from app.extensions import bcrypt
import pdb

from app.blueprints import auth


def test_login_route(client):
    response = client.get("/auth/login")
    assert response.status_code == 200


def test_login_form_rendered(client):
    # Simulate GET request to login page to check if the login form is rendered
    response = client.get("/auth/login")

    # Check if the login form is rendered
    assert response.status_code == 200
    assert (
        b"<form" in response.data
    )  # Assuming the login form is rendered as an HTML form
    assert (
        b"Username" in response.data
    )  # Assuming the login form contains a field for username
    assert (
        b"Password" in response.data
    )  # Assuming the login form contains a field for password


# def test_login_with_invalid_credentials(client):
#     # Simulate login request with invalid credentials
#     # response = client.post('/auth/login', data={'username': 'invalid_user', 'password': 'invalid_password'}, follow_redirects=True)
#     response = client.post(
#             '/auth/login', data={
#                 'form-login-username': 'a',
#                 'form-login-password': 'a'
#             })
#     # Check if the login form is rendered again with appropriate error message
#     pdb.set_trace()
#     assert response.status_code == 200  # Assuming the login form is rendered again
#     assert b'Wrong Password - Try again!' in response.data or b'User does not exist' in response.data  # Assuming an error flash message is displayed

#     # Check if user is not logged in (session does not contain user ID)
#     assert '_user_id' not in session

# # Test logout route
# def test_logout_route(client):
#     response = client.get('/auth/logout')
#     assert response.status_code == 302  # Redirects after logout
#     assert session.get('_user_id') is None  # User is logged out
