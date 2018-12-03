import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

host = "http://addressindex-api-dev.apps.devtest.onsclofo.uk"