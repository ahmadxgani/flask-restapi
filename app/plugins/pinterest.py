import re
import json

from requests import get
from bs4 import BeautifulSoup as soup

from pydotmap import DotMap

class PinterestImageScraper:

    def __init__(self):
        self.json_data_list = []

    # ---------------------------------------- GET GOOGLE RESULTS ---------------------------------
    @staticmethod
    def get_pinterest_links(body):
        searched_urls = []
        html = soup(body, 'html.parser')
        links = html.select('#main > div > div > div > a')
        print('[+] saving results ...')
        for link in links:
            link = link.get('href')
            link = re.sub(r'/url\?q=', '', link)
            if link[0] != "/" and "pinterest" in link:
                searched_urls.append(link)

        return searched_urls

    # -------------------------- save json data from source code of given pinterest url -------------
    def get_source(self, url):
        try:
            res = get(url)
        except Exception as e:
            return
        html = soup(res.text, 'html.parser')
        # get json data from script tag having id initial-state
        json_data = html.find_all("script", attrs={"id": "initial-state"})
        for a in json_data:
            self.json_data_list.append(a.string)

    # --------------------------- READ JSON OF PINTEREST WEBSITE ----------------------
    def save_image_url(self):
        print('[+] saving image urls ...')
        url_list = [i for i in self.json_data_list if i.strip()]
        if not len(url_list):
            return url_list
        url_list = []
        for js in self.json_data_list:
            try:
                data = DotMap(json.loads(js))
                urls = []
                for response in data.resourceResponses:
                    if isinstance(response.response.data, list):
                        for u in range(len(response.response.data)):
                            if isinstance(response.response.data[u].images.get("474x"), list):
                                for i in response.response.data[u].images.get("474x"):
                                    urls.append(i)
                            else:
                                urls.append(response.response.data[u].images.get("474x"))
                    else:
                        if isinstance(response.response.data.images.get("474x"), list):
                            for i in response.response.data.images["474x"]:
                                urls.append(i)
                        else:
                            urls.append(response.response.data.images.get("474x"))

                for data in urls:
                    url_list.append(data.url)
            except Exception as e:
                continue

        return url_list

    # -------------------------- get user keyword and google search for that keywords ---------------------
    @staticmethod
    def start_scraping(key):
        try:
            keyword = key + " pinterest"
            keyword = keyword.replace("+", "%20")
            url = f'http://www.google.co.in/search?hl=en&q={keyword}'
            print('[+] starting search ...')
            res = get(url)
            searched_urls = PinterestImageScraper.get_pinterest_links(res.content)
        except Exception as e:
            return []

        return searched_urls, key.replace(" ", "_")

    def make_ready(self, kata):
        extracted_urls, keyword = PinterestImageScraper.start_scraping(kata)

        print('[+] saving json data ...')
        for i in extracted_urls:
            self.get_source(i)

        # get all urls of images and save in a list
        url_list = self.save_image_url()
        
        if len(url_list):
            return url_list
        else:
            return None