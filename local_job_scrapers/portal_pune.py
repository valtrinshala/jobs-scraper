from common.helpers import *


class PortalPune:
    url = "https://portalpune.com/"
    date_format = "%d/%m/%Y"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text

        soup = BeautifulSoup(html, 'html.parser')

        jobs = soup.find_all('div', class_="job-item")

        for job in jobs:

            title = job.find('h3').text.strip()

            city = job.find_all('li', class_="d-inline-block")[1].text.strip()

            if city == 'Fushë Kos...':
                city = "Fushë Kosovë"
            elif city == 'Të gjitha...':
                city = None

            date = job.find_all('li', class_="d-inline-block")[0].text.strip()

            deadline = self.get_deadline(date)

            url = job.find('a').get('href').strip()

            image = job.find('img').get('src').strip()

            url_exists = check_if_url_exists("local_job", title, deadline)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": image,
                    "deadline": deadline,
                    "provider": "Portal Pune",
                    'country': "Kosovo",
                    'city': city,
                    "job_type": "full_time",
                    "work_type": "on_site"
                })

        return self.parsedData

    def get_deadline(self, days):
        if days.lower() == "skadon sot":
            date = datetime.now().strftime("%d/%m/%Y")
            return str(datetime.strptime(date, self.date_format).date())

        deadline_in_days = [int(x) for x in days.split() if x.isdigit()][0]

        current_date = datetime.now()
        future_date = current_date + timedelta(days=deadline_in_days)

        date = future_date.strftime("%d/%m/%Y")

        return str(datetime.strptime(date, self.date_format).date())
