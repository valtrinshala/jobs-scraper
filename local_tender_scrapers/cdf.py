import re
from common.helpers import *


class Cdf:
    url = "https://kcdf.org/procurement/"
    date_format = "%Y-%m-%d"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')
        jobs = soup.find_all('div', class_="elementor-column")[1].find_all('div', class_="elementor-text-editor elementor-clearfix")

        for job in jobs:
            data = str(job.find_all('tr')[1])
            title = self.get_title(data)
            deadline = self.get_deadline(data)

            url = job.find('a')['href']

            url_exists = check_if_url_exists("tender", title, deadline)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": None,
                    "deadline": deadline,
                    "provider": "Cdf",
                    'country': "Kosovo"
                })

        return self.parsedData

    def get_title(self, data):
        title_labels = ["<strong>Titulli:</strong>", "<strong>Title:</strong>"]
        title = None
        for label in title_labels:

            if label in data:
                title = data.split(label)[1].split("<br>")[0]
                break
        if title:
            title = title.split('</td>')[0]
            title = title.split('<a href')[0]
            title = title.strip()

        return title

    def get_deadline(self, data):
        deadline_labels = ["<strong>Data e dorëzimit:</strong> ", "<strong>Submission Date:</strong>"]
        deadline_str = None
        for label in deadline_labels:
            if label in data:
                match = re.search(r'(\d{2}\.\d{2}\.\d{4})', data.split(label)[1])
                if match:
                    deadline_str = match.group(1)
                    break

        if deadline_str:
            parsed_deadline = datetime.strptime(deadline_str, "%d.%m.%Y")
            formatted_deadline = parsed_deadline.strftime(self.date_format)
        else:
            formatted_deadline = None

        return formatted_deadline


