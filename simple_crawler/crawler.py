from simple_crawler.productpage import ProductPage
import queue as queue


class Crawler:

    def __init__(self, base_url, file_manager):
        self.base_url = base_url
        self.file_manager = file_manager
        self.url_queue = queue.Queue()
        self.url_set = {base_url, }
        self.product_name_set = set()

    def add_content(self, url, title, product_name):
        pass

    def crawl(self, request_delay, thread_quant):
        self.url_queue.put(self.base_url)

        while not url_queue.empty():
            url = url_queue.get()
            page = ProductPage(url, self.base_url, self.url_set)
            content, links = page.parse()
            self.add_content(content['url'], content[
                             'title'], content['product_name'])
            self.queue_links(links)

    def get_full_url(self, url):
        pass
