import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re


class ProductPage:

    target_regex = ".*/p"

    def __init__(self, page_url, base_url, queued_urls):
        self.page_url = page_url
        self.base_url = base_url

        if not self.is_parsing_target():
            raise Exception("Page out of website scope: {}".format(page_url))
        try:
            self.page_content = requests.get(page_url, timeout=10)
        except requests.exceptions.RequestException as e:
            raise RequestException(e)

        self.soup = BeautifulSoup(self.page_content.content, 'html.parser')
        self.queued_urls = queued_urls.copy()

    def parse(self):

        links = self.get_links()
        content = ""
        if self.is_scrapping_target():
            content = self.get_content()
            content["url"] = self.page_url
        return links, content

    def get_links(self):

        links_set = set()
        a_tags = self.soup.find_all('a', href=True)
        if not a_tags:
            raise ValueError("Could not find any links on page")

        for tag_content in a_tags:
            link = tag_content['href']
            if link not in self.queued_urls:
                self.queued_urls.add(link)
                links_set.add(link)

        return links_set

    def get_content(self):
        content = {}

        name_tags = self.soup.find_all("div", class_="productName")
        title_tags = self.soup.find_all("title")

        if not name_tags:
            raise ValueError("Could not find product name on page")

        content['product_name'] = name_tags[0].text
        content['title'] = title_tags[0].string

        return content

    def is_scrapping_target(self):
        regex = "^{}{}$".format(self.base_url, self.target_regex)
        if re.match(regex, self.page_url):
            return True
        return False

    def is_parsing_target(self):
        regex = "^({}|/).*$".format(self.base_url)
        if re.match(regex, self.page_url):
            return True
        return False
