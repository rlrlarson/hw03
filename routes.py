#import libraries
from flask import Flask, flash, render_template, request, url_for, redirect, jsonify, session
from models import db, User, Post, Follows
from forms import SignupForm, LoginForm, NewpostForm #, SearchForm
from passlib.hash import sha256_crypt
from flask_heroku import Heroku

#to deploy on heroku
#app = Flask(__name__)
#heroku = Heroku(app)

# to use locally
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rebeccalarson@localhost:5432/hw3_db' 

db.init_app(app)
app.secret_key = "cscie14a-hw3"


def add_username(followed_posts):
	edited_posts = []
	for p in followed_posts:
		edited_posts.append([p] + [User.query.filter_by(uid=p.author).first().username])
	return edited_posts

#routes
@app.route('/')
@app.route('/index')
def index():

	if 'username' in session:
		session_user = User.query.filter_by(username=session['username']).first()

		users_followed = Follows.query.filter_by(follower=session_user.uid).all()
		uids_followed = [f.following for f in users_followed] + [session_user.uid]
		followed_posts = Post.query.filter(Post.author.in_(uids_followed)).all()

		# added to display posts in time order
		followed_posts.reverse()

		followed_posts_with_username = add_username(followed_posts)

		return render_template('index.html', title='Home', posts=followed_posts_with_username, session_username=session_user.username)
	else:
		all_posts = Post.query.all()

		# added to display posts in time order
		all_posts.reverse()

		all_posts_with_username = add_username(all_posts)
		return render_template('index.html', title='Home', posts=all_posts_with_username)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		user = User.query.filter_by(username=username).first()

		if user is None or not sha256_crypt.verify(password, user.password):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		else:
			session['username'] = username
			return redirect(url_for('index'))
	else:
		return render_template('login.html', title='Login', form=form)

@app.route('/logout', methods=['POST'])
def logout():
	session.clear()
	return redirect(url_for('index'))

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
	form = NewpostForm()
	if request.method == 'POST':
		session_user = User.query.filter_by(username=session['username']).first()
		content = request.form['content']
		new_post = Post(author=session_user.uid, content=content)
		db.session.add(new_post)
		db.session.commit()
		return redirect(url_for('index'))
	else:
		return render_template('newpost.html', title='Newpost', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		existing_user = User.query.filter_by(username=username).first()
		if existing_user:
			flash('The username already exists. Please pick another one.')
			return redirect(url_for('signup'))
		else:
			user = User(username=username, password=sha256_crypt.hash(password))
			db.session.add(user)
			db.session.commit()
			flash('Congratulations, you are now a registered user!')
			return redirect(url_for('login'))
	else:
		return render_template('signup.html', title='Signup', form=form)


@app.route('/profile/<username>', methods=['GET'])
def profile(username):
	profile_user = User.query.filter_by(username=username).first()

	if profile_user:
		profile_user_posts = Post.query.filter_by(author=profile_user.uid).all()

		# added to display posts in time order
		profile_user_posts.reverse()

		profile_user_posts_with_username = add_username(profile_user_posts)

		if "username" in session:
			session_user = User.query.filter_by(username=session['username']).first()

			if profile_user == session_user:
				return render_template('profile.html', user=profile_user, posts=profile_user_posts_with_username, session_username=session_user.username)

			if Follows.query.filter_by(follower=session_user.uid, following=profile_user.uid).first():
				followed = True
			else:
				followed = False

			return render_template('profile.html', user=profile_user, posts=profile_user_posts_with_username, followed=followed)

		else:
			return render_template('profile.html', user=profile_user, posts=profile_user_posts_with_username)

	else:
		flash('That user does not exist.')
		return redirect(url_for('index'))


@app.route('/search', methods=['POST'])
def search():
	user_to_query = request.form['search_box']
	return redirect(url_for('profile', username=user_to_query))


@app.route('/follow/<username>', methods=['POST'])
def follow(username):
	session_user = User.query.filter_by(username=session['username']).first()
	user_to_follow = User.query.filter_by(username=username).first()
	new_follow = Follows(follower=session_user.uid, following=user_to_follow.uid)

	# if user is None:
	# 	flash('User {} not found.'.format(username))
	# 	return redirect(url_for('index'))

 	# if user_to_follow == session_user:
	 # 	flash('You cannot follow yourself!')
  #    	return redirect(url_for('profile', username=username))

	db.session.add(new_follow)
	db.session.commit()
	#flash('You are following {}!'.format(username))
	return redirect(url_for('profile', username=username))


@app.route('/unfollow/<username>', methods=['POST'])
def unfollow(username):
	session_user = User.query.filter_by(username=session['username']).first()
	user_to_unfollow = User.query.filter_by(username=username).first()
	delete_follow = Follows.query.filter_by(follower=session_user.uid, following=user_to_unfollow.uid).first()

    # if user is None:
    #     flash('User {} not found.'.format(username))
    #     return redirect(url_for('index'))

	# if user_to_unfollow == session_user:
	# 	flash('You cannot unfollow yourself!')
	# 	return redirect(url_for('profile', username=username))

	db.session.delete(delete_follow)
	db.session.commit()
	#flash('You are not following {}.'.format(username))
	return redirect(url_for('profile', username=username))

if __name__ == "__main__":
    app.run(debug=True)
