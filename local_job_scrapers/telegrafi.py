from common.helpers import *


class Telegrafi:
    url = "https://jobs.telegrafi.com/"
    date_format = "%d/%m/%Y"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')

        jobs = soup.find_all('div', class_="job-info")

        for job in jobs:

            titleEl = job.find('div', class_="job-name").find('h3')

            deadlineEl = job.find('div', class_="job-schedule")

            category = job.find('span', class_="puna-position-title").text.strip()

            city = job.find('span', class_="puna-location").text.strip()

            title = titleEl.text.strip()

            date = deadlineEl.text.strip()

            deadline = self.get_deadline(date)

            url = job.find('a').get('href').strip()

            image = job.find('img').get('src').strip()

            if image == '/assets/img/passBackLogo.svg':
                image = None

            url_exists = check_if_url_exists("local_job", title, deadline)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": image,
                    "deadline": deadline,
                    "provider": "Telegrafi",
                    "country": "Kosovo",
                    "city": city,
                    "categories": [category],
                    "job_type": "full_time",
                    "work_type": "on_site"
                })

        return self.parsedData

    def get_deadline(self, days):
        if days.lower() == "sot":
            date = datetime.now().strftime("%d/%m/%Y")
            return str(datetime.strptime(date, self.date_format).date())

        deadline_in_days = [int(x) for x in days.split() if x.isdigit()][0]

        current_date = datetime.now()
        future_date = current_date + timedelta(days=deadline_in_days)

        date = future_date.strftime("%d/%m/%Y")

        return str(datetime.strptime(date, self.date_format).date())
