from datetime import datetime, timedelta

from flask import jsonify, Blueprint, request, abort

from models.response.BaseResponse import BaseResponse
from models.schemas.competitoranalysis import CompetitorAnalysisParams
from services.reportservice import get_competitoranalysis_handler

report = Blueprint('report', __name__)


def parse_list_params(param: str, param_name: str):
    if param is None:
        abort(400, description="{param_name} cannot be null".format(param_name=param_name))
    param = param.strip()
    if len(param) == 0:
        abort(400, description="{param_name} cannot be empty".format(param_name=param_name))

    return param.split(',')


@report.route('/competitoranalysis/<company>/timeline/<timelineidentifier>', methods=['GET'])
def competitoranalysis(company: str, timelineidentifier: str):
    duration = request.args.get('duration')
    location = request.args.get('location')
    demographics = request.args.get('demographics')
    competitors = request.args.get('competitors')

    # TODO validations for query params
    if duration is None or len(duration.strip()) == 0:
        return "duration cannot be null or empty", 400

    # if location is None:
    #     return "location cannot be null", 400
    # if len(location.strip()) == 0:
    #     return "location cannot be empty string", 400
    #
    # if demographics is None:
    #     return "demographics cannot be null", 400
    # if len(demographics.strip()) == 0:
    #     return "demographics cannot be empty string", 400
    #
    # if competitors is None:
    #     return "competitors cannot be null", 400
    # if len(competitors.strip()) == 0:
    #     return "competitors cannot be empty string", 400

    # location = location.split(',')
    # demographics = demographics.split(',')
    # competitors = competitors.split(',')
    # print(location)
    location = parse_list_params(location, 'location')
    demographics = parse_list_params(demographics, 'demographics')
    competitors = parse_list_params(competitors, 'competitors')

    accepted_timelines = ['customer_volume', 'expenditure', 'transaction']
    if timelineidentifier not in accepted_timelines:
        return "timeline is not accepted", 400

    accepted_durations = ['last-one-year', 'last-two-year']
    if duration not in accepted_durations:
        return "duration is not valid", 400

    if duration == 'last-one-year':
        min_required_date = datetime.now() - timedelta(365)
    else:
        min_required_date = datetime.now() - timedelta(365 * 2)

    # required_column = ''
    # if timelineidentifier == 'expenditure':
    #     required_column = 'Spend'
    # elif timelineidentifier == 'transaction':
    #     required_column = 'Transactions'
    # elif timelineidentifier == 'customer_volume':
    #     required_column = 'Shoppers'

    # import csv
    # from collections import defaultdict
    # file_path = 'env/sample.csv'
    # data = None
    # with open(file_path, mode='r') as file:
    #     # reading the CSV file
    #     csv_file = csv.DictReader(file)
    #     filtered_data = defaultdict(dict)
    #     # displaying the contents of the CSV file
    #     for lines in csv_file:
    #         # print(lines)
    #         try:
    #             # print(datetime.strptime(lines['Month'], "%d/%m/%Y"))
    #             month = datetime.strptime(lines['Month'], "%m/%d/%Y")
    #             if not lines['Month'].startswith('#') and month >= min_required_date:
    #                 filtered_data[lines['brand']][datetime_to_month_and_year(month)] = lines[required_column]
    #         finally:
    #             pass
    #     companies = []
    #     for key, value in filtered_data.items():
    #         company = {
    #             'name': key,
    #             'data': value
    #         }
    #         companies.append(company)
    #
    #     data = {
    #         'companies': companies
    #     }
    #     result = BaseResponse(data=data, code=200)
    params = CompetitorAnalysisParams(
        # duration=duration,
        location=location,
        demographics=demographics,
        competitors=competitors,
        timelineidentifier=timelineidentifier,
        min_required_date=min_required_date
    )
    data = get_competitoranalysis_handler(params)
    result = BaseResponse(data=data, code=200)
    return jsonify(result)
