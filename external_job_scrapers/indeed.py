import re
from urllib.parse import urlparse, parse_qs
from common.helpers import *


class Indeed:
    url = "https://www.indeed.com/jobs?q=doctor&l=Remote&vjk=cbf747028cec6cfa"

    def __init__(self):
        self.parsedData = []
        self.popularJobs = ['Software Developer', 'Customer service representative', 'Virtual assistant',
                            'FlexJobs Corporation',
                            'Data science', 'Sales Representative', 'Tutor', 'Designer', 'Financial Analyst',
                            'Data entry', 'Information Security Analyst', 'Database Administrator', 'Financial Manager',
                            'Statistician']

    def get_data(self):

        for category in self.popularJobs:
            html = requests.get(f"https://api.scrapfly.io/scrape?tags=player%2Cproject%3Adefault&asp=true&render_js=true&key=scp-live-246e37fd604f4254b3d27f53b1b36d41&url=https://www.indeed.com/jobs?q={category}&l=Remote&vjk=cbf747028cec6cfa").text

            soup = BeautifulSoup(html, 'html.parser')

            jobs = soup.find_all('div', class_="slider_item")

            if not jobs:
                continue

            self.get_jobs(jobs, category)

        return self.parsedData

    def get_jobs(self, jobs, category):

        for job in jobs:
            salaryEl = job.find('div', class_="salary-snippet-container") or job.find('div',
                                                                                      class_="estimated-salary-container")

            title = job.find('h2', class_="jobTitle").text.strip()

            # locationEl = job.find('div', class_="companyLocation").text.strip()
            #
            # city, country = self.get_location(locationEl)

            salary = None

            if salaryEl:
                salary = salaryEl.text.strip()

            partUrl = job.find('h2', class_="jobTitle").find('a').get('href')
            parsed_url = urlparse(partUrl)
            query_params = parse_qs(parsed_url.query)
            jk_attribute = query_params.get('jk', [None])[0]

            if not jk_attribute:
                continue

            url = f"https://www.indeed.com/m/viewjob?jk={jk_attribute}"

            url_exists = check_if_url_exists("external_job", title)

            if url_exists is not True:
                data_entry = {
                    "name": title,
                    "url": url,
                    "image_path": None,
                    "deadline": None,
                    "categories": [category],
                    "price": salary,
                    'country': 'United States',
                    "is_remote": True,
                    "provider": "Indeed",
                }

                # if city:
                #     data_entry["city"] = city

                self.parsedData.append(data_entry)

    def get_location(self, location):
        pattern = r"Remote in ([a-zA-Z\s]+, [A-Z]{2} \d{5})"

        match = re.search(pattern, location)
        if match:
            location = match.group(1)

            url = f"http://api.geonames.org/searchJSON?q={location}&maxRows=10&username=ilir"

            response = requests.get(url)
            data = response.json()

            if data.get('geonames'):
                first_result = data['geonames'][0]
                city = first_result['name']
                country = first_result['countryName']

                return city, country

        return None, None
