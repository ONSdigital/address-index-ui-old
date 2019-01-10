from flask import current_app
import requests
import json
import re


def get_class_list():
    classifications = requests.get(current_app.config['API_URL'] + "/classifications")
    return json.loads(classifications.text)


def get_class_subset(code=None):

    class_call = requests.get(current_app.config['API_URL'] + "/classifications")
    class_list = json.loads(class_call.text)

    subset_list = []

    if code:

        if len(code) == 1:
            for classification in class_list['classifications']:
                if re.match(r'^(%s)[A-Z]$' % code, classification['code']):
                    subset_list.append({"code": classification['code'].encode("utf-8"),
                                        "label": classification['label'].encode("utf-8")})
        elif len(code) == 2:
            for classification in class_list['classifications']:
                if re.match(r'^(%s)[0-9]{2}$' % code, classification['code']):
                    subset_list.append({"code": classification['code'].encode("utf-8"),
                                        "label": classification['label'].encode("utf-8")})
        elif len(code) == 4:
            for classification in class_list['classifications']:
                if re.match(r'^(%s)[A-Z]{2}$' % code, classification['code']):
                    subset_list.append({"code": classification['code'].encode("utf-8"),
                                        "label": classification['label'].encode("utf-8")})
    else:
        for classification in class_list['classifications']:
            if re.match(r'^[A-Z]$', classification['code']):
                subset_list.append({"code": classification['code'].encode("utf-8"),
                                    "label": classification['label'].encode("utf-8")})

    return subset_list


def get_child_count(code):

    count = len(get_class_subset(code))

    return count


def get_classification_list(code=None):

    class_list = []

    for classification in get_class_subset(code):
        class_list.append({"code": classification['code'], "label": classification['label'],
                           "child_count": get_child_count(classification['code'])})

    return class_list
