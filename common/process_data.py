import requests
from common.api import *

logs = []


def process_data(type, source):
    with requests.Session() as session:
        data = source.get_data()
        for obj in data:
            try:
                if type == 'local_job':
                    url = local_job_url
                elif type == 'external_job':
                    url = external_job_url
                elif type == 'grant':
                    url = grant_url
                else:
                    url = tender_url

                response = session.post(url, json=obj)

                if response.status_code not in [201, 400]:
                    logs.append((obj, response.json()))
                print("Response:", response.json(), obj)
            except requests.exceptions.RequestException as e:
                print("An error occurred:", e, obj)
