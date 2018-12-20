from flask import current_app
import requests
import json


def get_class_list():
    classifications = requests.get(current_app.config['API_URL'] + "/classifications")
    return json.loads(classifications.text)
