import re
import bs4
import numpy as np
import json

def get_telefon(soup):
    div = soup.find_all("div")
    regex = "\+49 \(0\)[ 0-9]+|[0][0-9][ 0-9]+|\+49[ 0-9]+"
    numbers_raw = []
    numbers_clean = []
    for div in div:
        numbers_raw  = re.findall(regex, div.get_text())
        for number in numbers_raw:
            #print(number)
            number = number.replace(' ','')
            if len(number) >= 10 and len(number) <= 20:
                numbers_clean.append(number)
    numbers_unique = list(dict.fromkeys(numbers_clean))
    seperator = ', '
    numbers_string = seperator.join(numbers_unique)
    # print(numbers_string)
    return(numbers_string)



def get_email(soup):
    div = soup.find_all("div")
    regex1 = "[a-zA-Z0-9_.+-]+\(at\)[a-zA-Z0-9_.+-]+" # Erster Teill ist der offizielle. ". für Fall info(at)gmx.de
    regex2 = "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+"
    emails_clean = []
    for div in div:
        emails1 = re.findall(regex1, div.get_text())
        emails2 = re.findall(regex2, div.get_text())
        emails = emails1 + emails2
        for email in emails:
            emails_clean.append(email)
    seperator = ', '
    emails_unique = list(dict.fromkeys(emails_clean))
    emails_string = seperator.join(emails_unique).replace('(at)', '@')
    # print(emails_string)
    return(emails_string)



def get_owner(soup):
    div_2 = json.loads(soup.find_all("div", class_ = "history ui grey segment")[0].find_all("figure", class_ = "bizq")[0].get("data-data"))["event"]
    text = []
    owner = []
    for div in div_2:
        text.append(div['text'])
    for element in text:
        if element[0:3] == "GF ":
            owner.append(element.replace('GF ', ''))
    owner_string = ', '.join(owner)
    return owner_string


def get_foundation(soup):
    Div = soup.find_all('div', class_ = 'event')
    foundation_raw = Div[-1].find_all("div", class_ = "date")[0].get_text().strip().replace(' ', '').replace('\n', '')
    foundation = re.findall("[0-9.]+", foundation_raw)[0]
    return foundation

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
        print(None)
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
            #            print("String")
            if len(element) >= 1:
                if any(x in element for x in rechtsformen):
                    if len(element.strip()) <= 40:
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
                #                print("String")
                #                print(element)
                if any(x in element for x in rechtsformen):
                    #                    print("in rechtsfromen")
                    if len(element) >= 1:
                        #                        print("größer 1")
                        if len(element.strip()) <= 40:
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
