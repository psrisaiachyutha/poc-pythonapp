from typing import List

from utils.bigquery import create_bigquery_client


def search_brandname_handler(brand_name: str) -> List[str]:
    # creating a bigquery client
    bg_client = create_bigquery_client()
    raw_query = "SELECT country_name FROM `bigquery-public-data.country_codes.country_codes` where LOWER(country_name) like '{name}%'".format(
        name=brand_name.lower())

    job = bg_client.query(raw_query)
    return [row["country_name"] for row in job.result()]
