import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re


class ProductPage:

    target_regex = ".*/p"

    def __init__(self, page_url, base_url, queued_urls):
        self.page_url = page_url
        self.base_url = base_url
        try:
            self.page_content = requests.get(page_url)
        except requests.exceptions.RequestException as e:
            raise RequestException(e)
        self.soup = BeautifulSoup(self.page_content.content, 'html.parser')
        self.queued_urls = queued_urls

    def parse(self):
        links = self.get_links()
        content = ""
        if self.is_scrapping_target():
            content = self.get_content()
        return (links, content)

    def get_links(self):
        links_set = set()
        a_tags = self.soup.find_all('a', href=True)

        for tag_content in a_tags:
            link = tag_content['href']
            if link not in self.queued_urls:
                self.queued_urls[link] = False
                links_set.add(link)

        return links_set

    def get_content(self):
        tags = self.soup.find_all("div", class_="productName")
        return tags[0].text

    def is_scrapping_target(self):
        regex = "^{}{}$".format(self.base_url, self.target_regex)
        if re.match(regex, self.page_url):
            return True
        return False
