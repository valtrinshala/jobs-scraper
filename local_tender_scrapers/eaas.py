from common.helpers import *


class Eaas:
    url = "https://www.eeas.europa.eu/eeas/tenders_en?f%5B0%5D=tender_site%3AKosovo%2A&f%5B1%5D=tender_site%3AKosovo" \
          "%2A&s=321"
    date_format = "%Y-%m-%d"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')

        all_jobs = soup.find('div', class_="srch-results")

        jobs = all_jobs.find_all('div', class_="card")

        for job in jobs:

            title = job.find('a').text.strip()
            url = job.find('a').get('href').strip()
            deadline = None
            full_url = "https://www.eeas.europa.eu" + url

            deadline_element = job.find('div', class_='field--type-datetime')

            if deadline_element is not None:
                deadline = deadline_element.text.strip()

            deadline = self.format_date(deadline)

            url_exists = check_if_url_exists("tender", title, deadline)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": full_url,
                    "image_path": None,
                    "deadline": deadline,
                    "provider": "Eaas",
                    'country': "Kosovo"
                })

        return self.parsedData

    def format_date(self, date):
        if date:
            parsed_deadline = datetime.strptime(date, "%d.%m.%Y")
            formatted_deadline = parsed_deadline.strftime(self.date_format)
        else:
            formatted_deadline = None

        return formatted_deadline
