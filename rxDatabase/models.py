from . import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)                                                     
    email = db.Column(db.String(150), unique = True)                                     
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    records = db.relationship('Record')  

class Record(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    prescription_number=db.Column(db.String(150), unique=True)
    patient_name=db.Column(db.String(150))
    date_of_birth=db.Column(db.String(150))
    address=db.Column(db.String(150))
    date_prescribed=db.Column(db.String(150))
    drug_name=db.Column(db.String(150))
    city=db.Column(db.String)
    state=db.Column(db.String)
    zipcode=db.Column(db.Integer)