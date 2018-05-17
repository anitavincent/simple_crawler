#!/usr/bin/python
# -*- coding: utf-8-*-

from unittest import TestCase
from page import Page
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


class PageTest(TestCase):

    def test_parse(self):

        self.assertRaises(RequestException, Page,
                          "dstseresr",
                          "dstseresr",
                          set())

        page = Page(
            "https://www.epocacosmeticos.com.br/",
            "https://www.epocacosmeticos.com.br/",
            set())
        links, content = page.parse()
        self.assertEqual("", content)

        page = Page(
            "https://www.epocacosmeticos.com.br/mascara-facial-ricca-bubble-help/p",
            "https://www.epocacosmeticos.com.br/",
            set())

        links, content = page.parse()
        self.assertNotEqual("", content)

    def test_get_links(self):

        page = Page(
            "http://webscraper.io/screenshots",
            "http://webscraper.io/",
            set())

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

        page = Page(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Cat_poster_1.jpg/520px-Cat_poster_1.jpg",
            "https://upload.wikimedia.org/",
            set())

        self.assertRaises(ValueError, page.get_links)

    def test_get_content(self):

        page = Page(
            "https://www.epocacosmeticos.com.br/mascara-facial-ricca-bubble-help/p",
            "https://www.epocacosmeticos.com.br/",
            set())

        product_name = "Máscara Facial Ricca - Bubble Help! - 1 Un"
        title = "Máscara Facial Ricca - Bubble Help! - Época Cosméticos"

        self.assertEqual(product_name, page.get_content()['product_name'])
        self.assertEqual(title, page.get_content()['title'])

        page = Page(
            "https://www.epocacosmeticos.com.br/artliner-lancome-delineador/p",
            "https://www.epocacosmeticos.com.br/",
            set())

        product_name = "Artliner Lancôme - Delineador"
        title = "Artliner Lancôme - Delineador - Época Cosméticos"

        self.assertEqual(product_name, page.get_content()['product_name'])
        self.assertEqual(title, page.get_content()['title'])

        page = Page(
            "https://google.com",
            "https://google.com",
            set())

        self.assertRaises(ValueError, page.get_content)

    def test_is_scrapping_target(self):
        page = Page(
            "https://www.epocacosmeticos.com.br/mascara-facial-ricca-bubble-help/p",
            "https://www.epocacosmeticos.com.br/",
            set())
        self.assertTrue(page.is_scrapping_target())

        page = Page(
            "https://www.epocacosmeticos.com.br/",
            "https://www.epocacosmeticos.com.br/",
            set())
        self.assertFalse(page.is_scrapping_target())
