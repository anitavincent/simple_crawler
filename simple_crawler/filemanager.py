import csv
import os.path
import ast


class FileManager:

    def __init__(self, found_urls_file, result_file):
        self.found_urls_file = found_urls_file
        self.result_file = result_file
        self.data_directory = "../data/"

    def is_empty(self, filename):
        return os.stat(filename).st_size == 0

    def get_full_path(self, file_name):

        relative_path = "{}{}".format(self.data_directory, file_name)
        current_path = os.path.dirname(__file__)
        path = os.path.join(current_path, relative_path)

        return path

    def get_urls_dict(self):

        return_dict = {}
        file_location = self.get_full_path(self.found_urls_file)

        with open(file_location, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row["url"]
                is_parsed = ast.literal_eval(row["is_parsed"])
                return_dict[url] = is_parsed

        return return_dict

    def get_product_names_set(self):

        return_set = set()
        file_location = self.get_full_path(self.result_file)

        with open(file_location, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row["product_name"]
                return_set.add(name)

        return return_set

    def add_to_results(self, url, product_name, title):

        file_location = self.get_full_path(self.result_file)

        with open(file_location, 'a', newline='') as csvfile:

            fieldnames = ['url', 'product_name', 'title']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if self.is_empty(file_location):
                writer.writeheader()

            writer.writerow(
                {'url': url, 'product_name': product_name, 'title': title})

    def add_to_found_urls(self, url):

        file_location = self.get_full_path(self.found_urls_file)

        with open(file_location, 'a', newline='') as csvfile:
            fieldnames = ['url', 'is_parsed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if self.is_empty(file_location):
                writer.writeheader()

            writer.writerow({'url': url, 'is_parsed': False})

    def clear_result(self):

        filename = self.get_full_path(self.result_file)

        f = open(filename, "w+")
        f.close()

    def clear_found_urls(self):

        filename = self.get_full_path(self.found_urls_file)

        f = open(filename, "w+")
        f.close()
