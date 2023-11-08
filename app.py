# This is a sample Python script.
from threading import Thread

from flask import jsonify
from marshmallow import Schema
from marshmallow.fields import Field, String, Integer
from dotenv import load_dotenv
import os  # provides ways to access the Operating System and allows us to read the environment variables

from utils.rabbitmq import start_rabbitmq_consumer


# load_dotenv()

def execute_basic_bigquery():
    from google.cloud import bigquery

    client = bigquery.Client()

    # Perform a query.
    QUERY = (
        'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
        'WHERE state = "TX" '
        'LIMIT 100')
    # query_job = client.query(QUERY)  # API request
    # client.cancel_job(query_job.job_id, location='US')
    # print(query_job.job_id)
    query_job = client.get_job('2b97dd4a-659a-445a-a681-e26ee81bab13', location='us')
    rows = query_job.result()  # Waits for query to finish

    for row in rows:
        print(row.name)


def run_flask():
    from flask import Flask
    from controllers.report import report
    from controllers.search import search
    from gevent.pywsgi import WSGIServer
    # from flask_cors import  CORS

    app = Flask(__name__)

    # Register the API applications
    app.register_blueprint(report, url_prefix='/api/v1/report')
    app.register_blueprint(search, url_prefix='/api/v1/search')

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(error=str(e)), 400

    print(app.url_map)
    app.config['BASE_RESPONSE_SCHEMA'] = BaseResponse
    app.config['BASE_RESPONSE_DATA_KEY '] = 'data'
    app.run()

    # http_server = WSGIServer(('0.0.0.0', 5000), app)
    # http_server.serve_forever()


def create_bigquery():
    from google.cloud import bigquery
    from google.oauth2 import service_account

    # key_path = "env/gcloud-credentials.json"
    # scopes = ["https://www.googleapis.com/auth/bigquery"]
    # credentials = service_account.Credentials.from_service_account_file(
    #     key_path, scopes=scopes,
    # )

    # client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    client = bigquery.Client()  # this will automatically looks into the .env file
    query = "SELECT * FROM `bigquery-public-data.country_codes.country_codes` LIMIT 1000"

    job = client.query(query)
    print('country_name, alpha_2_code, alpha_3_code')
    for row in job.result():  # Wait for the job to complete.
        print("{}, {}, {}".format(row["country_name"], row["alpha_2_code"], row["alpha_3_code"]))

    client.close()
    # --protoPayload.methodName="jobservice.jobcompleted"


def execute_bigquery():
    from google.cloud import bigquery
    from google.oauth2 import service_account

    key_path = "env/gcloud-credentials.json"
    scopes = ["https://www.googleapis.com/auth/bigquery"]
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=scopes,
    )

    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    query = "SELECT * FROM `bigquery-public-data.country_codes.country_codes` LIMIT 1000"

    job = client.query(query)
    print('job id is', job.job_id)
    print('country_name, alpha_2_code, alpha_3_code')
    for row in job.result():  # Wait for the job to complete.
        print("{}, {}, {}".format(row["country_name"], row["alpha_2_code"], row["alpha_3_code"]))

    client.close()


class BaseResponse(Schema):
    data = Field()  # the data key
    message = String()
    code = Integer()




if __name__ == '__main__':
    load_dotenv()
    consumer_thread = Thread(target=start_rabbitmq_consumer)
    try:
        print('thread is starting')
        consumer_thread.start()
    except Exception as e:
        print('error message', e)
    run_flask()

    # start_rabbitmq_consumer().start()
    # print(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    # print(os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE"))
    # sol()
    # execute_basic_bigquery()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
