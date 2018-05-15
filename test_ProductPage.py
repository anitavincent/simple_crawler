from unittest import TestCase
from productpage import ProductPage
from bs4 import BeautifulSoup


class ProductPageTest(TestCase):

    def test_get_links(self):

        page = ProductPage(
            "http://webscraper.io/screenshots",
            "http://webscraper.io/",
            {})

        links = {'/',
                 '#',
                 'https://forum.webscraper.io/',
                 '/service',
                 '/data-specialist',
                 'http://chrome.google.com/webstore/detail/web-scraper/jnhgnonknehpejjnehehllkliplmbmhn',
                 '/contact',
                 '/screenshots',
                 '/tutorials',
                 '/test-sites',
                 '/documentation'}

        self.assertEqual(links, page.get_links())

    def test_get_content(self):

        page = ProductPage(
            "https://www.epocacosmeticos.com.br/mascara-facial-ricca-bubble-help/p",
            "https://www.epocacosmeticos.com.br/",
            {})

        content = "Máscara Facial Ricca - Bubble Help! - 1 Un"

        self.assertEqual(content, page.get_content())

    def test_is_scrapping_target(self):
        page = ProductPage(
            "https://www.epocacosmeticos.com.br/mascara-facial-ricca-bubble-help/p",
            "https://www.epocacosmeticos.com.br/",
            {})
        self.assertEqual(True, page.is_scrapping_target())

        page = ProductPage(
            "https://www.epocacosmeticos.com.br/",
            "https://www.epocacosmeticos.com.br/",
            {})
        self.assertEqual(False, page.is_scrapping_target())
