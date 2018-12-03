from flask import render_template, redirect, request, flash
from app import app
from app.forms import postcodeForm, addressForm
import math

import requests

import json

#host = "http://localhost:9000"
#host = "http://addressindex-api-branch.apps.devtest.onsclofo.uk"
host = "http://addressindex-api-dev.apps.devtest.onsclofo.uk"
maxPageResults = 1



def getClassList():
    classifications = requests.get(host + "/codelists/classification")
    return json.loads(classifications.text)

@app.context_processor
def utility_processor():
    return dict(round=round)


@app.route('/', methods=['GET', 'POST'])
@app.route("/postcode", methods=['GET', 'POST'])
def postcode():
    form = postcodeForm()

    if request.method == 'POST':
        if form.validate_on_submit() == False:
            flash('All fields are required.')
            return render_template('postcode.html', form = form)
        else:
            return redirect('/postcode/' + form.postcode.data )
    elif request.method == 'GET':
        return render_template('postcode.html', form = form)




@app.route('/postcode/<postcode>', methods=['GET', 'POST'])
def results(postcode):

    form = postcodeForm()
    page = int(request.args.get('page', 1))

    if form.validate_on_submit():

        postcodeQueryParams = "?classificationfilter=" + form.classificationFilter.data + "&historical=" + form.historical.data

        return redirect('/postcode/' + form.postcode.data + postcodeQueryParams )

    classificationfilter = request.args.get('classificationfilter', None)
    offset = (page * maxPageResults) - maxPageResults

    uri = host + "/addresses/postcode/" + postcode
    params = {'classificationfilter' : classificationfilter, 'limit' : maxPageResults, 'offset' : offset, 'historical' : request.args.get('historical', 'True')}
    response = requests.get(uri, params=params )

    postcodeResults = json.loads(response.text)

    maxPage = math.ceil(postcodeResults['response']['total'] / maxPageResults)
    # maxPage = 7

    queryParams = "&historical=" + request.args.get('historical', 'True')
    if classificationfilter :
        queryParams = queryParams + "&classificationfilter=" + classificationfilter

    classList = getClassList()

    return render_template('postcoderesults.html', postcodeResults = postcodeResults, classList = classList, form = form, page = page, maxPage = maxPage, queryParams = queryParams)


@app.route('/result/<uprn>')
def result(uprn):

    uri = host + "/addresses/uprn/" + uprn
    response = requests.get(uri)

    uprnResult = json.loads(response.text)

    classList = getClassList()

    return render_template('result.html', uprnResult = uprnResult, classList = classList)


@app.route('/help')
def help():
    return render_template('help.html')

@app.route("/addresses", methods=['GET', 'POST'])
def addresses():
    form = addressForm()
    if form.validate_on_submit():
        return redirect('/addresses/' + form.address.data )
    return render_template("addresses.html", form = form)


@app.route('/addresses/<address>', methods=['GET', 'POST'])
def addressResults(address):

    form = addressForm()
    if form.validate_on_submit():

        addressQueryParams = "?classificationfilter=" + form.classificationFilter.data + "&historical=" + form.historical.data

        return redirect('/addresses/' + form.address.data + addressQueryParams )

    classificationfilter = request.args.get('classificationfilter', None)
    offset = request.args.get('offset', 0)

    uri = host + "/addresses?input=" + address
    params = {'classificationfilter' : classificationfilter, 'limit' : maxPageResults, 'offset' : offset, 'historical' : request.args.get('historical', 'True')}
    response = requests.get(uri, params=params )

    addressResults = json.loads(response.text)

    classList = getClassList()

    return render_template('addressresults.html', addressResults = addressResults, classList = classList, form = form, searchterm = address)


@app.route("/bulk", methods=['GET', 'POST'])
def bulk():
    form = postcodeForm()
    if form.validate_on_submit():
        return redirect('/bulk/' + form.postcode.data )
    return render_template("postcode.html", form = form)