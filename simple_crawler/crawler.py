from simple_crawler.page import Page
from simple_crawler.filemanager import FileManager
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
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

    # gets a batch of urls from queue
    def get_url_batch(self, size):
        batch = []

        while not self.url_queue.empty() and len(batch) <= size:
            batch.append(self.url_queue.get())

        return batch

    def parse(self, url):
        links = ""
        content = ""

        for i in range(0, 3):
            try:
                page = Page(url, self.base_url, self.url_set)
                links, content = page.parse()
                break
            except RequestException as e:
                self.log.add_error(e)
            except Exception as e:
                self.log.add_error(e)
                break

        return (links, content)

    def run_threads(self, urls, request_delay):

        future_list = []
        for url in urls:
                # wait before next request
            sleep(request_delay)
            # run parse url on a thread
            future = self.thread_pool.submit(self.parse, url)
            future_list.append(future)

        wait(future_list, return_when="ALL_COMPLETED")

        return future_list

    def process_threads_result(self, future_list):

        for future in future_list:
                # gets return of parse
                # parse was run by a thread
            links, content = future.result()

            if content != "":
                self.add_content(content['url'], content[
                                 'title'], content['product_name'])
            self.queue_links(links)

    def crawl(self, request_delay, thread_quant):
        self.url_queue.put(self.base_url)
        self.thread_pool = ThreadPoolExecutor(max_workers=thread_quant)

        while not self.url_queue.empty():

            url_batch = self.get_url_batch(thread_quant)

            future_list = self.run_threads(url_batch, request_delay)
            self.process_threads_result(future_list)

            self.log.add_pages_processed(
                len(self.url_set), len(self.product_name_set))

    def get_full_url(self, url):
        regex = "^/.*$"
        if re.match(regex, url):
            return "{}{}".format(self.base_url, url)
        return url
