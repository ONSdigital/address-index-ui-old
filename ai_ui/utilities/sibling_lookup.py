from flask import current_app
import requests
import json


def get_siblings(relatives):

    sibling_list = []

    for level in relatives:
        for sibling in level['siblings']:
            sibling_request = requests.get(current_app.config['API_URL'] + "/addresses/uprn/" + str(sibling))
            sibling_result = json.loads(sibling_request.text)

            sibling_uprn = sibling
            sibling_address = sibling_result['response']['address']['formattedAddressNag']

            sibling_list.append({"uprn": sibling_uprn,
                                "address": sibling_address})

    return sibling_list
