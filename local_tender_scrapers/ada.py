from common.helpers import *


class ADA:
    url = "https://www.entwicklung.at/en/projects/all-projects?tx_mmcprojectlist_projectlist%5B%40widget_0%5D%5BcurrentPage%5D=1&tx_mmcprojectlist_projectlist%5BdemandListFilter%5D%5Bactive%5D=1&tx_mmcprojectlist_projectlist%5BdemandListFilter%5D%5Bcountry%5D=100&tx_mmcprojectlist_projectlist%5BdemandListFilter%5D%5BsearchTerm%5D=&tx_mmcprojectlist_projectlist%5BdemandListFilter%5D%5Btopic%5D=&tx_mmcprojectlist_projectlist%5B__trustedProperties%5D=%7B%22demandListFilter%22%3A%7B%22searchTerm%22%3A1%2C%22country%22%3A1%2C%22topic%22%3A1%2C%22active%22%3A1%7D%7D78aaf3c7f06b04e1766c43f0bc4a03d5606ad34f&cHash=4d30b7ee75a2b8dd22e81b948221af8b"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')

        jobs = soup.find_all('div', class_="tx_mmcprojectlist--item")

        for job in jobs:
            title = job.find('a').text.strip()
            url = job.find('a').get('href').strip()
            full_url = "https://www.entwicklung.at" + url
            deadline = None
            end_span = job.find('span', text=lambda text: text and 'End' in text)
            if end_span:
                deadline_span = end_span.find_next_sibling('span')
                if deadline_span:
                    deadline_str = deadline_span.text.strip()
                    deadline = self.format_date(deadline_str)

            url_exists = check_if_url_exists("tender", title)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": full_url,
                    "image_path": None,
                    "deadline": deadline,
                    "provider": "ADA",
                    'country': "Kosovo"
                })

        return self.parsedData

    def format_date(self, date):
        if not date:
            return None

        parsed_date = datetime.strptime(date, "%d.%m.%Y")

        return parsed_date.strftime("%Y-%m-%d")
