import pika
import json
# import pandas
# import db_dtypes
def create_rabbitmq_connection(host_name: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host_name))
    return connection


def create_channel(connection):
    return connection.channel()


def publish_message_to_rabbitmq(channel, queue_name: str, routing_key: str, message_body, exchange=''):
    # Declare a queue
    channel.queue_declare(queue=queue_name)

    # Publish a message to the queue
    channel.basic_publish(exchange=exchange,
                          routing_key=routing_key,
                          body=message_body)


def close_connection(connection):
    connection.close()

def start_rabbitmq_consumer():

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='my-queue')

    # def callback(ch, method, properties, body):
    #     print(f"Received: {body}")

    def callback(ch, method, properties, body):

        message_body = json.loads(body)
        print(message_body)
        #ch.basic_ack(delivery_tag = method.delivery_tag)
        create_bigquery()

    channel.basic_consume(queue='my-queue', on_message_callback=callback, auto_ack=True)

    print("Waiting for messages. To exit, press Ctrl+C")

    #channel.basic_consume(queue='my-queue', on_message_callback=callback)
    channel.start_consuming()
    #return Thread(target=channel.start_consuming)

def execute_basic_bigquery():
    from google.cloud import bigquery

    client = bigquery.Client()

    # Perform a query.
    QUERY = (
        'SELECT TO_JSON_STRING(*)  FROM `bigquery-public-data.usa_names.usa_1910_2013` '
        
        'LIMIT 100')
    # query_job = client.query(QUERY)  # API request
    # client.cancel_job(query_job.job_id, location='US')
    # print(query_job.job_id)
    query_job = client.get_job('2b97dd4a-659a-445a-a681-e26ee81bab13', location='us')
    rows = query_job.result()  # Waits for query to finish
    print('printing the bigquery response', rows)
    # for row in rows:
    #     print(row.name)


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
    job.result().to_dataframe().to_csv('abc.csv')
    #df = job.to_dataframe()
    #df.to_csv('Your_filename.csv')
    # print('country_name, alpha_2_code, alpha_3_code')
    # for row in job.result():  # Wait for the job to complete.
    #     print("{}, {}, {}".format(row["country_name"], row["alpha_2_code"], row["alpha_3_code"]))
    #     print(row)
    # print('completed big query')
    client.close()
    # --protoPayload.methodName="jobservice.jobcompleted"

