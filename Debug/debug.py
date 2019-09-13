import re
from bs4 import BeautifulSoup
import bs4
import numpy as np
import requests


## request
r = requests.get("https://www.bitsandpretzels.com/")
html = r.text
soup = BeautifulSoup(html, "html5lib")

links_html = soup.find_all('a')


# IMRPRESSUM URL
Links = []
for link_html in links_html:
    link = link_html.get('href')
    Links.append(link)

def trest():
    impressumlist = ["impressum", "legal", "imprint", "disclaimer", "kontakt"]
    for impressum in impressumlist:
        for link in Links:
            print(link)
            if impressum in link.lower():
                return link
trest()

# IMPRESSUM SOUP
def get_soup(url, count = 0):
    # count = {}
    # count[0] = 0
    trueloop = {}
    trueloop[0] = 0
    r = None
    while r is None:
        trueloop[0] += 1
        if trueloop[0] >= 2:
            print("Connection Failed")
            return None
            break
        else:
            try:                                            # könnte auch Session einführen
                r = requests.get(url)
            except requests.exceptions.Timeout:
                continue
            except requests.ConnectionError as e:
                print(e)
                print("new try in 20s")
                time.sleep(20)
                continue
            except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
                print (e)
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    if re.findall("Zu viele Abfragen", soup.get_text()):
        print("nortdata: Zu viele Abfragen - new try in 30s")
        time.sleep(30)
        count = count + 1
        if count <= 2:
            get_soup(url, count)
        else:
            return None
    return soup

url = ["https://www.startplatz.de/impressum/"]
def get_soup_impressum(website_links_list):
    impressumlist = ["impressum", "legal", "imprint", "disclaimer", "kontakt", "contact"]
    for impressum in impressumlist:
        for link in website_links_list:
            if impressum in link.lower():
                soup = get_soup(link)
                return soup
                break
    return None



### firma
'https://www.jobverde.de/impressum'




# alle div
# Wenn unterstes Element --> append
# Wenn weitere untere Elemente --> weiter runter gehen



div = soup.find_all("div")
firmalist = []


all_div = []
for element in div:
    all_div.append(element.text)

all_div_join = "\n".join(all_div).split("\n")

cleared_text = []
for string in all_div_join:
    string = string.strip()
    if len(string) >= 2:
        cleared_text.append(string)

rechtsformen = ["GmbH", "GbR", "OHG", " KG ", "KG\n", "AG ", "AG\n", "GmbH & Co KG", " UG "]
for string in cleared_text:
    if any(x in string for x in rechtsformen):
        firmalist.append(string)
        
if len(firmalist) == 0:
    print(firmalist)
    print(None)
else:
    unique,pos = np.unique(firmalist,return_inverse=True)
    counts = np.bincount(pos)
    maxpos = counts.argmax()
    firma = str(unique[maxpos]).replace('\n', '')
    # print(firma)
    print (firma)      


#########################################################
   

for element in div:
    for div_tag in soup.find_all('div'):
        if div_tag.find(lambda t: t.name != 'div'):
            print(div_tag.text)
            print('-' * 80)

#########################################################

def element_loop(Element, iteration, firmalist):
    print("function call")
    if iteration == 1:
        print("iteration 1")
        element = Element
        if type(element) == bs4.element.NavigableString:
            print("String")
            if len(element) >= 1:
                if any(x in element for x in rechtsformen):
                    if len(element) <= 30:
                        firmalist.append(element)
                        print(element)
        if type(element) == bs4.element.Tag:
            print("Tag")
#            print(element.get_text())
#            return None
            if any(x in element.get_text() for x in rechtsformen):
                print("ddeper")
                print(element)
                return element_loop(element, 2, firmalist)
    if iteration == 2: 
        print("iteration 2")
#        print("+\n")
        for c,element in enumerate(Element):
            print(str(c) + "/" + str(len(Element)))
    #        print("------------" + str(c))
    #        print(element)
    #        iterations[1] += 1
    #        print(iterations[1])
            if type(element) == bs4.element.NavigableString:
                print("String")
                print(element)
                if any(x in element for x in rechtsformen):
                    print("in rechtsfromen")
                    if len(element) >= 1:
                        print("größer 1")
                        if len(element) <= 80:
                            firmalist.append(element)
                            print(element)
            if type(element) == bs4.element.Tag:
                print("Tag")
                print(element)
                if any(x in element.get_text() for x in rechtsformen):
                    return element_loop(element, 2, firmalist)
            print("============ NEXT ITERATION ==================")
        return firmalist
    
def get_firma(soup):   
    div = soup.find_all("div")
    rechtsformen = ["GmbH", "GbR", "OHG", " KG ", "KG\n", "AG ", "AG\n", "GmbH & Co KG", " UG "]
    firmalist = []
    iterations = {}
    iterations[1] = 1
    for c,element in enumerate(div):
        print(element)
