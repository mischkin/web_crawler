def create_csv():
    f = open("C:/Users/admin/2. Privat/Startup Crawler/Firmenliste/test.csv", "w")
    writer = csv.DictWriter(f, delimiter = ';', fieldnames=['Geschäftsführer', 'E-mail', 'Telefonnummer', 'Unternehmen','Mitarbeiter', 'Website',"Adresse", "Gründung", "Gegenstand", "Handelsregister" ])
    writer.writeheader()
    f.close()

def create_dataframe(data):
    company = list(data.keys())[0]
    data = data[list(data.keys())[0]]
    north = data["northdata"]
    north = csv_syntax_clean(north)
    pandas_dic = {'Geschäftsführer': north["owner"] ,'E-mail': data["email"]   , 'Telefonnummer': data["telefon"], 'Unternehmen': data["firma"] ,'Mitarbeiter': "Platzhalter", 'Website': company ,"Adresse": north["Adresse"] , "Gründung": north["foundation"], "Gegenstand": north["Gegenstand"] , "Handelsregister": north["Handelsregister"]}
    df = pd.DataFrame(data=pandas_dic, index = [0])
    return df

def csv_syntax_clean(north):
    for key in north:
        north[key] = re.sub(' +',' ', north[key].replace(';', '.').replace('\t', ' ').replace('\n', ' ').replace('\t', ' '))
    return north

def export_csv(df):
    filepath="C:/Users/admin/2. Privat/Startup Crawler/Firmenliste/test.csv"
    df.to_csv(filepath, mode='a',  sep=';', index=False, header = False, encoding='iso-8859-1')

