# api2.py
from flask import Blueprint, jsonify

api2 = Blueprint('api2', __name__)


@api2.route('/resource', methods=['GET'])
def get_resource2():
    data = {"message": "This is API 2 resource data."}
    return jsonify(data)
