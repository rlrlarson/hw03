# create models
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Follows(db.Model):
	__tablename__ = 'follows'
	fid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	follower = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
	following = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)

class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(64), unique=True, nullable=False)
	password = db.Column(db.String(128), nullable=False)

class Post(db.Model):
	__tablename__ = 'posts'
	pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	author = db.Column(db.Integer, db.ForeignKey('users.uid') , nullable=False)
	content = db.Column(db.String(1024), nullable=False)
