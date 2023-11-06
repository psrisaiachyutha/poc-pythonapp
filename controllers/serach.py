from flask import jsonify, Blueprint, request
from services.searchservice import search_brandname_handler

search = Blueprint('search', __name__)


@search.get('/brand')
def fetch_brand_info():
    brand_name = request.args.get('brandname')

    # validating the query params
    if brand_name is None:
        return {
            'code': 400,
            'message': 'brandname must be send to search'
        }

    brand_name = brand_name.strip()
    if len(brand_name) == 0:
        return {
            'code': 400,
            'message': 'brandname cannot be empty string'
        }

    result = search_brandname_handler(brand_name)
    return {
        'data': result,
        'code': 200
    }
