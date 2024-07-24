from common.job_category_translator import JobCategoryTranslator
from common.helpers import *


class Xing:
    date_format = "%Y-%m-%d"

    def __init__(self):
        self.parsedData = []

        self.on_site_categories = {
            20000, 70000, 41100, 180000, 41200, 200000, 210000, 40700, 210700, 230500,
            80000, 21100, 10000, 90000, 40000, 210100, 90200, 10200, 10400, 21200,
            170000, 20600, 80100, 230000, 90100, 230800, 230100, 10500, 230200, 150100,
            220000, 40900, 10300, 20400, 40300, 20900, 110000, 230600
        }

        self.remote_categories = [
            20000, 180000, 21100, 90000, 90200, 170000, 90100, 230200, 110000
        ]

        self.industry_to_category_map = {
            20000: "Verkauf (ohne Produktspezialisierung)",
            70000: "Lagerwirtschaft, Post und Zustellung, Güterumschlag",
            41100: "Maschinenbau- und Betriebstechnik",
            180000: "Büro und Sekretariat",
            41200: "Elektrotechnik",
            200000: "Erziehung, Sozialarbeit, Heilerziehungspflege",
            210000: "Krankenpflege, Rettungsdienst und Geburtshilfe",
            40700: "Metallbearbeitung",
            210700: "Altenpflege",
            230500: "Reinigung",
            80000: "Speisenzubereitung",
            21100: "Einkauf und Vertrieb",
            10000: "Bau- und Transportgeräteführung",
            90000: "Informatik",
            40000: "Klempnerei, Sanitär-, Heizungs- und Klimatechnik",
            210100: "Arzt- und Praxishilfe",
            90200: "IT-Netzwerktechnik, -Administration, -Organisation",
            10200: "Hochbau",
            10400: "Bauplanung und -überwachung, Architektur",
            21200: "Verkauf von Lebensmitteln",
            170000: "Werbung und Marketing",
            20600: "Holzbe- und -verarbeitung",
            80100: "Hotellerie",
            230000: "Aus- und Trockenbau, Isolierung, Zimmerei, Glaserie",
            90100: "Softwareentwicklung und Programmierung",
            230800: "Maler, Stuckateure, Bautenschutz",
            230100: "Hauswirtschaft und Verbraucherberatung",
            10500: "Gartenbau",
            230200: "Handel",
            150100: "Rechtsberatung, -sprechung und -ordnung",
            220000: "Körperpflege",
            40900: "Metallboberflächenbehandlung",
            10300: "Bodenverlegung",
            20400: "Textilverarbeitung",
            40300: "Drucktechnik, Buchbinderei",
            20900: "Industrielle Glasherstellung / Industrielle Keramikherstellung",
            110000: "Verlags- und Medienwirtschaft",
            230600: "Berg-, Tagebau und Sprengtechnik"
        }

        self.translator = JobCategoryTranslator()

    def get_data(self):

        self.get_jobs_based_on_type(is_remote=True)
        self.get_jobs_based_on_type(is_remote=False)

        return self.parsedData

    def get_jobs(self, jobs, category, is_remote):

        albanian_category = self.translator.get_translation(
            self.industry_to_category_map.get(category)) if self.industry_to_category_map.get(category) else None

        for job in jobs:
            url = job.get('link', None)
            title = job.get('title', None)
            city = job.get('location', None)
            image_path = job.get('thumbnail', None)
            deadline = None

            if not url:
                continue

            url_exists = check_if_url_exists(type="external_job", name=title, deadline=None, url=url)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": image_path,
                    "deadline": deadline,
                    "provider": 'XING',
                    "categories": [albanian_category],
                    "city": city,
                    'country': "Germany",
                    "job_type": "full_time",
                    "work_type": "remote" if is_remote else "on_site"
                })
        return self.parsedData

    def get_jobs_based_on_type(self, is_remote):

        categories = self.remote_categories if is_remote else self.on_site_categories
        job_type = 'filter.remote_option[]=FULL_REMOTE' if is_remote else 'filter.type[]=FULL_TIME'

        for category in categories:
            url = f"https://www.xing.com/jobs/api/search?filter.industry[]={category}&{job_type}&limit=25&offset=0"
            data = self.fetch_data_from_api(url)

            jobs = data.get('items', {})

            self.get_jobs(jobs, category, is_remote)

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
