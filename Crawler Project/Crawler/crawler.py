import requests
from bs4 import BeautifulSoup
import re
from nltk.tokenize import RegexpTokenizer
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import ast


#1. Startseite URL
start_url = 'https://gruene-startups.de/gruene-unternehmen/'
#url = 'https://biofabrik.com/'
#url = 'https://biofabrik.com/Impressum/'
url = 'https://gruene-startups.de/gruene-unternehmen/wpbdp_category/clean-tech/'

#2. Alle Links auf Startseite

def GetLinks(url):
    RawLinks = []
    try:                                            # könnte auch Session einführen
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    links_html = soup.find_all('a')
    for link_html in links_html:
        link = str(link_html.get('href'))
        if len(link) >= 4:
            if link[0:4] == 'http':
                RawLinks.append(link) 
    RawLinks = list(set(RawLinks))
    #print(RawLinks)
    return RawLinks

def GetRegExpr(url):
    pos1 = 'http://www.'
    reg1 = 'http://[\w-]+\.[\w-]+\.[\w-]+'
    pos2 = 'https://www.'
    reg2 = 'https://[\w-]+\.[\w-]+\.[\w-]+'
    pos3 = 'http://'
    reg3 = 'http://[\w-]+\.[\w-]+'
    pos4 = 'https://'
    reg4 = 'https://[\w-]+\.[\w-]+'
    if url[0:11] == pos1:
        return(reg1, pos1)
    if url[0:12] == pos2:
        return(reg2, pos2)
    if url[0:7] == pos3 and url[0:11] != pos1:
        return(reg3, pos3)
    if url[0:8] == pos4 and url[0:12] != pos2:
        return(reg4, pos4)
    else:
        return(None, None)

def GetUrlVariations(url):
    UrlVariations = []
    UrlVariations.append(url)
    if GetRegExpr(url)[1] == 'http://www.':
        UrlVariations.append(url.split('http://')[0] + url.split('www.')[1])
    if GetRegExpr(url)[1] == 'http://':
        UrlVariations.append(url.split('http://')[0] + 'www.' + url.split('http://')[1])    
    if url[-1] != '/':
        UrlVariations.append(url + '/')
    if url[-1] == '/':
        UrlVariations.append(url[0:-1])
    return UrlVariations

    
def GetCategoryLinks(url):
    CatLinks = []
    RawLinks = GetLinks(url)
    for c,link in enumerate(RawLinks):
        print("{}/{} RawLinks".format(c,len(RawLinks)))
        if link.find('wpbdp_category') != -1:
                CatLinks.append(link)    
    CatLinks = list(set(CatLinks))
    return CatLinks

def GetWebsiteLinks(Startseite, urls):
    WebsiteLinks = []
    StartseiteVariations = GetUrlVariations(Startseite)
    for link in urls:
        if any(Startseite in link for Startseite in StartseiteVariations):
            WebsiteLinks.append(link)
    return WebsiteLinks
            
            
def GetStartseiteLinks(url): 
    StartLinks = []
    RawLinks = GetLinks(url)
    for c,link in enumerate(RawLinks):
        print("{}/{} RawLinks".format(c,len(RawLinks)))
        regexp = GetRegExpr(str(link))[0]
        print("regex: " + str(regexp))
        if regexp != None:
            reg = re.findall(regexp, link)
            if len(reg) >= 1:
                print(str(link) + " vs " + str(reg[0])) 
                if str(link) == str(reg[0]) or str(link) == str(reg[0] + "/"):
                        StartLinks.append(link)   
    print("vorher" + str(StartLinks))
    StartLinks = list(set(StartLinks))
    print("nachher" + str(StartLinks))
    return StartLinks

