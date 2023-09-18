from collections import UserDict, UserString
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, url_for, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf.csrf import CSRFProtect
from models import Feedback, User, db, connect_db, Users
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
csrf = CSRFProtect(app)

# Initialize SQLAlchemy with your app
db.init_app(app)


# Initialize DebugToolbarExtension
toolbar = DebugToolbarExtension(app)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

    app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

csrf = CSRFProtect(app)
debug = DebugToolbarExtension(app)


@app.route("/")
def register():
    """Redirect to /register"""
    return redirect(url_for('register'))

@app.route('/register', methods = ['GET', "POST"])
def new_user():
    form = RegistrationForm()
    
    if form. validate_on_submit():
        """Show form submitted will register/create a user, prcess the registration form by adding new user"""
       
        username = form.username.data,
        password =  form.password.data,
        email =  form.email.data,
        first_name = form.first_name.data,
        last_name = form.last_name.data
        

        flash('Registeration sucessful')
        return redirect(url_for('secret'))
    return render_template('register.html', form = form)

@app.route('/login', methods = ['GET', ['POST']])
def login():
    """Show form that when submitted will login a user"""
    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        if username == 'admin' and password == 'password':
            flash('Login sucess!', 'sucess')
            return redirect(url_for('secret'))
        
        else:
            flash('Login failed. Recheck credentials','danger')

    return render_template('login.html', form = form)

@app.route('/users/<int:username>', methods = ['GET'])
def use_profile(username):
    if 'username' not in session or session['username'] !=username:
        flash ('This is a secret page. Only authenticated users can access','danger')
    return redirect(url_for('index'))

    user = User.query.filter_by(username=username).first()
    feedback = Feedback.query.filter_by(user_id=user.id).all()
    return render_template('user_profile.html', user=user, feedback=feedback)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    # Ensure that only the logged-in user can delete their account
    if 'username' not in session or session['username'] != username:
        flash('You do not have permission to delete this account.', 'danger')
        return redirect(url_for('index'))

    # Fetch the user and their feedback from the database
    user = User.query.filter_by(username=username).first()

    if user:
        # Delete the user and their feedback
        db.session.delete(user)
        db.session.commit()

        # Clear user information from the session
        session.pop('username', None)

        flash('Account deleted successfully.', 'success')
    else:
        flash('User not found.', 'danger')

    return redirect(url_for('index'))

    
@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    # Ensure that only the logged-in user can delete their account
    if 'username' not in session or session['username'] != username:
        flash('You do not have permission to delete this account.', 'danger')
        return redirect(url_for('index'))

    # Fetch the user and their feedback from the database
    user = User.query.filter_by(username=username).first()

    if user:
        # Delete the user and their feedback
        db.session.delete(user)
        db.session.commit()

        # Clear user information from the session
        session.pop('username', None)

        flash('Account deleted successfully.', 'success')
    else:
        flash('User not found.', 'danger')

    return redirect(url_for('index'))

@app.route('/users/<username>/feedback/add', methods=['POST'])
def add_feedback(username):
    # Ensure that only the logged-in user can add feedback
    if 'username' not in session or session['username'] != username:
        flash('You do not have permission to add feedback.', 'danger')
        return redirect(url_for('index'))

    # Retrieve the feedback data from the form
    text = request.form.get('text')

    # Create a new feedback instance and add it to the user
    user = User.query.filter_by(username=username).first()

    if user:
        feedback = Feedback(text=text, user_id=user.id)
        db.session.add(feedback)
        db.session.commit()
        flash('Feedback added successfully.', 'success')
    else:
        flash('User not found.', 'danger')

    return redirect(url_for('user_profile', username=username))

@app.route('/feedback/<int:feedback_id>/update', methods=['GET'])
def edit_feedback_form(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    # Ensure that only the user who wrote the feedback can edit it
    if 'username' not in session or session['username'] != feedback.user.username:
        flash('You do not have permission to edit this feedback.', 'danger')
        return redirect(url_for('index'))

    return render_template('edit_feedback.html', feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    # Ensure that only the user who wrote the feedback can delete it
    if 'username' not in session or session['username'] != feedback.user.username:
        flash('You do not have permission to delete this feedback.', 'danger')
        return redirect(url_for('index'))

    # Delete the feedback and commit changes to the database
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback deleted successfully.', 'success')

    return redirect(url_for('user_profile', username=feedback.user.username))



@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('YOu are now logged out', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug= True)