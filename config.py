import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ENVIRONMENT = os.getenv('ENVIRONMENT')


host = os.getenv('HOST')
port = os.getenv('PORT')
api_url = os.getenv('API_URL')


