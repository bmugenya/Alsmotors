from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


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
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)



class Car(db.Model, Updateable):

    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.VARCHAR)
    name = db.Column(db.String(64))
    type = db.Column(db.String(64))
    brand = db.Column(db.String(64))
    make = db.Column(db.String(64))
    price = db.Column(db.String(64))
    models = db.Column(db.String(64))
    location = db.Column(db.String(64))
    fuel = db.Column(db.String(64))
    transmission = db.Column(db.String(64))
    featured = db.Column(db.String(64))
    promotion = db.Column(db.String(64))
    used = db.Column(db.String(64))


    def select(self):
        return Car.select()

    def __repr__(self):
        return '<Car {}>'.format(self.name)



@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
