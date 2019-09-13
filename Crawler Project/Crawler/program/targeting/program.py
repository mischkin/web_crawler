from data import get_soup_impressum, get_data_impressum,  get_soup_northdata, get_data_northdata, combine_data
from export_csv import create_dataframe, export_csv
from company_crawler import company_crawler
from import_urls import import_urls
import pandas as pd


def run_program(urllist):
    fail_website_links_list = {}
    fail_website_links_list[0] = 0

    for url in urllist:
        website_links_list = company_crawler(url)  # get all website links
        if website_links_list == None:
            print("skip: website_links_list")
            fail_website_links_list[0] += 1
            continue

    # Input: Urllist
    # 1. Iteration über urllist
    # 2. alle links einer Url (company_crawler)
    # 3. Alle Wörter aller Seiten in eine Liste
    # 4. Statistiken Worte
    # 5. Classifizierung der Website
    # 6. Output: Website + Klassifizierung







# run_program(["https://www.photocircle.net","https://www.fdx.de", "https://landpack.de"],"test05")
# run_program(["http://www.klima-kontor.de"],"test05")

run_program("links01.csv", "test04")

