from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv('.env')

class Config:

    SECRET_KEY = os.getenv('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_POOL_RECYCLE = 280
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 10}


