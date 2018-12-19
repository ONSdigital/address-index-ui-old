from flask import Flask, Blueprint

from config import Config


app = Flask(__name__)

app.config.from_object(Config)


from ai_ui import routes