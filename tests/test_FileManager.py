from unittest import TestCase
from filemanager import FileManager


class FileManagerTest(TestCase):

    def setUp(self):
        self.manager = FileManager("found_urls.csv", "products.csv")

    def test_change_products_result(self):
        self.manager.clear_result()
        products = self.manager.get_product_names_set()
        self.assertEqual(set(), products)

        self.manager.add_to_results("epoca.com", "Blush", "Blush - Epoca")

        self.manager.add_to_results("epoca.com", "Batom", "Batom")
        products = self.manager.get_product_names_set()
        self.assertEqual({"Blush", "Batom"}, products)

        self.manager.clear_result()
        products = self.manager.get_product_names_set()
        self.assertEqual(set(), products)

    def test_change_found_urls(self):

        self.manager.clear_found_urls()
        urls = self.manager.get_urls_dict()
        self.assertEqual({}, urls)

        self.manager.add_to_found_urls("epoca.com")
        self.manager.add_to_found_urls("google.com")

        products = self.manager.get_urls_dict()
        self.assertEqual(
            {"epoca.com": False, "google.com": False}, products)

        self.manager.clear_found_urls()
        urls = self.manager.get_urls_dict()
        self.assertEqual({}, urls)
