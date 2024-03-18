import pytest
import pdb
from flask_wtf.csrf import generate_csrf

def test_login_form_validation(app, forms):
    LoginForm=forms['LoginForm']
    with app.test_request_context('/auth/login', method='POST', data={'username': 'valid_username', 'password': 'valid_password'}):
        form = LoginForm()
        form.csrf_token.data = generate_csrf()
        # Test valid data
        assert form.validate()  # Should pass validation with valid data

        # Test missing username
        form.username.data = ''
        form.password.data = 'valid_password'
        assert not form.validate()  # Should fail validation without username

        # Test missing password
        form.username.data = 'valid_username'
        form.password.data = ''
        assert not form.validate()  # Should fail validation without password

# Test for PostForm
def test_post_form_validation(app, forms):
    PostForm = forms['PostForm']
    with app.test_request_context('/submit_post', method='POST', data={'title': 'Test Post', 'content': 'This is a test post.', 'author': 'Test Author', 'slug': 'test-post'}):
        form = PostForm()
        form.csrf_token.data = generate_csrf()
        
        # Test valid data
        assert form.validate()  # Should pass validation with valid data

        # Test missing title
        form.title.data = ''
        assert not form.validate()  # Should fail validation without title

        # Test missing content
        form.title.data = 'Test Post'
        form.content.data = ''
        assert not form.validate()  # Should fail validation without content

        # Test missing slug
        form.content.data = 'This is a test post.'
        form.slug.data = ''
        assert not form.validate()  # Should fail validation without slug

# Test for SearchForm
def test_search_form_validation(app, forms):
    SearchForm = forms['SearchForm']
    with app.test_request_context('/search', method='POST', data={'searched': 'keyword'}):
        form = SearchForm()
        form.csrf_token.data = generate_csrf()
        
        # Test valid data
        assert form.validate()  # Should pass validation with valid data

        # Test missing searched term
        form.searched.data = ''
        assert not form.validate()  # Should fail validation without searched term

# Test for NamerForm
def test_namer_form_validation(app, forms):
    NamerForm = forms['NamerForm']
    with app.test_request_context('/get_name', method='POST', data={'name': 'John'}):
        form = NamerForm()
        form.csrf_token.data = generate_csrf()
        
        # Test valid data
        assert form.validate()  # Should pass validation with valid data

        # Test missing name
        form.name.data = ''
        assert not form.validate()  # Should fail validation without name

# Test for PasswordForm
def test_password_form_validation(app, forms):
    PasswordForm = forms['PasswordForm']
    with app.test_request_context('/register', method='POST', data={'email': 'test@example.com', 'pw': 'password'}):
        form = PasswordForm()
        form.csrf_token.data = generate_csrf()
        
        # Test valid data
        assert form.validate()  # Should pass validation with valid data

        # Test missing email
        form.email.data = ''
        assert not form.validate()  # Should fail validation without email

        # Test missing password
        form.email.data = 'test@example.com'
        form.pw.data = ''
        assert not form.validate()  # Should fail validation without password

# Test for UserForm
def test_user_form_validation(app, forms):
    UserForm = forms['UserForm']
    with app.test_request_context('/register_user', method='POST', data={'name': 'Test User', 'username': 'test_user', 'email': 'test@example.com', 'favorite_pizza_place': 'Pizza Hut', 'password': 'password', 'password2': 'password'}):
        form = UserForm()
        form.csrf_token.data = generate_csrf()
        
        # Test valid data
        assert form.validate()  # Should pass validation with valid data

        # Test missing name
        form.name.data = ''
        assert not form.validate()  # Should fail validation without name

        # Test missing username
        form.name.data = 'Test User'
        form.username.data = ''
        assert not form.validate()  # Should fail validation without username

        # Test missing email
        form.username.data = 'test_user'
        form.email.data = ''
        assert not form.validate()  # Should fail validation without email

        # Test missing password
        form.email.data = 'test@example.com'
        form.password.data = ''
        assert not form.validate()  # Should fail validation without password

        # Test passwords mismatch
        form.password.data = 'password'
        form.password2.data = 'different_password'
        assert not form.validate()  # Should fail validation with mismatched passwords
