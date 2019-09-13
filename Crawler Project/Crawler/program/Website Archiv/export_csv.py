import pandas as pd
import re
import csv
import os

def create_csv(filename):
    f = open("C:/Users/admin/2. Privat/Startup Crawler/Startseiten/{}.csv".format(filename), "w")
    writer = csv.DictWriter(f, delimiter = ';', fieldnames=['Startseite'])
    writer.writeheader()
    f.close()

def create_dataframe(data):
    # company = list(data.keys())[0]
    # data = data[list(data.keys())[0]]
    # data = data[company]
    # data = csv_syntax_clean(data)
    # keys = ["owner", "email","telefon","firma","Adresse", "foundation", "Gegenstand", "Handelsregister" ]
    # for key in keys:
    #     if key not in list(data.keys()):
    #         data[key] = 'missing'
    # pandas_dic = {'Geschäftsführer': data["owner"] ,'E-mail': data["email"]   , 'Telefonnummer': data["telefon"], 'Unternehmen': data["firma"] ,'Mitarbeiter': "Platzhalter", 'Website': company ,'Adresse': data["Adresse"] , 'Gründung': data["foundation"], 'Gegenstand': data["Gegenstand"] , 'Handelsregister': data["Handelsregister"]}
    # print("==========================================")
    # print(data)
    # print("==========================================")
    df = pd.DataFrame(data)
    df = clean_df(df).drop_duplicates()
    return df

def clean_df(df):
    for i in range(0,len(df)):
        # print(df[0][i][-1])
        if df[0][i][-1] == "/":
            # print("vorher" + str(df[0][i]))
            df[0][i] = df[0][i][:-1]
            # print("nachher" + str(df[0][i]))
    return df


# def csv_syntax_clean(north):
#     for key in north:
#         north[key] = re.sub(' +',' ', north[key].replace(';', '.').replace('\t', ' ').replace('\n', ' ').replace('\t', ' '))
#     return north

def export_csv(df,filename):
    filepath="C:/Users/admin/2. Privat/Startup Crawler/Startseiten/{}.csv".format(filename)
    if os.path.isfile(filepath) == False:
        create_csv(filename)
    print("==========================================")
    print(filepath)
    print("==========================================")
    df.to_csv(filepath, mode='a',  sep=';', index=False, header = False, encoding='iso-8859-1')

