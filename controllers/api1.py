# api1.py
import datetime

import DateTime
from flask import jsonify, Blueprint, request
from marshmallow import ValidationError

from models.schemas.CreatePersonRequestSchema import CreatePersonRequestSchema
from services.api1service import create_person_handler

api1 = Blueprint('api1', __name__)


@api1.route('/resource/<r1>/a/<timeline>', methods=['GET'])
def get_resource1(r1: str, timeline: str):
    from datetime import datetime, timedelta
    accepted_timelines = ['last-one-year', 'last-two-year']
    if timeline not in accepted_timelines:
        return "timeline is not accepted", 400

    if timeline == 'last-one-year':
        min_required_date = datetime.now() - timedelta(365)
    else:
        min_required_date = datetime.now() - timedelta(365 * 2)
    #min_required_date =
    print('min required date', min_required_date)
    import csv
    from collections import defaultdict
    file_path = 'env/sample.csv'
    data = None
    with open(file_path, mode='r') as file:
        # reading the CSV file
        csv_file = csv.DictReader(file)
        filtered_data = defaultdict(dict)
        # displaying the contents of the CSV file
        for lines in csv_file:
            #print(lines)
            try:
                print(datetime.strptime(lines['Month'], "%d/%m/%Y"))
                if not lines['Month'].startswith('#') and datetime.strptime(lines['Month'], "%m/%d/%Y") >= min_required_date:
                    filtered_data[lines['brand']][lines['Month']] = lines['Spend']
            finally:
                pass
        data = filtered_data



    #data = {"message": "This is API 1 resource data." + r1 + "sample " + s1}
    #print(data)
    return jsonify(data)


@api1.post('/resource/person')
def create_resource():
    request_body_json = request.get_json()
    schema = CreatePersonRequestSchema()
    try:
        # Validate request body against schema data types
        result = schema.load(request_body_json)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400

    # result = create_person_handler(result)
    return {
        'data': result,
        'code': 203,
        'error': 'errrrrr'
    }
