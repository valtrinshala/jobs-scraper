import re
from common.helpers import *


class Gjirafa:
    url = "https://gjirafa.com/Top/Pune"
    date_format = "%d/%m/%Y"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')

        allJobs = soup.find('ul', class_="listView")
        jobs = allJobs.find_all('li')

        for job in jobs:

            title = None
            deadline = None
            category = None
            city = None
            url = None
            image = None
            titleEl = job.find('h3', id="titulli")

            if titleEl is not None:
                title = titleEl.text.strip()

            preferencesEl = job.findAll('div', class_="half mrrjp_ct")

            if len(preferencesEl) != 0 and preferencesEl is not None:
                deadline = self.get_deadline(preferencesEl[1])

            if len(preferencesEl) != 0 and preferencesEl is not None:
                category = self.get_category(preferencesEl[0])

            if len(preferencesEl) != 0 and preferencesEl is not None:
                city = self.get_city(preferencesEl[0])

            url = job.find('a')
            if url is not None:
                url = url.get('href').strip()

            image_el = job.find('div', class_='mp_img')
            if image_el is not None:
                image = self.get_image(image_el)

            if image == '/Images/promovoIco.png':
                image = None

            if title is not None:

                url_exists = check_if_url_exists("local_job", title, deadline)

                if url_exists is not True:
                    self.parsedData.append({
                        "name": title,
                        "url": url,
                        "image_path": image,
                        "deadline": deadline,
                        "provider": "Gjirafa",
                        'country': "Kosovo",
                        'city': city,
                        'categories': [category],
                        "job_type": "full_time",
                        "work_type": "on_site"
                    })

        return self.parsedData

    def get_deadline(self, deadline_el):
        deadline_pattern = r"Data e Skadimit:</em>\s*([\d/]+)"
        deadline_match = re.search(deadline_pattern, str(deadline_el))

        if deadline_match:
            deadline = deadline_match.group(1)
            deadline_date = datetime.strptime(deadline, "%d/%m/%Y").date()
            return str(deadline_date)

        return None

    def get_category(self, category_el):
        category_pattern = r"Kategoria:</em>\s*([\w\s]+)"
        category_match = re.search(category_pattern, str(category_el))

        if category_match:
            category = category_match.group(1)
        else:
            category = None

        return category

    def get_city(self, city_el):
        city_pattern = r"Shteti:</em>\s*([\w\s]+)"
        city_match = re.search(city_pattern, str(city_el))

        if city_match:
            city = city_match.group(1)
        else:
            city = None

        return city

    def get_image(self, element):
        style_attribute = element['style']
        start_index = style_attribute.index("url('") + len("url('")
        end_index = style_attribute.index("')")
        return style_attribute[start_index:end_index]

