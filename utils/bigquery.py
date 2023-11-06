def create_bigquery_client():
    from google.cloud import bigquery
    from google.oauth2 import service_account

    key_path = "env/gcloud-credentials.json"
    scopes = ["https://www.googleapis.com/auth/bigquery"]
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=scopes,
    )

    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    return client

def cancel_bigquery_job():
    pass
