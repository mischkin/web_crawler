from program.data import get_data, get_impressum_soup
from program.export_csv import create_dataframe, export_csv
from program.get_links import company_crawler


def run_program(urllist):
    #create_csv()
    for url in urllist:

        WebsiteLinksDic = company_crawler(url)  # get all website links
        soup_impressum = get_impressum_soup(WebsiteLinksDic)
        data = get_data(WebsiteLinksDic, soup_impressum) # get data
        df = create_dataframe(data) # vreate dataframe
        export_csv(df)
    return data

#run_program(["https://www.photocircle.net","https://www.fdx.de", "https://landpack.de"])
run_program(["https://www.fdx.de"])


