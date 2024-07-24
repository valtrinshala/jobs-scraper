from common.helpers import *


class WorldBank:
    url = "https://search.worldbank.org/api/v2/procnotices?format=json&fct=procurement_group_desc_exact,notice_type_exact,procurement_method_code_exact,procurement_method_name_exact,project_ctry_code_exact,project_ctry_name_exact,regionname_exact,rregioncode,project_id,sector_exact,sectorcode_exact&fl=id,bid_description,project_ctry_name,project_name,notice_type,notice_status,notice_lang_name,submission_date,noticedate&srt=submission_date%20desc,id%20asc&apilang=en&rows=20&srce=both&os=0&project_ctry_name_exact=Kosovo&regionname_exact=&sector.sector_description=&notice_type_exact=&procurement_method_name_exact=&procurement_group_desc_exact="
    date_format = "%Y-%m-%d"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        data = self.fetch_data_from_api(self.url)
        if data is None:
            return None

        data = data['procnotices']
        for item in data:

            title = item['bid_description']
            category = item['notice_type']
            url = f"https://projects.worldbank.org/en/projects-operations/procurement-detail/{item['id']}"
            image = None
            # deadline = self.format_date(item['expirationDate'])
            provider = "World Bank"
            city = None

            url_exists = check_if_url_exists("tender", title)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": image,
                    "deadline": None,
                    "provider": provider,
                    "city": city,
                    "categories": [category],
                    'country': "Kosovo",
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

    def format_date(self, date):
        datetime_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

        return datetime_obj.strftime(self.date_format)
