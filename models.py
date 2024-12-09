from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    avatar = db.Column(db.String(500), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='posts', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @property
    def likes_count(self):
        """Calculate the number of likes for the post"""
        return PostLike.query.filter_by(post_id=self.id).count()

    @property
    def favorites_count(self):
        """Calculate the number of favorites for the post"""
        return PostFavor.query.filter_by(post_id=self.id).count()

    @property
    def comments_count(self):
        """Calculate the number of comments"""
        return self.comments.count()

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='comments')

class PostLike(db.Model):
    __tablename__ = 'posts_like'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('posts.id'), nullable=False)

class PostFavor(db.Model):
    __tablename__ = 'posts_favor'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('posts.id'), nullable=False)
