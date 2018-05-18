from simple_crawler.crawler import Crawler
from simple_crawler.filemanager import FileManager
from simple_crawler.log import Log
import sqlite3


def cleanup_database():
    pass


def main():

    manager = FileManager("products.csv", "urls.db")
    log = Log(verbose=True)
    s = Crawler("https://www.epocacosmeticos.com.br", manager, log)
    s.crawl(0.20, 20)

    manager.cleanup_database()

    log.add_message("Crawling finished")

if __name__ == '__main__':
    main()
