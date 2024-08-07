"""
Module for defining database models for the application.

This module contains the database models for representing users and posts in the application.

Classes:
    Users: Model for representing users in the database.
    Posts: Model for representing posts in the database.

Imports:
    - datetime: Module for working with dates and times.
    - timezone: Class representing a time zone.
    - UserMixin: Class providing default implementations for User class methods.
    - db: Database instance from SQLAlchemy.
    - bcrypt: Instance of Bcrypt for hashing passwords.
"""

from datetime import datetime, timezone
from flask_login import UserMixin
from .extensions import db, bcrypt


class Users(db.Model, UserMixin):
    """Model for representing users in the database."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    favorite_pizza_place = db.Column(db.String(200), default="You")
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    profile_pic = db.Column(db.String(), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    password_hash = db.Column(db.String(128))
    posts = db.relationship("Posts", backref="poster")

    @property
    def password(self):
        """Getter for the user's password."""
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """Setter for the user's password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Verify the user's password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Representation of the user object."""
        return f"<User {self.username}>"

    def update_profile(self, **kwargs):
        """Update user's profile information."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete_account(self):
        """Delete user's account."""
        db.session.delete(self)
        db.session.commit()


class Posts(db.Model):
    """Model for representing posts in the database."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    slug = db.Column(db.String(255))
    poster_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def get_formatted_date(self):
        """Get formatted date string of the post's creation."""
        return self.date_posted.strftime("%B %d, %Y")

    def __repr__(self):
        """Representation of the post object."""
        return f"<Post {self.title}>"

    def update_title(self, new_title):
        """Update the title of the post."""
        self.title = new_title

    def update_content(self, new_content):
        """Update the content of the post."""
        self.content = new_content

    def get_date_posted_formatted(self):
        """Get the formatted date the post was posted."""
        return self.date_posted.strftime("%Y-%m-%d %H:%M:%S")
