import csv
import os.path
import ast
import sqlite3


class FileManager:

    def __init__(self, result_file, saved_urls_db):
        self.result_file = result_file
        self.saved_urls_db = saved_urls_db
        self.data_directory = "../data/"

        self.db_conn = sqlite3.connect(self.get_full_path(saved_urls_db))
        self.db_cursor = self.db_conn.cursor()

    def add_found_url(self, url, is_parsed=False):
        if is_parsed:
            parsed = 1
        else:
            parsed = 0
        query = "INSERT INTO saved_urls VALUES ('{}', '{}')".format(
            url, parsed)

        self.db_cursor.execute(query)
        self.db_conn.commit()

    def change_url_to_parsed(self, url):

        query = "UPDATE saved_urls SET is_parsed = '1' WHERE url = '{}'".format(
            url)
        self.db_cursor.execute(query)
        self.db_conn.commit()

    def get_saved_urls_set(self):

        self.db_conn.row_factory = lambda cursor, row: row[0]
        c = self.db_conn.cursor()
        all_urls = c.execute('SELECT url FROM saved_urls').fetchall()

        return set(all_urls)

    def get_unparsed_urls_set(self):

        self.db_conn.row_factory = lambda cursor, row: row[0]
        c = self.db_conn.cursor()
        query = "SELECT url FROM saved_urls WHERE is_parsed='0'"
        unparsed_urls = c.execute(query).fetchall()

        return set(unparsed_urls)

    def setup_database(self):

        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS saved_urls
                           (url text, is_parsed boolean)
                            """)

        self.db_conn.commit()

    def cleanup_database(self):

        self.db_cursor.execute('''DROP TABLE IF EXISTS saved_urls''')
        self.db_conn.commit()

    def database_is_empty(self):

        query_count = "select count(*) from sqlite_master where type='table' and name='saved_urls'"
        number_of_tables = self.db_cursor.execute(query_count).fetchall()[0][0]

        return number_of_tables == 0

    def is_empty(self, filename):
        return os.stat(filename).st_size == 0

    def get_full_path(self, file_name):

        relative_path = "{}{}".format(self.data_directory, file_name)
        current_path = os.path.dirname(__file__)
        path = os.path.join(current_path, relative_path)

        return path

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

    def clear_result(self):

        filename = self.get_full_path(self.result_file)

        f = open(filename, "w+")
        f.close()
