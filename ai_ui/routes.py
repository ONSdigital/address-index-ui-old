from flask import render_template, redirect, request, flash
from ai_ui import app
from ai_ui.forms import PostcodeForm, AddressForm, UPRNForm, FilterForm
from config import api_url
import math

import requests

import json
import re


def get_class_subset(code=None):

    class_call = requests.get(api_url + "/classifications")
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





@app.route('/filters')
@app.route('/filters/<start_point>')
def filters(start_point=None):
    form = FilterForm()

    called_from = request.args.get('called_from')
    existing_filters = request.args.get('existing_filters')

    class_list = get_classification_list(start_point)

    return render_template('filters.html', class_list=class_list, form=form,
                           existing_filters=existing_filters, called_from=called_from)



