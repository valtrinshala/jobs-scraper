from common.job_category_translator import JobCategoryTranslator
from common.helpers import *


class ArbeitsAgentur:
    date_format = "%Y-%m-%d"

    def __init__(self):
        self.parsedData = []
        self.on_site_categories = [
            "Verkauf (ohne Produktspezialisierung)",
            "Lagerwirtschaft, Post und Zustellung, Güterumschlag",
            "Maschinenbau- und Betriebstechnik",
            "Büro und Sekretariat",
            "Elektrotechnik",
            "Erziehung, Sozialarbeit, Heilerziehungspflege",
            "Krankenpflege, Rettungsdienst und Geburtshilfe",
            "Metallbearbeitung",
            "Altenpflege",
            "Reinigung",
            "Speisenzubereitung",
            "Einkauf und Vertrieb",
            "Bau- und Transportgeräteführung",
            "Informatik",
            "Klempnerei, Sanitär-, Heizungs- und Klimatechnik",
            "Arzt- und Praxishilfe",
            "IT-Netzwerktechnik, -Administration, -Organisation",
            "Hochbau",
            "Bauplanung und -überwachung, Architektur",
            "Verkauf von Lebensmitteln",
            "Werbung und Marketing",
            "Holzbe- und -verarbeitung",
            "Hotellerie",
            "Aus- und Trockenbau, Isolierung, Zimmerei, Glaserie",
            "Softwareentwicklung und Programmierung",
            "Maler, Stuckateure, Bautenschutz",
            "Hauswirtschaft und Verbraucherberatung",
            "Gartenbau",
            "Handel",
            "Rechtsberatung, -sprechung und -ordnung",
            "Körperpflege",
            "Metallboberflächenbehandlung",
            "Bodenverlegung",
            "Textilverarbeitung",
            "Drucktechnik, Buchbinderei",
            "Metallerzeugung",
            "Industrielle Glasherstellung",
            "Industrielle Glasherstellung",
            "Industrielle Keramikherstellung",
            "Verlags- und Medienwirtschaft",
            "Berg-, Tagebau und Sprengtechnik"
        ]

        self.remote_categories = [
            'Verkauf (ohne Produktspezialisierung)', 'Büro und Sekretariat', 'Einkauf und Vertrieb', 'Informatik',
            'IT-Netzwerktechnik, -Administration, -Organisation',
            'Werbung und Marketing', 'Softwareentwicklung und Programmierung', 'Handel',
            'Rechtsberatung, -sprechung und –ordnung', 'Verlags- und Medienwirtschaft'
        ]

        self.translator = JobCategoryTranslator()

    def get_data(self):

        self.get_jobs_based_on_type(is_remote=True)
        self.get_jobs_based_on_type(is_remote=False)

        return self.parsedData

    def get_jobs(self, jobs, category, is_remote):

        albanian_category = self.translator.get_translation(category)
        for item in jobs:

            title = item.get('titel', None)

            if not title:
                continue

            url = f"https://www.arbeitsagentur.de/jobsuche/jobdetail/{item['refnr']}"
            provider = "ArbeitsAgentur"

            arbeitsort = item.get('arbeitsort', {})
            city = arbeitsort.get('ort', None)

            url_exists = check_if_url_exists(type="external_job", name=title, deadline=None, url=url)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": None,
                    "deadline": None,
                    "provider": provider,
                    "categories": [albanian_category],
                    "city": city,
                    'country': "Germany",
                    "job_type": "full_time",
                    "work_type": "remote" if is_remote else "on_site"
                })

    def get_jobs_based_on_type(self, is_remote):

        categories = self.remote_categories if is_remote else self.on_site_categories
        arbeitszeit = 'ho' if is_remote else 'vz'

        for category in categories:
            url = f"https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs?berufsfeld={category}&page=1&size=25&arbeitszeit={arbeitszeit}"
            data = self.fetch_data_from_api(url)

            if data is None or not data.get('stellenangebote'):
                continue

            jobs = data['stellenangebote']
            self.get_jobs(jobs, category, is_remote)

    def fetch_data_from_api(self, api_url):
        try:
            response = requests.get(api_url, headers={'x-api-key': 'dcdeacbd-2b62-4261-a1fa-d7202b579848'})

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
