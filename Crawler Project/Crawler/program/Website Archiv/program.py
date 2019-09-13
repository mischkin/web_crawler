# Ziel:
# Input: Seitenarchiv ( z.B: grune-startups)
# Output: Alle Startseiten

from get_links import GetLinks
from export_csv import create_dataframe, export_csv


def program(url, filename):
    linklist = GetLinks(url)
    df = create_dataframe(linklist)
    export_csv(df, filename)
program("https://www.koeln.de/internetstadt_koeln/koelner_startups/koelner-startups-von-a-bis-z_819116.html", "köln_startups_1")