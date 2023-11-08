import csv
import json
from collections import defaultdict
from datetime import datetime

from pika.exceptions import AMQPConnectionError

from models.schemas.competitoranalysis import CompetitorAnalysisParams
from utils.rabbitmq import create_rabbitmq_connection, create_channel, publish_message_to_rabbitmq, close_connection


def datetime_to_month_and_year(date: datetime) -> str:
    month = date.strftime("%b")
    year = date.year
    return month + ' ' + str(year)


def get_competitoranalysis_handler(input1: CompetitorAnalysisParams):
    required_column = ''
    if input1.timelineidentifier == 'expenditure':
        required_column = 'Spend'
    elif input1.timelineidentifier == 'transaction':
        required_column = 'Transactions'
    elif input1.timelineidentifier == 'customer_volume':
        required_column = 'Shoppers'

    file_path = 'env/sample.csv'
    data = None
    with open(file_path, mode='r') as file:
        # reading the CSV file
        csv_file = csv.DictReader(file)
        filtered_data = defaultdict(dict)
        # displaying the contents of the CSV file
        for lines in csv_file:
            # print(lines)
            try:
                # print(datetime.strptime(lines['Month'], "%d/%m/%Y"))
                month = datetime.strptime(lines['Month'], "%m/%d/%Y")
                if not lines['Month'].startswith('#') and month >= input1.min_required_date:
                    filtered_data[lines['brand']][datetime_to_month_and_year(month)] = lines[required_column]
            finally:
                pass
        companies = []
        for key, value in filtered_data.items():
            company = {
                'name': key,
                'data': value
            }
            companies.append(company)

        data = {
            'companies': companies
        }
        return data

def get_aggregate_handler(input1: CompetitorAnalysisParams):
    required_column = ''
    if input1.timelineidentifier == 'expenditure':
        required_column = 'Spend'
    elif input1.timelineidentifier == 'transaction':
        required_column = 'Transactions'
    elif input1.timelineidentifier == 'customer_volume':
        required_column = 'Shoppers'

    file_path = 'env/sample.csv'
    data = None
    with open(file_path, mode='r') as file:
        # reading the CSV file
        csv_file = csv.DictReader(file)
        filtered_data = defaultdict(dict)
        # displaying the contents of the CSV file
        for lines in csv_file:
            # print(lines)
            try:
                # print(datetime.strptime(lines['Month'], "%d/%m/%Y"))
                month = datetime.strptime(lines['Month'], "%m/%d/%Y")
                if not lines['Month'].startswith('#') and month >= input1.min_required_date:
                    filtered_data[lines['brand']][datetime_to_month_and_year(month)] = lines[required_column]
            finally:
                pass
        companies = []
        for key, value in filtered_data.items():
            company = {
                'name': key,
                'data': value
            }
            companies.append(company)

        data = {
            'companies': companies
        }
        return data


def generate_report_handler(input1: dict):
    # TODO add message to rabbitmq
    json_message = str(input1)
    json_message = json.dumps(input1)

    try:
        connection = create_rabbitmq_connection('localhost')
        try:
            channel = create_channel(connection)
            publish_message_to_rabbitmq(channel, 'my-queue', 'my-queue', json_message, '')
        finally:
            close_connection(connection)
    except AMQPConnectionError:
        print("RabbitMQ connection error. Retrying in 5 seconds...")
        return {
            "message": "rabbitmq connection error"
        }

    return {
        "message": "accepted request for report generation"
    }

