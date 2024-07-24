from common.helpers import *


class EProkurorimi:
    url = "https://e-prokurimi.rks-gov.net/SPIN_PROD/application/ipn/DocumentManagement/NewPreglediDokumenataFrm.aspx/"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        cookies = {
            'ASP.NET_SessionId': 'qx3lrv0hzjozfjgzzejyrw0i',
            'lang': 'sq-AL',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            # 'Cookie': 'ASP.NET_SessionId=qx3lrv0hzjozfjgzzejyrw0i; lang=sq-AL',
            'DNT': '1',
            'Referer': 'https://e-prokurimi.rks-gov.net/HOME/ClanakItemNew.aspx?id=327',
            'Sec-Fetch-Dest': 'iframe',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        response = requests.get(
            'http://e-prokurimi.rks-gov.net/SPIN_PROD/application/ipn/DocumentManagement/NewPreglediDokumenataFrm.aspx',
            cookies=cookies,
            headers=headers,
        )

        print (response)
        # html = requests.get(self.url).text
        #
        # soup = BeautifulSoup(html, 'html.parser')
        #
        # jobs = soup.find_all('div', class_="DatumObjave")

        # for item in all_items:
        #     title = item.text.strip()
        #     url = item.find('a').get('href').strip()
        #     image = item.find('img').get('src').strip()
        #
        #     url_exists = check_if_url_exists("tender", title)
        #
        #     if url_exists is not True:
        #         raw_text = get_raw_text(url)
        #
        #         # openai_model = OpenAiModel("deadline", raw_text)
        #         # deadline = openai_model.getResponse()
        #
        #         self.parsedData.append({
        #             "name": title,
        #             "url": url,
        #             "image_path": image,
        #             "deadline": None,
        #             "provider": "Kcs",
        #             'country': "Kosovo"
        #         })

        return self.parsedData
