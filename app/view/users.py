from flask import Blueprint
from app.model.data_model import Users
from app import db

users = Blueprint('users', __name__)

@users.route('/users', methods=['GET'])
def add_user():
    """Register a new user"""

    return 'add user'



   

