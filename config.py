'''Flask configuration'''
from os import environ, path, urandom

#from dotenv import load_dotenv
#basedir = path.abspath(path.dirname(__file__))
#load_dotenv(path.join(basedir, '.env'))

class Config:
    '''Base config'''
    # Flask-WTF requires an enryption key - the string can be anything
    SECRET_KEY = urandom(32) #environ.get('SECRET_KEY')
    #SERVER_NAME = 'local.docker:5000'
    JSONIFY_PRETTYPRINT_REGULAR = True
    
class ProdConfig(Config):
    '''Production config'''
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    

class DevConfig(Config):
    '''Development config'''
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True