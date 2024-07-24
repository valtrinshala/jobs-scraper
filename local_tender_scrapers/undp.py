from common.helpers import *


def format_date(date):
    if not date:
        return None

    parsed_date = datetime.strptime(date, "%d-%b-%y")
    return parsed_date.strftime("%Y-%m-%d")


class Undp:
    url = "https://procurement-notices.undp.org/search.cfm"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')

        jobs = soup.find_all('tr', class_=['odd', 'even'])

        for job in jobs:

            columns = job.find_all('td')
            for column in columns:
                if "kosovo" in column.text.lower().strip():
                    self.save_tender(job)

        return self.parsedData

    def save_tender(self, job):

        a_tag = job.find('a')
        urlEl = a_tag.get('href')

        url = f"https://procurement-notices.undp.org/{urlEl}"
        title = a_tag.text.strip() if a_tag else None

        deadline_tag = job.find_all('nobr')[0] if job.find_all('nobr') else None
        deadline = deadline_tag.text.split()[0] if deadline_tag else None

        deadline = format_date(deadline)

        url_exists = check_if_url_exists("tender", title)

        if url_exists is not True:
            self.parsedData.append({
                "name": title,
                "url": url,
                "image_path": None,
                "deadline": deadline,
                "provider": "Undp",
                'country': "Kosovo"
            })
