class Crawler:

    def __init__(self, base_url, file_manager):
        self.base_url = base_url
        self.found_urls = file_manager.get_urls_dict()
        self.saved_products = file_manager.get_product_names_dict()

    def add_to_results(self, url, title, product_name):
        pass

    def crawl(self, request_delay, thread_quant):
        pass

    def get_full_url(self, url):
        pass
