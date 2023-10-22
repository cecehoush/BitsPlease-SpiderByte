from datetime import datetime
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    password = db.Column(db.LargeBinary, nullable=False)
    userChallenge = db.relationship('UserChallenge', backref='user_ref', lazy=True)
    favorites = db.relationship('Challenge', secondary='favorite_challenges', backref=db.backref('favorited_by', lazy=True))
    user_type = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'user',  # Discriminator value for User instances
        'polymorphic_on': user_type  # Specifying which column to use for discrimination
    }

class Admin(User):
    __tablename__ = 'admins'
    __mapper_args__ = {
        'polymorphic_identity': 'admin',  # Discriminator value for Admin instances
    }

class Professor(User):
    __tablename__ = 'professors'
    __mapper_args__ = {
        'polymorphic_identity': 'professor'  
    }

class UserChallenge(db.Model):
    __tablename__ = 'user_challenges'
    challengeid = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)

class Course(db.Model):
    __tablename__= 'courses'
    courseid = db.Column(db.String, primary_key=True)
    description = db.Column(db.String)

class Challenge(db.Model):
    __tablename__ = 'challenges'
    challengeid = db.Column(db.String, primary_key=True)
    courseid = db.Column(db.String)
    description = db.Column(db.String)
    difficulty = db.Column(db.String)
    test_cases = db.relationship('TestCase', backref='challenge', cascade='all,delete')

class TestCase(db.Model):
    __tablename__ = 'test_cases'
    id = db.Column(db.Integer, primary_key=True)
    challengeid = db.Column(db.String, db.ForeignKey('challenges.challengeid'), nullable=False)
    test_function = db.Column(db.String, nullable=False)
    input = db.Column(db.String, nullable=False)
    required_output = db.Column(db.String, nullable=False)

class FavoriteChallenge(db.Model):
    __tablename__ = 'favorite_challenges'
    user_id = db.Column(db.String, db.ForeignKey('users.id'), primary_key=True)
    challenge_id = db.Column(db.String, db.ForeignKey('challenges.challengeid'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


#   user_type = db.Column(db.String)

