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

	# def follow(self, user):
	# 	if not self.is_following(user):
	# 		self.followed.append(user)

	# def unfollow(self, user):
	# 	if self.is_following(user):
	# 		self.followed.remove(user)

	# def is_following(self, user):
	# 	return self.followed.filter(follows.c.following == user.uid).count() == 1

	# def followed_posts(self):
	# 	followed_posts = Post.query.join(
	# 		follows, (follows.c.following == Post.author)).filter(
	# 			follows.c.follower == self.uid)
	# 	own = Post.query.filter_by(author=self.uid)
	# 	return followed_posts.union(own).order_by(Post.timestamp.desc())


class Post(db.Model):
	__tablename__ = 'posts'
	pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
	author = db.Column(db.Integer, db.ForeignKey('users.uid') , nullable=False)
	content = db.Column(db.String(1024), nullable=False)
