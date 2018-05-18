#!/usr/bin/python
# -*- coding: utf-8-*-

from unittest import TestCase
from filemanager import FileManager
from page import Page
from crawler import Crawler
from log import Log
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


class CrawlerTest(TestCase):

    def setUp(self):

        manager = FileManager("products.csv", "urls.db")
        manager.cleanup_database()
        log = Log(verbose=False)
        self.crawler = Crawler(
            "https://www.epocacosmeticos.com.br", manager, log)

    def test_get_full_url(self):

        full_url = self.crawler.get_full_url("/bla")
        self.assertEqual("https://www.epocacosmeticos.com.br/bla", full_url)

        full_url = self.crawler.get_full_url(
            "https://www.epocacosmeticos.com.br/bla")
        self.assertEqual("https://www.epocacosmeticos.com.br/bla", full_url)

    def test_queue_links(self):
        links = ["httpd://linka", "httpd://linkb"]
        self.crawler.queue_links(links)

        self.crawler.url_queue.get()
        result1 = self.crawler.url_queue.get()
        result2 = self.crawler.url_queue.get()

        self.assertEqual(links[0], result1)
        self.assertEqual(links[1], result2)

    def test_get_url_batch(self):

        self.crawler.url_queue.get()
        links = ["httpd://link1", "httpd://link2",
                 "httpd://link3", "httpd://link4"]
        self.crawler.queue_links(links)

        batch = self.crawler.get_url_batch(3)

        self.assertEqual(links[0:3], batch)

    def test_parse(self):

        links, content = self.crawler.parse(
            "https://www.epocacosmeticos.com.br/")

        self.assertEqual("", content)
        self.assertTrue(len(links) > 0)

        links, content = self.crawler.parse(
            "https://www.epocacosmeticos.com.br/mascara-facial-ricca-bubble-help/p")

        product_name = "Máscara Facial Ricca - Bubble Help! - 1 Un"
        title = "Máscara Facial Ricca - Bubble Help! - Época Cosméticos"

        self.assertEqual(product_name, content['product_name'])
        self.assertEqual(title, content['title'])
        self.assertTrue(len(links) > 0)
