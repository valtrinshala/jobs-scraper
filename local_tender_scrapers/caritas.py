from common.helpers import *


class Caritas:
    url = "https://www.caritaskosova.org/sq/shpallje"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')

        section = soup.find('div', class_="section-tpl")

        jobs = section.find_all('a')

        for job in jobs:

            title = job.text.strip()

            url = job.get('href').strip()

            url_exists = check_if_url_exists("tender", title)

            if url_exists is not True:

                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": None,
                    "deadline": None,
                    "provider": "Caritas",
                    'country': "Kosovo"
                })

        return self.parsedData
