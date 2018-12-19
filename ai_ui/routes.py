from flask import render_template, redirect, request, flash
from ai_ui import app
from ai_ui.forms import PostcodeForm, AddressForm, UPRNForm, FilterForm
from config import api_url
import math

import requests

import json
import re


def get_class_list():
    classifications = requests.get(api_url + "/classifications")
    return json.loads(classifications.text)


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


@app.context_processor
def utility_processor():
    return dict(round=round)


@app.route('/', methods=['GET', 'POST'])
@app.route("/addresses", methods=['GET', 'POST'])
def address_search():
    form = AddressForm()

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('All fields are required.')
            return render_template('addresses.html', form=form)
        else:
            return redirect('/addresses/' + form.address.data)
    elif request.method == 'GET':
        return render_template('addresses.html', form=form)


@app.route("/postcode", methods=['GET', 'POST'])
def postcode_search():
    form = PostcodeForm()

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('All fields are required.')
            return render_template('postcode.html', form=form)
        else:
            return redirect('/postcode/' + form.postcode.data)
    elif request.method == 'GET':
        return render_template('postcode.html', form=form)


@app.route('/postcode/<postcode>', methods=['GET', 'POST'])
def postcode_results(postcode):

    form = PostcodeForm()
    page = int(request.args.get('page', 1))

    if form.validate_on_submit():

        postcode_query_params = "?classificationfilter=" + form.classificationFilter.data + \
                                "&historical=" + form.historical.data + "&verbose=true" + \
                                "&resultsperpage=" + form.resultsPerPage.data

        return redirect('/postcode/' + form.postcode.data + postcode_query_params)

    classificationfilter = request.args.get('classificationfilter', None)
    max_page_results = int(request.args.get('resultsperpage', '10'))
    offset = (page * max_page_results) - max_page_results

    uri = api_url + "/addresses/postcode/" + postcode
    params = {'classificationfilter': classificationfilter, 'limit': max_page_results, 'offset': offset,
              'historical': request.args.get('historical', 'True'), 'verbose': 'true',
              'resultsperpage': request.args.get('resultsperpage', '10')}
    response = requests.get(uri, params=params)

    postcode_results_list = json.loads(response.text)

    if not(postcode_results_list['response']['total']) or postcode_results_list['response']['total'] == 0:
        max_page = 0
    else:
        max_page = int(math.ceil(postcode_results_list['response']['total'] / max_page_results)) + 1

    query_params = "&historical=" + request.args.get('historical', 'True') + "&verbose=true" + \
                   '&resultsperpage=' + request.args.get('resultsperpage', '10')
    if classificationfilter:
        query_params = query_params + "&classificationfilter=" + classificationfilter

    class_list = get_class_list()

    return render_template('postcoderesults.html', postcodeResults=postcode_results_list, classList=class_list,
                           form=form, page=page, maxPage=max_page, queryParams=query_params)


@app.route("/uprn", methods=['GET', 'POST'])
def uprn_search():
    form = UPRNForm()

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('All fields are required.')
            return render_template('uprn.html', form=form)
        else:
            return redirect('/result/' + form.uprn.data)
    elif request.method == 'GET':
        return render_template('uprn.html', form=form)


@app.route('/result/<uprn>')
def result(uprn):

    uri = api_url + "/addresses/uprn/" + uprn
    params = {'verbose': 'true'}
    response = requests.get(uri, params=params)

    if response.status_code == 404:
        uprn_result = ""
    else:
        uprn_result = json.loads(response.text)

    class_list = get_class_list()

    return render_template('result.html', uprnResult=uprn_result, classList=class_list, uprn=uprn)


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/filters')
@app.route('/filters/<start_point>')
def filters(start_point=None):
    form = FilterForm()

    called_from = request.args.get('called_from')
    existing_filters = request.args.get('existing_filters')

    class_list = get_classification_list(start_point)

    return render_template('filters.html', class_list=class_list, form=form,
                           existing_filters=existing_filters, called_from=called_from)


@app.route('/addresses/<address>', methods=['GET', 'POST'])
def address_results(address):

    form = AddressForm()
    page = int(request.args.get('page', 1))

    if form.validate_on_submit():

        address_query_params = "?classificationfilter=" + form.classificationFilter.data + \
                             "&historical=" + form.historical.data + "&verbose=true" + \
                             "&resultsperpage=" + form.resultsPerPage.data

        return redirect('/addresses/' + form.address.data + address_query_params)

    classificationfilter = request.args.get('classificationfilter', None)
    max_page_results = int(request.args.get('resultsperpage', '10'))
    offset = (page * max_page_results) - max_page_results

    uri = api_url + "/addresses?input=" + address
    params = {'classificationfilter': classificationfilter, 'limit': max_page_results, 'offset': offset,
              'historical': request.args.get('historical', 'True'), 'verbose': 'true',
              'resultsperpage': request.args.get('resultsperpage', '10')}
    response = requests.get(uri, params=params)

    address_results_list = json.loads(response.text)

    if not(address_results_list['response']['total']) or address_results_list['response']['total'] == 0:
        max_page = 0
    else:
        max_page = int(math.ceil(address_results_list['response']['total'] / max_page_results)) + 1

    query_params = "&historical=" + request.args.get('historical', 'True') + "&verbose=true"\
                   + '&resultsperpage=' + request.args.get('resultsperpage', '10')
    if classificationfilter:
        query_params = query_params + "&classificationfilter=" + classificationfilter

    class_list = get_class_list()

    return render_template('addressresults.html', addressResults=address_results_list, classList=class_list, form=form,
                           page=page, maxPage=max_page, queryParams=query_params, searchterm=address)
