"""This code creates the class "Fetcher" which will execute the following steps:
- 1: fetch the data from a main page url;
- 2: save it to a file in tar.gz format;
- 3: call the specific parser of the source;
- 4: use it to create a dictionary with urls from the main page of the source;
- 5: fetch each child url contained in the dictionary;
- 6: save it to a file in tar.gz format;
- 7: use again the parser of the source to create a dataframe containing the title of the child url and the body of the news;
- 8: save the child page information in the database;
- 9: loop through the steps 5 to 8;
- 10: save the main page information in the database;

The "Fetcher" class has the following methods:

- __init__: creates the "Fetcher" object, by defining the source_id, name, url, raw_directory, processed_directory, cfg_log. Also, creates a "Directories_Manager" object, which is used to create the directory for the date and entity in both raw and  processed directories. By last, it calls the method "self.import_parser", which defines which source parser will be used.

- fetch_page_data: fetches the data of a given url and compress it into the data/raw file

- fetch_all_pages: fetches the data of the main page of the website, using the parameters of the source of the class

- fetch_website_pages: fetches the data of the main page and its childs, using both parameters of the source of the class and the urls in the main page, and them saves the body compressed and the and the metadata in the 'news' table of the database 

- fetch_api: fetches the data of the API of the source, saves the body compressed and the metadata in the 'news' table of the database 

- import_parser: import the parser class of the source, based on its name

- import_log: creates the log object, to be used in the future when the log is deployed
"""

import requests
from bs4 import BeautifulSoup as bs
from db import Db
#from format.estrategia import Parser

class Fetcher:
    def __init__(self, source, cfg_db):
        """The "Fetcher" object is a class to allow the fetching, parsing and storage of url data, from main pages and it childs.

        The "Fetcher" object requires the following arguments:
        - source(tuple(of information from the table sources of the database)): a tuple with all the relevant information of the source for this processing;
        - raw_directory(string): the directory where the data fetched, non-processed, will be stored ;
        - processed_directory(string): the directory where the data processed will be stored. Data processed are matrices, containing the title and body of the child pages;
        - cfg_log(string): the log configuration, as presented in the config/config.yaml file, and retrieved by the data_fetch scripts
        - cfg_db(string): the database configuration, as presented in the config/config.yaml file, and retrieved by the data_fetch scripts

        Also, the "Fetcher" object creates a "Directories_Manager" object, to assure that the datetime and entity directory is created and, by last, uses the method "self.import_parser" to create a "Parser" object of the source being processed."""
        (
            self.url_base,
            self.disciplina
        ) = source
        self.session = requests.Session()
        self.cfg_db = cfg_db
        self.db = Db(self.cfg_db)

        # Creating the "Parser" object, in accordance with the source being processed right now
        #self.parser_obj = self.import_parser()


    def fetch_pages_data(self, url=""):
        """
        This method fetchs the data from a website and them compress it into a gz file
        - page_name(string): This method can fetch two types of pages: main and child. By standard, the method will process as a main page
        - url(string): The url of the webpage as str. By standard, the method will use the self.url, that is, the url of the main page of the source
        """
        page_number = 1
        loop_finished = False

        while not loop_finished:
            if url == "":
                url = self.url_base + f"?page={page_number}&per_page=20"

            # The method will try to fetch the data, parse it as a soup and compress. In case of exception, it will return a request_error
            try:
                # Request the data from the url
                pg = self.session.get(url)
                soup = bs(pg.content, "html.parser")
                page_number += 1

            except Exception as fetch_exception:
                # Update the log with error if request does not succeed
                print(fetch_exception)
                soup = "request_error"
                loop_finished = True
                break

            finally:
                with open(f"D:/DocumentosHD/04 - Programacao/Github/Questao360/data/text/{page_number}.txt", "w") as file:
                    file.write(soup)


