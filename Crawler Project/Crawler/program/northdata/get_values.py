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
    L = []
    L2 = []
    L2b = []
    L3 = []
    L4 = []
    Ls1 =[]
    # print(soup)
    div1 = soup.find_all("div")
    rechtsformen = ["GmbH", "GbR", "OHG", " KG ", "KG\n", "AG ", "AG\n", "GmbH & Co KG"]
    firmalist = []
    for c,element in enumerate(div1):
        #        print(str(c) + "/" + str(len(div1)-1))
        L.append(element)
        if len(element) >= 1 and type(element) == bs4.element.NavigableString:
            if any(x in element for x in rechtsformen):
                #                print("Ebene 1: " + str(c) + "/" + str(len(element)))
                if len(element) <= 30:
                    firmalist.append(element)
                #                    print(element)
        if len(element) >= 1 and type(element) == bs4.element.Tag:
            if any(x in element.get_text() for x in rechtsformen):
                for c, element in enumerate(element):
                    # print("Ebene 2: " + str(c) + "/" + str(len(element)))
                    #                    print(element)
                    if len(element) >= 1 and type(element) == bs4.element.NavigableString:
                        if any(x in element for x in rechtsformen):
                            #                            print("Ebene 2 " + str(c) + "/" + str(len(element)))
                            if len(element) <= 30:
                                firmalist.append(element)
                                #print(element)
                    if len(element) >= 1 and type(element) == bs4.element.Tag:
                        if any(x in element.get_text() for x in rechtsformen):
                            for c,element in enumerate(element):
                                #  print("Ebene 3: " + str(c) + "/" + str(len(element)))
                                #                                print(element)
                                if len(element) >= 1 and type(element) == bs4.element.NavigableString:
                                    if any(x in element for x in rechtsformen):
                                        if len(element) <= 30:
                                            firmalist.append(element)
                                if len(element) >= 1 and type(element) == bs4.element.Tag:
                                    if any(x in element.get_text() for x in rechtsformen):
                                        for c,element in enumerate(element):
                                            # print("Ebene 4: " + str(c) + "/" + str(len(element)))
                                            #print(element)
                                            if len(element) >= 1 and type(element) == bs4.element.NavigableString:
                                                if any(x in element for x in rechtsformen):
                                                    if len(element) <= 30:
                                                        firmalist.append(element)
                                            if len(element) >= 1 and type(element) == bs4.element.Tag:
                                                if any(x in element.get_text() for x in rechtsformen):
                                                    for c,element in enumerate(element):
                                                        #print("Ebene 5: " + str(c) + "/" + str(len(element)))
                                                        if len(element) >= 1 and type(element) == bs4.element.NavigableString:
                                                            if any(x in element for x in rechtsformen):
                                                                if len(element) <= 30:
                                                                    firmalist.append(element)
                                                        if len(element) >= 1 and type(element) == bs4.element.Tag:
                                                            if any(x in element.get_text() for x in rechtsformen):
                                                                for c,element in enumerate(element):
                                                                    if len(element) >= 1 and type(element) == bs4.element.NavigableString:
                                                                        if any(x in element for x in rechtsformen):
                                                                            if len(element) <= 30:
                                                                                firmalist.append(element)
                                                                    if len(element) >= 1 and type(element) == bs4.element.Tag:
                                                                        if any(x in element.get_text() for x in rechtsformen):
                                                                            #print("Ebene 6: " + str(c) + "/" + str(len(element)))
                                                                            #print(element)
                                                                            for c,element in enumerate(element):
                                                                                if len(element) >= 1 and type(element) == bs4.element.NavigableString:
                                                                                    if any(x in element for x in rechtsformen):
                                                                                        if len(element) <= 30:
                                                                                            firmalist.append(element)
                                                                                if len(element) >= 1 and type(element) == bs4.element.Tag:
                                                                                    if any(x in element.get_text() for x in rechtsformen):
                                                                                        # print("Ebene 7: " + str(c) + "/" + str(len(element)))
                                                                                        #print(element)
                                                                                        for c,element in enumerate(element):
                                                                                            if len(element) >= 1 and type(element) == bs4.element.NavigableString:
                                                                                                if any(x in element for x in rechtsformen):
                                                                                                    if len(element) <= 30:
                                                                                                        firmalist.append(element)
                                                                                            if len(element) >= 1 and type(element) == bs4.element.Tag:
                                                                                                if any(x in element.get_text() for x in rechtsformen):
                                                                                                    #print("Ebene 8: " + str(c) + "/" + str(len(element)))
                                                                                                    #print(element)
                                                                                                    for c,element in enumerate(element):
                                                                                                        if len(element) >= 1 and type(element) == bs4.element.NavigableString:
                                                                                                            if any(x in element for x in rechtsformen):
                                                                                                                #                                                                                                                print("Ebene 9: " + str(c) + "/" + str(len(element)))
                                                                                                                if len(element) <= 30:
                                                                                                                    firmalist.append(element)
                                                                                                                #                                                                                                                    print(element)
                                                                                                        if len(element) >= 1 and type(element) == bs4.element.Tag:
                                                                                                            #                                                                                                            print("Ebene 9: Tag")
                                                                                                            if any(x in element.get_text() for x in rechtsformen):
                                                                                                                for c,element in enumerate(element):
                                                                                                                    if len(element) >= 1 and type(element) == bs4.element.NavigableString:
                                                                                                                        if any(x in element for x in rechtsformen):
                                                                                                                            #                                                                                                                            print("Ebene 10: " + str(c) + "/" + str(len(element)))
                                                                                                                            if len(element) <= 30:
                                                                                                                                firmalist.append(element)
                                                                                                                            #                                                                                                                                print(element)
                                                                                                                    if len(element) >= 1 and type(element) == bs4.element.Tag:
                                                                                                                        #                                                                                                                        print("Ebene 10: Tag")
                                                                                                                        L2.append(element)
                                                                                                                        if any(x in element.get_text() for x in rechtsformen):
                                                                                                                            L2b.append(element)
                                                                                                                            for c,element in enumerate(element):
                                                                                                                                if len(element) >= 1 and type(element) == bs4.element.NavigableString:
                                                                                                                                    if any(x in element for x in rechtsformen):
                                                                                                                                        #                                                                                                                                        print("Ebene 11: " + str(c) + "/" + str(len(element)))
                                                                                                                                        if len(element) <= 30:
                                                                                                                                            firmalist.append(element)
                                                                                                                                        #                                                                                                                                            print(element)
                                                                                                                                if len(element) >= 1 and type(element) == bs4.element.Tag:
                                                                                                                                    #                                                                                                                                    print("Ebene 11: Tag" + str(element))
                                                                                                                                    if any(x in element.get_text() for x in rechtsformen):
                                                                                                                                        L3.append(element)
                                                                                                                                        for c,element in enumerate(element):
                                                                                                                                            #                                                                                                                                            print("Ebene 12: " + str(c) + "/" + str(len(element)))
                                                                                                                                            #                                                                                                                                            print(element)
                                                                                                                                            L4.append(element)

    #print(firmalist)
    if len(firmalist) == 0:
        return None
    else:
        unique,pos = np.unique(firmalist,return_inverse=True)
        counts = np.bincount(pos)
        maxpos = counts.argmax()
        firma = str(unique[maxpos]).replace('\n', '')
        # print(firma)
        return (firma)

