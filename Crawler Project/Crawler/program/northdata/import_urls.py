import pandas as pd

def import_urls(filepath):
    basepath = "C:/Users/admin/2. Privat/Startup Crawler/Startseiten/"
    filepath = basepath + filepath
    df = pd.read_csv(filepath, squeeze="boolean")
    list = df.tolist()
    return list