#        print("\n================================\n")
        element_loop(element, 1, firmalist)
    if len(firmalist) == 0:
        print(firmalist)
        print(None)
    else:
        unique,pos = np.unique(firmalist,return_inverse=True)
        counts = np.bincount(pos)
        maxpos = counts.argmax()
        firma = str(unique[maxpos]).replace('\n', '')
        # print(firma)
        print (firma)   
    return firmalist


#===========================================================================================================
    ## NEU
    
def element_loop(elementlist, iteration, firmalist):
    if iteration == 1:
        taglist = []
        for element in elementlist:
            if type(element) == bs4.element.NavigableString:
                print("String")
                print(element)
                if any(x in element for x in rechtsformen):
                    print("in rechtsfromen")
                    if len(element) >= 1:
                        print("größer 1")
                        if len(element) <= 80:
                            firmalist.append(element)
                            print(element)
            if type(element) == bs4.element.Tag:
                print("Tag")
                taglist.append(element)
                return element_loop(taglist, 2, firmalist)
    if iteration == 2:
        for Element in elementlist:
            taglist = []
            for element in Element:
                if type(element) == bs4.element.NavigableString:
                    print("String")
                    print(element)
                    if any(x in element for x in rechtsformen):
                        print("in rechtsfromen")
                        if len(element) >= 1:
                            print("größer 1")
                            if len(element) <= 80:
                                firmalist.append(element)
                                print(element)
                if type(element) == bs4.element.Tag:
                    print("Tag")
                    taglist.append(element)
                    return element_loop(taglist, 2, firmalist)
        return firmalist
    
def get_firma(soup):   
    div = soup.find_all("div")
    rechtsformen = ["GmbH", "GbR", "OHG", " KG ", "KG\n", "AG ", "AG\n", "GmbH & Co KG", " UG "]
    firmalist = []
    iterations = {}
    iterations[1] = 1
    for c,element in enumerate(div):
        print(element)
#        print("\n================================\n")
        element_loop(element, 1, firmalist) 
        
        
    if len(firmalist) == 0:
        print(firmalist)
        print(None)
    else:
        unique,pos = np.unique(firmalist,return_inverse=True)
        counts = np.bincount(pos)
        maxpos = counts.argmax()
        firma = str(unique[maxpos]).replace('\n', '')
        # print(firma)
        print (firma)   
    return firmalist




#=======================================================================
    
## SEHR NEU
def get_firma(soup):   
    div = soup.find_all("div")
    rechtsformen = ["GmbH", "GbR", "OHG", " KG ", "KG\n", "AG ", "AG\n", "GmbH & Co KG", " UG "]
    firmalist = []
    iterations = {}
    iterations[1] = 1
    for c,element in enumerate(div):
        print(" div Ebene: " + str(c) + "/" + str(len(div)))
        print(element)
        print("\n================================\n")
        neue_firmalist = element_loop_1(element, firmalist, rechtsformen)
        firmalist.append(neue_firmalist)
    print(firmalist)
    if len(firmalist) == 0:
        print(firmalist)
        print(None)
    else:
        unique,pos = np.unique(firmalist,return_inverse=True)
        counts = np.bincount(pos)
        maxpos = counts.argmax()
        firma = str(unique[maxpos]).replace('\n', '')
        # print(firma)
        print (firma)   
    return firmalist


  
def element_loop_1(Element, firmalist, rechtsformen):
    print("element_loop_1")
    elementlist = []
    for element in Element:
        if type(element) == bs4.element.NavigableString:
#            print("String")
            if len(element) >= 1:
                if any(x in element for x in rechtsformen):
                    if len(element) <= 30:
                        firmalist.append(element)
        if type(element) == bs4.element.Tag:
#            print("Tag")
    #            print(element.get_text())
    #            return None
            if any(x in element.get_text() for x in rechtsformen):
                elementlist.append(element)
    neue_firmalist = element_loop_2(elementlist, firmalist, rechtsformen)
    return neue_firmalist


def element_loop_2(elementlist, firmalist, rechtsformen, limit = 0):
    if limit >= 100:
        return firmalist
    limit += 1
    print("element_loop_1")
    neue_elementliste = []
    for listelement in elementlist:
        for c,element in enumerate(listelement):
#            print(str(c) + "/" + str(len(Element)))
    #        print("------------" + str(c))
    #        print(element)
    #        iterations[1] += 1
    #        print(iterations[1])
            if type(element) == bs4.element.NavigableString:
                print("String")
                print(element)
                if any(x in element for x in rechtsformen):
                    print("in rechtsfromen")
                    if len(element) >= 1:
                        print("größer 1")
                        if len(element) <= 80:
                            firmalist.append(element)
                            print(element)
            if type(element) == bs4.element.Tag:
                print("Tag")
                print(element)
                if any(x in element.get_text() for x in rechtsformen):
                    neue_elementliste.append(element)
    if len(neue_elementliste) >= 1:
        return element_loop_2(neue_elementliste, firmalist, rechtsformen, limit)
    else:
        return firmalist


    
    
#==========================








#===========================================================================================================
    





































                    
                    
#########################################################




##