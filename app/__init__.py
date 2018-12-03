from flask import Flask, Blueprint

from config import Config
from developers import developers


app = Flask(__name__)

app.config.from_object(Config)
app.register_blueprint(developers, url_prefix='/developers')



from app import routes


from app import developers