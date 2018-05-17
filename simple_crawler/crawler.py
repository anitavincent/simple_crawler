from simple_crawler.productpage import ProductPage
from simple_crawler.filemanager import FileManager
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from time import sleep
import queue as queue
import re


class Crawler:

    def __init__(self, base_url, file_manager, log):
        self.base_url = base_url
        self.file_manager = file_manager
        self.log = log
        self.url_queue = queue.Queue()
        self.url_set = {"{}/".format(base_url), }
        self.product_name_set = set()

    def add_content(self, url, title, product_name):
        if product_name in self.product_name_set:
            return

        self.product_name_set.add(product_name)
        self.file_manager.add_to_results(url, product_name, title)

    def queue_links(self, links):
        for link in links:
            link = self.get_full_url(link)
            if link in self.url_set:
                continue

            self.url_set.add(link)
            self.url_queue.put(link)

    def get_url_batch(self, size):
        batch = []

        while not self.url_queue.empty() and len(batch) <= size:
            batch.append(self.url_queue.get())

        return batch

    def parse_concurrently(self, url):

        links = ""
        content = ""

        try:
            page = ProductPage(url, self.base_url, self.url_set)
            links, content = page.parse()
        except Exception as e:
            self.log.add_error(e)

        return (links, content)

    def crawl(self, request_delay, thread_quant):
        self.url_queue.put(self.base_url)
        self.thread_pool = ThreadPoolExecutor(max_workers=thread_quant)

        while not self.url_queue.empty():

            urls = self.get_url_batch(thread_quant)

            future_list = []
            for url in urls:
                sleep(request_delay)
                future = self.thread_pool.submit(self.parse_concurrently, url)
                future_list.append(future)

            wait(future_list, return_when="ALL_COMPLETED")

            for future in future_list:
                links, content = future.result()

                if content != "":
                    self.add_content(content['url'], content[
                                     'title'], content['product_name'])
                self.queue_links(links)

            self.log.add_pages_processed(
                len(self.url_set), len(self.product_name_set))

    def get_full_url(self, url):
        regex = "^/.*$"
        if re.match(regex, url):
            return "{}{}".format(self.base_url, url)
        return url
