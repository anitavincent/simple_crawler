from simple_crawler.crawler import Crawler
from simple_crawler.filemanager import FileManager
from simple_crawler.log import Log


def main():
    manager = FileManager("found_urls.csv", "products.csv")
    log = Log(verbose=True)
    s = Crawler("https://www.epocacosmeticos.com.br", manager, log)
    s.crawl(0.20, 20)

if __name__ == '__main__':
    main()
