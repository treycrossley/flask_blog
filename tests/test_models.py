def test_user_creation(db, models):
    """
    Test the creation of a user.

    Args:
        db: Database fixture.
        models: Fixture providing access to model classes.

    """
    Users = models["Users"]
    # Create a user
    user = Users(username="test_user", name="Test User", email="test@example.com")
    db.session.add(user)
    db.session.commit()

    # Query the user from the database
    queried_user = Users.query.filter_by(username="test_user").first()

    # Assert that the user was created successfully
    assert queried_user is not None
    assert queried_user.name == "Test User"
    assert queried_user.email == "test@example.com"


def test_password_hashing(models):
    """
    Test the password hashing functionality.

    Args:
        models: Fixture providing access to model classes.

    """
    Users = models["Users"]
    # Create a user with a password
    user = Users(username="test_user", name="Test User", email="test@example.com")
    user.password = "password123"  # This will trigger the setter method

    # Check if the password hash is generated correctly
    assert user.password_hash is not None

    # Verify the password against the hash
    assert user.verify_password("password123") is True
    assert user.verify_password("wrong_password") is False


def test_post_creation(db, models):
    """
    Test the creation of a post.

    Args:
        db: Database fixture.
        models: Fixture providing access to model classes.

    """
    Users = models["Users"]
    Posts = models["Posts"]
    # Create a user
    user = Users(username="test_user", name="Test User", email="test@example.com")
    db.session.add(user)
    db.session.commit()

    # Create a post by the user
    post = Posts(title="Test Post", content="This is a test post.", poster=user)
    db.session.add(post)
    db.session.commit()

    # Query the post from the database
    queried_post = Posts.query.filter_by(title="Test Post").first()

    # Assert that the post was created successfully
    assert queried_post is not None
    assert queried_post.content == "This is a test post."
    assert queried_post.poster == user
