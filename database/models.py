import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

from sqlalchemy.sql.sqltypes import DateTime

# database_name = "fit_tracker"
# database_path = "postgresql://{}/{}".format('localhost:5432', database_name)
database_path = "postgres://iocqyckhiidpmx:0c335fcf04d1356120385e698702a08147839f0d7041378240ad09147daa1a52@ec2-52-204-29-205.compute-1.amazonaws.com:5432/ddv8n1nupk8n5m"

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
User

'''
class User(db.Model):  
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    nick_name = Column(String)
    age = Column(Integer)
    bodys = db.relationship('Body_Measurement', backref='users', lazy=True)

    def __init__(self, full_name, age, nick_name):
        self.full_name = full_name
        self.age = age
        self.nick_name = nick_name

    def __repr__(self):
        return json.dumps(self.format())
        
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'full_name': self.full_name,
        'age': self.age,
        'nick_name': self.nick_name
        }

'''
Body_Measurement

'''
class Body_Measurement(db.Model):  
    __tablename__ = 'body_measurement'

    id = Column(Integer, primary_key=True)
    weight = Column(db.Float(), nullable=False, default=0)
    height = Column(db.Float(), nullable=False, default=0)
    user_id = Column(Integer, db.ForeignKey('user.id'))
    # user = db.relationship('User', backref=db.backref('body_measurement', lazy=True))

    def __init__(self, weight, height, user_id):
        self.weight = weight
        self.height = height
        self.user_id = user_id
    
    def __repr__(self):
        return json.dumps(self.format())
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())

    def get_all(self):
        return Body_Measurement.query.all()

    def get_by_id(self, id):
        return Body_Measurement.query.get(id)

    def format(self):
        return {
        'id': self.id,
        'type': self.type
        }