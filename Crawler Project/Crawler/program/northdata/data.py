from request import get_soup
from get_values import get_firma, get_telefon, get_email, get_owner, get_foundation







def get_soup_impressum(website_links_list):
    impressumlist = ["impressum", "legal", "imprint", "disclaimer", "kontakt", "contact"]
    for impressum in impressumlist:
        for link in website_links_list:
            if impressum in link.lower():
                print(link)
                soup = get_soup(link)
                return soup
                break
    return None



def get_data_impressum(soup_impressum):
    Word_Dic = {}
    Word_Dic["firma"] = {}
    Word_Dic["firma"] = get_firma(soup_impressum)
    Word_Dic["telefon"] = {}
    Word_Dic["telefon"] = get_telefon(soup_impressum)
    Word_Dic["email"] = {}
    Word_Dic["email"] = get_email(soup_impressum)
    # print("impressum parsing fertig ")
    return(Word_Dic)


def get_soup_northdata(firma):
    base_url = "https://www.northdata.de/"
    name_split = firma.split(" ")
    name_split_string = [""]
    for i in range(0,len(name_split)):
        name_split_string[0] = str(name_split_string[0])  + str(name_split[i]) + "+"
    name_split_string[0] = name_split_string[0][:-1]
    search_url = str(base_url) + str(name_split_string[0])
    # print(search_url)
    soup = get_soup(search_url)
    soup = test_northdata(soup)
    return soup

def test_northdata(soup):
    div = soup.find_all("title")
    text = soup.find('title').get_text()
    if "SUCHE NACH" in text:
        return None
    else:
        return soup


def get_data_northdata(soup_northdata):
    soup = soup_northdata
    data_dic = {}
    try:
        div_1 = soup.find_all("div", class_="column")[2].find_all("p")
    except:
        return None
    keys_1 = ["Name", "Handelsregister", "Adresse", "Gegenstand"]
    for i in range(0,len(keys_1)):
        text = div_1[i].get_text().strip()
        data_dic[keys_1[i]] = text
    data_dic["owner"] = get_owner(soup_northdata)
    data_dic["foundation"] = get_foundation(soup_northdata)
    return data_dic #, div_2, div_3, div_4



def combine_data(url, impressum, northdata):
    data={}
    data[url] = {**impressum, **northdata}
    return data

