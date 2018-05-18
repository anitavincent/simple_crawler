from unittest import TestCase
from filemanager import FileManager


class FileManagerTest(TestCase):

    def setUp(self):
        self.manager = FileManager("products.csv", "urls.db")

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

    def test_change_saved_urls(self):

        self.manager.cleanup_database()
        self.manager.setup_database()

        self.manager.add_found_url("epoca.com")
        self.manager.add_found_url("google.com")
        self.manager.add_found_url("wow.com")
        self.manager.add_found_url("fb.com")

        self.manager.change_url_to_parsed("wow.com")
        self.manager.change_url_to_parsed("fb.com")

        saved_urls = self.manager.get_saved_urls_set()
        self.assertEqual(
            {"epoca.com", "google.com", "wow.com", "fb.com"}, saved_urls)

        parsed_urls = self.manager.get_unparsed_urls_set()
        self.assertEqual(
            {"epoca.com", "google.com"}, parsed_urls)

        self.manager.cleanup_database()
        self.assertTrue(self.manager.database_is_empty())
