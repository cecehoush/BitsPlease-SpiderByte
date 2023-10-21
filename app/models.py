from datetime import datetime
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    password = db.Column(db.LargeBinary, nullable=False)
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
