from datetime import datetime, timedelta

import requests
import json
from bs4 import BeautifulSoup
from common.api import *


def check_if_url_exists(type, name, deadline=None, url=None):
    try:
        params = {
            'name': name,
        }

        if deadline is not None:
            params['deadline'] = deadline

        if url is not None:
            params['url'] = url

        if type == 'local_job':
            response = requests.get(local_job_url, params=params)
        elif type == 'external_job':
            response = requests.get(external_job_url, params=params)
        elif type == 'grant':
            response = requests.get(grant_url, params=params)
        else:
            response = requests.get(tender_url, params=params)

        if response.status_code != 200:
            return False

        response = response.json()
        return response['data'] is not None

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return False


def is_webpage(url):
    response = requests.head(url)
    content_type = response.headers.get("content-type")
    if content_type is None:
        return False
    return content_type.startswith("text/html")


def add_one_month_deadline():
    current_date = datetime.now()

    one_month_from_now = current_date + timedelta(days=30)

    date_format = "%Y-%m-%d"

    return one_month_from_now.strftime(date_format)


def get_raw_text(url):
    if not is_webpage(url):
        return False

    response = requests.get(url)
    job_content = BeautifulSoup(response.text, 'html.parser')
    text = job_content.get_text().replace("\n", "").strip()

    return text
