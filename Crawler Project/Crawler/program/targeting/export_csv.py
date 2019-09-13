import pandas as pd
import re
import csv
import os

def create_csv(file_export):
    f = open("C:/Users/admin/2. Privat/Startup Crawler/Firmenliste/{}.csv".format(file_export), "w")
    writer = csv.DictWriter(f, delimiter = ';', fieldnames=['Geschäftsführer', 'E-mail', 'Telefonnummer', 'Unternehmen','Mitarbeiter', 'Website',"Adresse", "Gründung", "Gegenstand", "Handelsregister" ])
    writer.writeheader()
    f.close()

def create_dataframe(data):
    company = list(data.keys())[0]
    # data = data[list(data.keys())[0]]
    data = data[company]
    data = csv_syntax_clean(data)
    keys = ["owner", "email","telefon","firma","Adresse", "foundation", "Gegenstand", "Handelsregister" ]
    for key in keys:
        if key not in list(data.keys()):
            data[key] = 'missing'
    pandas_dic = {'Geschäftsführer': data["owner"] ,'E-mail': data["email"]   , 'Telefonnummer': data["telefon"], 'Unternehmen': data["firma"] ,'Mitarbeiter': "Platzhalter", 'Website': company ,'Adresse': data["Adresse"] , 'Gründung': data["foundation"], 'Gegenstand': data["Gegenstand"] , 'Handelsregister': data["Handelsregister"]}
    df = pd.DataFrame(data=pandas_dic, index = [0])
    return df

def csv_syntax_clean(north):
    for key in north:
        north[key] = re.sub(' +',' ', north[key].replace(';', '.').replace('\t', ' ').replace('\n', ' ').replace('\t', ' '))
    return north

def export_csv(df,file_export):
    filepath="C:/Users/admin/2. Privat/Startup Crawler/Firmenliste/{}.csv".format(file_export)
    if os.path.isfile(filepath) == False:
        create_csv(file_export)
    print(filepath)
    df.to_csv(filepath, mode='a',  sep=';', index=False, header = False) #iso-8859-1'

