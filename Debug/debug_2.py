import re
from bs4 import BeautifulSoup
import bs4
import numpy as np
import requests





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

def get_soup_impressum(website_links_list):
    impressumlist = ["impressum", "legal", "imprint", "disclaimer", "kontakt", "contact"]
    for impressum in impressumlist:
        for link in website_links_list:
            if impressum in link.lower():
                soup = get_soup(link)
                return soup
                break
    return None

url = ["https://www.jobverde.de/impressum"]
soup = get_soup_impressum(url)












def get_firma(soup):   
    div = soup.find_all("div")
    rechtsformen = ["GmbH", "GbR", "OHG", " KG ", "KG\n", "AG ", "AG\n", "GmbH & Co KG", " UG "]
    final_firmalist = []
    iterations = {}
    iterations[1] = 1
    for c,element in enumerate(div):
#        print(" div Ebene: " + str(c) + "/" + str(len(div)))
#        print("\n================================\n")
#        print(element)
        firmalist = []
        neue_firmalist = element_loop_1(element, firmalist, rechtsformen)
#        print(neue_firmalist)
        final_firmalist.append(neue_firmalist)
#    print(firmalist)

    final_firmalist = [item for sublist in final_firmalist for item in sublist]
#    print("FINAL")
#    print(final_firmalist)
    if len(final_firmalist) == 0:
#        print(firmalist)
         return None
    else:
        unique,pos = np.unique(final_firmalist,return_inverse=True)
        counts = np.bincount(pos)
        maxpos = counts.argmax()
        firma = str(unique[maxpos]).replace('\n', '').strip()
        # print(firma)
#        print (firma)   
    print(firma)
    return firma


  
def element_loop_1(Element, firmalist, rechtsformen):
    firmalist = firmalist
#    print("element_loop_1")
    elementlist = []
    for element in Element:
        if type(element) == bs4.element.NavigableString:
#            print(element)
            if len(element) >= 1:
                if any(x in element for x in rechtsformen):
                    if len(element.strip()) <= 60:
                        firmalist.append(element)
        if type(element) == bs4.element.Tag:
#            print("Tag")
    #            print(element.get_text())
    #            return None
            if any(x in element.get_text() for x in rechtsformen):
                elementlist.append(element)
    neue_firmalist = element_loop_2(elementlist, firmalist, rechtsformen)
    print(neue_firmalist)
    return neue_firmalist


def element_loop_2(elementlist, firmalist, rechtsformen, limit = 0):
#    print(firmalist)
    firmalist = firmalist
    if limit >= 100:
        return firmalist
    limit += 1
#    print(limit)
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
#                    print("in rechtsfromen")
                    if len(element) >= 1:
#                        print("größer 1")
                        if len(element.strip()) <= 60:
                            firmalist.append(element)
#                            print(element)
            if type(element) == bs4.element.Tag:
#                print("Tag")
#                print(element)
                if any(x in element.get_text() for x in rechtsformen):
                    neue_elementliste.append(element)
#    print(firmalist)
    if len(neue_elementliste) >= 1:
#        print("erneut")
        return element_loop_2(neue_elementliste, firmalist, rechtsformen, limit)
    else:
        return firmalist



firmalist = get_firma(soup)