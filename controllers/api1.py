# api1.py
from flask import jsonify, Blueprint, request
from marshmallow import ValidationError

from models.schemas.CreatePersonRequestSchema import CreatePersonRequestSchema
from services.api1service import create_person_handler

api1 = Blueprint('api1', __name__)


@api1.route('/resource', methods=['GET'])
def get_resource1():
    data = {"message": "This is API 1 resource data."}
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
