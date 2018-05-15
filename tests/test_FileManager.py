from unittest import TestCase
from filemanager import FileManager


class FileManagerTest(TestCase):

    def setUp(self):
        self.manager = FileManager("found_urls.csv", "products.csv")

    def test_change_products_result(self):
        self.manager.clear_result()
        products = self.manager.get_product_names_dict()
        self.assertEqual({}, products)

        self.manager.add_to_results("epoca.com", "Blush", "Blush - Epoca")
        self.manager.add_to_results("epoca.com", "Batom", "Batom")
        products = self.manager.get_product_names_dict()
        self.assertEqual({"Blush": True, "Batom": True}, products)

        self.manager.clear_result()
        products = self.manager.get_products_names_dict()
        self.assertEqual({}, products)

    def test_change_found_urls(self):

        self.manager.clear_found_urls()
        urls = self.manager.get_urls_dict()
        self.assertEqual({}, urls)
