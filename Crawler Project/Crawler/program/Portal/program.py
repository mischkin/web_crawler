# Ziel:
# Input: Seitenarchiv ( z.B: grune-startups)
# Output: Alle Startseiten

from get_links import cat_crawler
from export_csv import create_dataframe, export_csv


def program(urllist, filename):
    for url in urllist:
        linklist = cat_crawler(url)[1]
        df = create_dataframe(linklist)
        export_csv(df, filename)
program(["https://gruene-startups.de/gruene-unternehmen/"], "links01")