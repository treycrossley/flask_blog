def test_create_app(app):
    """
    Test whether the app is created correctly for testing.

    Args:
        app: Flask application instance.

    Asserts:
        - Whether the app is in testing mode.
        - Whether the TESTING configuration is set to True.
    """
    assert app.testing
    assert app.config["TESTING"]


def test_blueprints_registered(app):
    """
    Test whether the blueprints are registered correctly.

    Args:
        app: Flask application instance.

    Asserts:
        - Whether the "auth" blueprint is registered.
        - Whether the "posts" blueprint is registered.
        - Whether the "users" blueprint is registered.
        - Whether the "general" blueprint is registered.
    """
    with app.app_context():
        assert "auth" in app.blueprints
        assert "posts" in app.blueprints
        assert "users" in app.blueprints
        assert "general" in app.blueprints
