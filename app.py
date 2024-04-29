from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_ex"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "Oh no dont let anyone find it"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

toolbar = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)

@app.route('/')
def not_this_one():
    """redirects to /register for homepage"""
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Home page for users to sign up"""

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        hashed_pwd = User.register(username, password)
        new_user = User(username=hashed_pwd.username, 
                        password=hashed_pwd.password, 
                        email=email, 
                        first_name=first_name, 
                        last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        return redirect(f'/users/{new_user.username}')
    
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login_user():
    """Page for the user to login to their account"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f'We missed you {user.username}, Please never leave me again...', 'success')
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid username or password, try again loser"]
    
    return render_template('login.html', form=form)

@app.route('/users/<username>')
def user_info(username):
    """user page that needs to have a user 
    loged in to be able to view"""

    if 'username' not in session:
        flash("Please log in or create an account", "danger")
        return redirect('/')
    else:
        user = User.query.get_or_404(username)
        form = FeedbackForm()
        return render_template('userInfo.html', user=user, form=form)
    
@app.route('/logout')
def logout_user():
    """logout the user"""
    session.pop('username')
    flash('Goodbye, come again', 'info')
    return redirect('/')

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Delete a user"""

    if "username" not in session or username != session['username']:
        flash("Please log in or create an account", "danger")
        return redirect('/')
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/")

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    """place for users to add feedback"""
    if "username" not in session or username != session['username']:
        flash("Please log in or create an account", "danger")
        return redirect('/')
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{feedback.username}')
    else:
        return render_template()

@app.route('/users/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    """place for the user to update feedback"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        flash("Please log in or create an account", "danger")
        return redirect('/')
    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    return render_template("edit.html", form=form, feedback=feedback)
    
@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    """place for users to delete their feedback"""

    feedback = Feedback.query.get(feedback_id)
    temp = feedback.username
    
    if "username" not in session or feedback.username != session['username']:
        flash("Please log in or create an account", "danger")
        return redirect('/')

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f'/users/{temp}')
