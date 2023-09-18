from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User model"""
    __tablename__ = "Users"
   
    username = db.Column(db.String(20), nullable = False)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)


class Feedback(db.Model):
    """Feedback Model"""
    __tablename__ = "Feedback"

    id = db.Column(db.Integer, primary_key = True, unique=True, autoincrement = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.String(20), db.Foreign_key('username.id', ondelete = 'CASCADE', nullable = False))
    