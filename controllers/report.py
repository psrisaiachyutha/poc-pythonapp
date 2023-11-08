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

    location = parse_list_params(location, 'location')
    demographics = parse_list_params(demographics, 'demographics')
    competitors = parse_list_params(competitors, 'competitors')

    accepted_timelines = ['customer_volume', 'expenditure', 'transaction']
    if timelineidentifier not in accepted_timelines:
        abort(400, description="timeline is not accepted")

    accepted_durations = ['last-one-year', 'last-two-year']
    if duration not in accepted_durations:
        return "duration is not valid", 400

    if duration == 'last-one-year':
        min_required_date = datetime.now() - timedelta(365)
    else:
        min_required_date = datetime.now() - timedelta(365 * 2)

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


@report.route('/competitoranalysis/<company>/aggregate/<aggregateidentifier>', methods=['GET'])
def share_of_wallet(company: str, aggregateidentifier: str):
    duration = request.args.get('duration')
    location = request.args.get('location')
    demographics = request.args.get('demographics')
    competitors = request.args.get('competitors')

    # TODO validations for query params
    if duration is None or len(duration.strip()) == 0:
        return "duration cannot be null or empty", 400

    location = parse_list_params(location, 'location')
    demographics = parse_list_params(demographics, 'demographics')
    competitors = parse_list_params(competitors, 'competitors')

    accepted_timelines = ['cross_visit', 'expenditure', 'wallet_share']
    if aggregateidentifier not in accepted_timelines:
        return "timeline is not accepted", 400

    accepted_durations = ['last-one-year', 'last-two-year']
    if duration not in accepted_durations:
        return "duration is not valid", 400

    if duration == 'last-one-year':
        min_required_date = datetime.now() - timedelta(365)
    else:
        min_required_date = datetime.now() - timedelta(365 * 2)



