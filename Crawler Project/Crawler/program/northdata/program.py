from data import get_soup_impressum, get_data_impressum,  get_soup_northdata, get_data_northdata, combine_data
from export_csv import create_dataframe, export_csv
from company_crawler import company_crawler
from import_urls import import_urls
import pandas as pd


def run_program(file_import, file_export): # Input: Startseiten
    urllist = import_urls(file_import)
    fail = {}
    fail[0] = 0
    success = {}
    success[0] = 0
    fail_website_links_list = {}
    fail_website_links_list[0] = 0
    fail_soup_impressum = {}
    fail_soup_impressum[0] = 0
    fail_data_impressum = {}
    fail_data_impressum[0] = 0
    fail_firma = {}
    fail_firma[0] = 0
    fail_soup_northdata = {}
    fail_soup_northdata[0] = 0
    fail_data_northdata = {}
    fail_data_northdata[0] = 0


# print(urllist)
    for c,url in enumerate(urllist):
        print("\n")
        print(str(c) + "/" + str(len(urllist)))
        website_links_list = company_crawler(url)  # get all website links
        if website_links_list == None:
            print("skip: website_links_list")
            fail_soup_impressum[0] += 1
            continue
#1. Impressum ####
        soup_impressum = get_soup_impressum(website_links_list)
        if soup_impressum == None:
            print("skip: soup_impressum")
            fail_soup_impressum[0] += 1
            continue
        data_impressum = get_data_impressum(soup_impressum) # get data
        if data_impressum == None:
            print("skip: data_impressum")
            fail_data_impressum[0] += 1
            continue
        firma = data_impressum["firma"]
        if firma == None:
            print("skip: firma")
            fail_firma[0] += 1
            continue
#2. Northdata ####
        soup_northdata = get_soup_northdata(firma)
        if soup_northdata == None:
            print("skip: soup_northdata")
            fail_soup_northdata[0] += 1
            continue
        data_northdata = get_data_northdata(soup_northdata)
        if data_northdata == None:
            print("skip: data_northdata")
            fail_data_northdata[0] += 1
            continue
#3. Combine data
        data = combine_data(url, data_impressum, data_northdata)
#4. Export ####
        df = create_dataframe(data) # vreate dataframe
        # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        #     print(df)
        # print(df["Gegenstand"])
        export_csv(df, file_export)
        success[0] += 1
        print("success")
    print("\n---------- erfolgreich durchgelaufen ----------")

    print("\n--Analyse--")
    print(str(success[0]) + " von " + str(success[0]+ fail_soup_impressum[0] + fail_data_impressum[0] + fail_firma[0] + fail_soup_northdata[0] + fail_data_northdata[0]) + " erfolgreich")

    print("\nfails:")
    print("impressum_soup: " + str(fail_soup_impressum[0]))
    print("impressum_data: " + str(fail_data_impressum[0]))
    print("firma: " + str(fail_firma[0]))
    print("soup_northdata: " + str(fail_soup_northdata[0]))
    print("data_northdata: " + str(fail_data_northdata[0]))





# run_program(["https://www.photocircle.net","https://www.fdx.de", "https://landpack.de"],"test05")
# run_program(["http://www.klima-kontor.de"],"test05")

run_program("links01.csv", "test04")

#run_program("test.csv", "test05")





## TODO ##

# get_firma umstrukturieren
# neue Input Liste
# Machine Learning Prototype

# ANALYSE
## Logs immer wegspeichern



# Optimierung
## get_impressum_soup
### page id: wenn "impressum" in get_text
### kein Impressum: Nach sowas wie gmbh und Adresse suchen?!?!
### Browser leitet Startseite weiter (z.B https://www.ecobookstore.de zu https://www.ecobookstore.de/store)
## firma
### wenn uG WOrt Limit hochsetzen wegen "haftungsbeschränkt"
### Wenn mehrere IMpressum: impressum/imprint/disclaimer: WEnn in erstem nicht findet, nächstes probieren...

# Ideen
## NOrthdata Alternativen: Gruenderszene, Xing...
## Exceptions reinbringen: Kein Impressum, Kein Northdata Eintrag, Keine Unternehmensform
## wenn link: href = /page_id=123 (s.biofabrik)
## wenn kein Impressum: DAnn auf Startseite suchen usw...
## Rechtsformen Liste: AG zu allgemeine, aber wenn steht AG\n weil dannach Absatz erkennt er es nicht
## get_words: div2-div4 noch nach Daten extrahieren
## Weitere nortdata   daten einbauen (Jahresbilanz usw...) # Json aus northdata auseinandernehmen
## Telefonnumer Varianten optimieren (alle möglichen Formate, aber normale Zahlenreihen ausschließen...)

