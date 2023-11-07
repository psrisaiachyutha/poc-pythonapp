from typing import Union

from google.cloud import bigquery
from google.cloud.bigquery import LoadJob, CopyJob, ExtractJob, QueryJob, UnknownJob


def create_bigquery_client():
    from google.oauth2 import service_account

    key_path = "env/gcloud-credentials.json"
    scopes = ["https://www.googleapis.com/auth/bigquery"]
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=scopes,
    )

    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    return client


def cancel_job(
        client: bigquery.Client,
        job_id: str,
        location: str = "us"
) -> None:
    job = client.cancel_job(job_id, location=location)
    print(f"{job.location}:{job.job_id} cancelled")


def get_job(
        client: bigquery.Client,
        job_id: str,
        location: str = "us"
) -> Union[LoadJob, CopyJob, ExtractJob, QueryJob, UnknownJob]:
    job = client.get_job(job_id, location=location)
    return job



