import os,random, string

class Config(object):
    # Set up the App SECRET_KEY
    SECRET_KEY  = os.getenv('SECRET_KEY')

    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))   

    SQLALCHEMY_TRACK_MODIFICATIONS = False
   

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEBUG_DATABASE_URI')

# Load all possible configurations
configurations = {
    'production': ProductionConfig,
    'development': DevelopmentConfig
}