#3 Wörter extrahieren
def get_words(url, source = "north"):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    if source == "north":
        # Block
        data_dic = {}
        div_1 = soup.find_all("div", class_ = "column")[2].find_all("p")
        keys_1 = ["Name", "Handelsregister", "Adresse", "Gegenstand"]
        for c,p in enumerate(div_1):
            text = p.get_text().strip()
            data_dic[keys_1[c]] = text
        # Historie
        div_2 = ast.literal_eval(soup.find_all("div", class_ = "history ui grey segment")[0].find_all("figure", class_ = "bizq")[0].get("data-data"))["event"]
        history_list = []
        for c,element in enumerate(div_2): # Zeiten müssen noch chronologisch geordnet werden
            event = element["text"]
            time = element["time"]
            history_list.append(time)
            history_list.append(event) 
        # Jahresabschluss
        div_3 = ast.literal_eval(soup.find_all("div", class_ = "drill-downs charts ui grey segment")[0].find_all("div", class_ = "tab-content")[0].get("data-data"))
        # Bilanzsumme
        div_4 = ast.literal_eval(soup.find_all("div", class_ = "tab-content has-bar-charts")[0].get("data-data").strip().replace("\n", "").replace("false", '"false"'))
        return(div_1, div_2, div_3, div_4)
    else:        
        Meta = soup.find_all('meta')
        Content = []
        for meta in Meta:
            Content.append(meta.get('content'))
        text_html = soup.find_all('p')
        text = []
        for item in text_html:
            text.append(item.get_text())
        text_string = ''.join(text)
        tokenizer = RegexpTokenizer('\w+')
        tokens = tokenizer.tokenize(text_string)
        words = []
        for word in tokens:
            words.append(word.lower())
        sw = nltk.corpus.stopwords.words('english') # all words that are not stopwordsr = requests.get
        words_ns = []
        for word in words:
            if word not in sw:
                words_ns.append(word.lower())
        return words_ns







# Suchwörter
Suchwörter = ['gmbh', 'ug', 'ggmbh', 'gug']
Rechtsform = []
for word in words:
    for suchwort in Suchwörter:
        if word.find(suchwort) != -1:
            Rechtsform.append(word)
        
        

#  Visualisierung
def plot_word_dist(wordlist):
    freqdist1 = nltk.FreqDist(wordlist)
    freqdist1.plot(25)

#######################################################################
# Programm

def cat_crawler(url):
    # Dic mit allen Links
    LinkDic = {}
    # Startup Urls sammeln
    print("===================================")
    print("get all category links")
    print("===================================")

    CatLinks = GetCategoryLinks(url)
    # Startseiten Urls sammeln
    print("===================================")
    print("get Startseite Links for each category Link")
    print("===================================")
    for c,catlink in enumerate(CatLinks):
        print("{}/{} CatLinks".format(c,len(CatLinks)))
        print("\ngetting Starseite Links for {}\n".format(catlink))
        StartLinks = GetStartseiteLinks(catlink)
        print("Liste für: " + str(catlink) + str(StartLinks))
        LinkDic[catlink] = StartLinks 
    LinkList = [item for sublist in list(LinkDic.values()) for item in sublist]
    return LinkDic, LinkList

def company_crawler(urllist):
    WebsiteLinksDic = {}
    for c,company in enumerate(urllist):
        print(company + ": {}/{}".format(c, len(urllist)))
        RawCompanyLinks = GetLinks(company)
        WebsiteLinks = GetWebsiteLinks(company, RawCompanyLinks)
        WebsiteLinksDic[company] = WebsiteLinks
        print(WebsiteLinksDic[company])
    return WebsiteLinksDic
        
        
def word_crawler(LinkDic):
    Word_Dic = {}
    for c,company in enumerate(result_company):
        print(company + " beginnt: " + str(c) + "/" + str(len(result_company)))
        Word_Dic[company] = {}
        for c,link in enumerate(result_company[company]):
            print(str(c)+ "/" + str(len(result_company[company])))
            print(link)
            Word_Dic[company][link] = get_words(link)
            #print(Word_Dic[company])
        print(company + " fertig ")

        
def north_data(company_name):
    base_url = "https://www.northdata.de/"
    name_split = company_name.split(" ")
    name_split_string = [""]
    for i in range(0,len(name_split)):
        name_split_string[0] = str(name_split_string[0])  + str(name_split[i]) + "+"
    name_split_string[0] = name_split_string[0][:-1]
    search_url = str(base_url) + str(name_split_string[0])
    print(search_url)
    north_dic = get_words(search_url)   
    return north_dic
    
result = cat_crawler(start_url)

## words je company (alle links)
urllist = result[1]
result_company = company_crawler(urllist)

# northdata
company_name = "circle concepts GmbH"
result = north_data(company_name)


   

# LIste aus Dictionary
a = [item for sublist in list(Word_Dic.values()) for item in sublist]















