from datetime import datetime
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    password = db.Column(db.LargeBinary, nullable=False)
    userChallenge = db.relationship('UserChallenge', backref='user_ref', lazy=True)
    favorites = db.relationship('Challenge', secondary='favorite_challenges', backref=db.backref('favorited_by', lazy=True))


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
# answers = db.Column(db.String)  #make multiple answers possible 

class FavoriteChallenge(db.Model):
    __tablename__ = 'favorite_challenges'
    user_id = db.Column(db.String, db.ForeignKey('users.id'), primary_key=True)
    challenge_id = db.Column(db.String, db.ForeignKey('challenges.challengeid'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


#   user_type = db.Column(db.String)

# class Reseller(User):
#     __tablename__ = 'resellers'
#     company = db.Column(db.String)
#     address = db.Column(db.String)
#     phone = db.Column(db.String)
#     website = db.Column(db.String)
#     __mapper_args__ = {
#         'polymorphic_identity': 'reseller'  # Discriminator value for Admin instances
#     }
# class Admin(User):
#     __tablename__ = 'admins'
#     name = db.Column(db.String)
#     title = db.Column(db.String)
#     __mapper_args__ = {
#         'polymorphic_identity': 'admin'  # Discriminator value for Admin instances
#     }
