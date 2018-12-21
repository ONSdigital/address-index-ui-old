from flask import Blueprint, render_template, request, redirect, flash, current_app
from flask_login import login_required
from ai_ui.forms.postcode import PostcodeForm
from ai_ui.forms.address import AddressForm
from ai_ui.forms.uprn import UPRNForm
from ai_ui.utilities.classifications import get_class_list

import requests
import json
import math

search_bp = Blueprint('search_bp', __name__, static_folder='static', template_folder='templates')


@search_bp.context_processor
def utility_processor():
    return dict(round=round)


@search_bp.route("/addresses", methods=['GET', 'POST'])
@login_required
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


@search_bp.route("/postcode", methods=['GET', 'POST'])
@login_required
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


@search_bp.route("/uprn", methods=['GET', 'POST'])
@login_required
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


@search_bp.route('/addresses/<address>', methods=['GET', 'POST'])
@login_required
def address_results(address):

    form = AddressForm()
    page = int(request.args.get('page', 1))

    if form.validate_on_submit():

        address_query_params = "?classificationfilter=" + form.classificationFilter.data + \
                               "&historical=" + form.historical.data + "&verbose=true" + \
                               "&resultsperpage=" + str(form.resultsPerPage.data)

        return redirect('/addresses/' + form.address.data + address_query_params)

    classificationfilter = request.args.get('classificationfilter', None)
    max_page_results = int(request.args.get('resultsperpage', 10))
    offset = (page * max_page_results) - max_page_results

    uri = current_app.config['API_URL'] + "/addresses?input=" + address
    params = {'classificationfilter': classificationfilter, 'limit': max_page_results, 'offset': offset,
              'historical': request.args.get('historical', 'True'), 'verbose': 'true',
              'resultsperpage': request.args.get('resultsperpage', 10)}
    response = requests.get(uri, params=params)

    address_results_list = json.loads(response.text)

    if not(address_results_list['response']['total']) or address_results_list['response']['total'] == 0:
        max_page = 0
    else:
        max_page = int(math.ceil(address_results_list['response']['total'] / max_page_results))

    query_params = "&historical=" + request.args.get('historical', 'True') + "&verbose=true" \
                   + '&resultsperpage=' + str(request.args.get('resultsperpage', 10))
    if classificationfilter:
        query_params = query_params + "&classificationfilter=" + classificationfilter

    class_list = get_class_list()

    return render_template('addressresults.html', addressResults=address_results_list, classList=class_list, form=form,
                           page=page, maxPage=max_page, queryParams=query_params, searchterm=address)


@search_bp.route('/postcode/<postcode>', methods=['GET', 'POST'])
@login_required
def postcode_results(postcode):

    form = PostcodeForm()
    page = int(request.args.get('page', 1))

    if form.validate_on_submit():

        postcode_query_params = "?classificationfilter=" + form.classificationFilter.data + \
                                "&historical=" + form.historical.data + "&verbose=true" + \
                                "&resultsperpage=" + form.resultsPerPage.data

        return redirect('/postcode/' + form.postcode.data + postcode_query_params)

    classificationfilter = request.args.get('classificationfilter', None)
    max_page_results = int(request.args.get('resultsperpage', 10))
    offset = (page * max_page_results) - max_page_results

    uri = current_app.config['API_URL'] + "/addresses/postcode/" + postcode
    params = {'classificationfilter': classificationfilter, 'limit': max_page_results, 'offset': offset,
              'historical': request.args.get('historical', 'True'), 'verbose': 'true',
              'resultsperpage': request.args.get('resultsperpage', 10)}
    response = requests.get(uri, params=params)

    postcode_results_list = json.loads(response.text)

    if not(postcode_results_list['response']['total']) or postcode_results_list['response']['total'] == 0:
        max_page = 0
    else:
        max_page = int(math.ceil(postcode_results_list['response']['total'] / max_page_results))

    query_params = "&historical=" + request.args.get('historical', 'True') + "&verbose=true" + \
                   '&resultsperpage=' + request.args.get('resultsperpage', 10)
    if classificationfilter:
        query_params = query_params + "&classificationfilter=" + classificationfilter

    class_list = get_class_list()

    return render_template('postcoderesults.html', postcodeResults=postcode_results_list, classList=class_list,
                           form=form, page=page, maxPage=max_page, queryParams=query_params)


@search_bp.route('/result/<uprn>')
@login_required
def result(uprn):

    uri = current_app.config['API_URL'] + "/addresses/uprn/" + uprn
    params = {'verbose': 'true'}
    response = requests.get(uri, params=params)

    if response.status_code == 404:
        uprn_result = ""
    else:
        uprn_result = json.loads(response.text)

    class_list = get_class_list()

    return render_template('result.html', uprnResult=uprn_result, classList=class_list, uprn=uprn)
