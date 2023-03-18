from app import db, login_manager
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from hashlib import md5



class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class User(db.Model, UserMixin,Updateable):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def avatar_url(self):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon'

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None


class Car(db.Model, Updateable):

    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.VARCHAR)
    name = db.Column(db.String(64))
    year = db.Column(db.DateTime, default=datetime.utcnow)
    engine = db.Column(db.String(64))
    drive_type = db.Column(db.String(64))
    brand = db.Column(db.String(64))
    category = db.Column(db.String(64))
    model = db.Column(db.String(64))
    location = db.Column(db.String(64))
    fuel_type = db.Column(db.String(64))
    transmission = db.Column(db.String(64))
    promotion = db.Column(db.Boolean, default=False)
    used = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Car {}>'.format(self.name)

    @property
    def url(self):
        return url_for('cars.get', id=self.id)

class Image(db.Model, Updateable):
    
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    images = db.Column(db.VARCHAR)
    body_type = db.Column(db.String(64))
    description = db.Column(db.VARCHAR)
    cars_id = db.Column(db.Integer, db.ForeignKey('cars.id'))

    def __repr__(self):
        return '<Image {}>'.format(self.body_type)

    @property
    def url(self):
        return url_for('images.get', id=self.id)


class Notification(db.Model):
    
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    mobile = db.Column(db.String(120))
    email = db.Column(db.String(120))
    message =  db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    cars_id = db.Column(db.Integer, db.ForeignKey('cars.id'))

    @property
    def avatar_url(self):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon'

    def __repr__(self):
        return '<Notification {}>'.format(self.message)


class Contact(db.Model):
    
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    mobile = db.Column(db.String(120))
    email = db.Column(db.String(64))
    message =  db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
   
    def __repr__(self):
        return '<Contact {}>'.format(self.message)

class Subscribe(db.Model):
    
    __tablename__ = 'subscribers'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def avatar_url(self):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon'
   
    def __repr__(self):
        return '<Subscribe {}>'.format(self.email)

