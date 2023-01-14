import os

class Config:
    # database options
    DATABASE_URL = os.environ.get('DATABASE_URI') 
    # security options
    SECRET_KEY = os.environ.get('SECRET_KEY', 'top-secret!')


