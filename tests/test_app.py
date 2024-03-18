def test_create_app(app):
    assert app.testing
    assert app.config['TESTING']  # Ensure that TESTING config is True

def test_blueprints_registered(app):
    with app.app_context():
        assert 'auth' in app.blueprints
        assert 'posts' in app.blueprints
        assert 'users' in app.blueprints
        assert 'general' in app.blueprints