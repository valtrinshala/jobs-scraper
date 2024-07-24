from common.helpers import *


class Kastori:
    url = "https://octopus-app-sngkk.ondigitalocean.app/v1/jobs?page=1&limit=16&typeOfJob=pune,praktike"
    date_format = "%Y-%m-%d"

    def __init__(self):
        self.parsedData = []

    def get_data(self):

        data = self.fetch_data_from_api(self.url)

        if data is None:
            return None

        data = data['data']
        for item in data:

            title = item['title']
            # description = item['description']
            url = f"https://www.kastori.net/shpalljet/{item['_id']}"
            image = item['company']['images']['md']['url']
            deadline = self.formatDate(item['expirationDate'])
            provider = "Kastori"
            categories = item.get('categories', [])
            category = categories[0]['title'] if categories and isinstance(categories, list) and categories else None
            city = item.get('company', {}).get('city', None)

            url_exists = check_if_url_exists("local_job", title, deadline)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": image,
                    "deadline": deadline,
                    "provider": provider,
                    "categories": [category],
                    "city": city,
                    'country': "Kosovo",
                    "job_type": "full_time",
                    "work_type": "on_site"
                })

        return self.parsedData

    def fetch_data_from_api(self, api_url):
        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Error: Unable to fetch data from API. Status code: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def formatDate(self, date):
        datetime_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

        return datetime_obj.strftime(self.date_format)
