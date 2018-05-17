class Log:

    def __init__(self, verbose=False):
        self.verbose = verbose

    def add_error(self, error_message):
        print("[Warning] {}".format(error_message))

    def add_url_removal(self, url, reason=""):
        print("[Warning] Removing {} from queue. {}".format(url, reason))

    def add_pages_processed(self, number_of_pages, number_of_products):
        if self.verbose:
            print("[Log] {} pages processed, {} product pages found".format(
                number_of_pages, number_of_products))

    def add_message(self, message):
        print("[Log] {}".format(message))
