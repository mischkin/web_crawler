import re
from bs4 import BeautifulSoup
import numpy as np
import requests


r = requests.get("http://geco-gardens.de")
html = r.text
soup = BeautifulSoup(html, "html5lib")

links_html = soup.find_all('a')


Links = []
for link_html in links_html:
    link = link_html.get('href')
    Links.append(link)
    
    
    
def GetLinks(url):
    RawLinks = []
    soup = get_soup(url)
    links_html = soup.find_all('a')
    for link_html in links_html:
        link = str(link_html.get('href'))
        if len(link) >= 4:
            if url[-1] = "/":
                url = url[:-1]
            if 'http' not in link:
                fullurl = url + link

                RawLinks.append(fullurl)
    RawLinks = list(set(RawLinks))
    #print(RawLinks)
    return RawLinks


impressumlist = ["impressum", "legal", "imprint", "disclaimer", "kontakt"]
for link in Links:
    for impressum in impressumlist:
        if impressum in link.lower():
            print(link)
            break