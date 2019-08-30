from data import get_soup_impressum, get_data_impressum,  get_soup_northdata, get_data_northdata, combine_data
from export_csv import create_dataframe, export_csv
from company_crawler import company_crawler


def run_program(urllist, filename): # Input: Startseiten
    for url in urllist:
        website_links_list = company_crawler(url)  # get all website links

#1. Impressum ####
        soup_impressum = get_soup_impressum(website_links_list)
        data_impressum = get_data_impressum(soup_impressum) # get data
        firma = data_impressum["firma"]
#2. Northdata ####
        soup_northdata = get_soup_northdata(firma)
        data_northdata = get_data_northdata(soup_northdata)
#3. Combine data
        data = combine_data(url, data_impressum, data_northdata)
#4. Export ####
        df = create_dataframe(data) # vreate dataframe
        export_csv(df, filename)
    print("ganz durchgelaufen")
    return data

# run_program(["https://www.photocircle.net","https://www.fdx.de", "https://landpack.de"],"test05")
run_program(["https://landpack.de", "https://www.photocircle.net","https://www.fdx.de"],"test05")

# run_program(["https://www.fdx.de", ], "test04")




## TODO
# Exceptions reinbringen: Kein Impressum, Kein Northdata Eintrag, Keine Unternehmensform
# wenn link: href = /page_id=123 (s.biofabrik)
# wenn kein Impressum: DAnn auf Startseite suchen usw...
# Rechtsformen Liste: AG zu allgemeine, aber wenn steht AG\n weil dannach Absatz erkennt er es nicht
# get_words: div2-div4 noch nach Daten extrahieren
# Weitere nortdata   daten einbauen (Jahresbilanz usw...) # Json aus northdata auseinandernehmen
# Telefonnumer Varianten optimieren (alle möglichen Formate, aber normale Zahlenreihen ausschließen...)

