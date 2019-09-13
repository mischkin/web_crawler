# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 16:04:46 2019

@author: admin
"""


import requests
import re
from bs4 import BeautifulSoup
import bs4
import sys
import time

#url = "https://www.matchachin.com/impressum/"
url = "https://www.bioforpets.de/legal-disclosure/"
#url = "https://www.matchachin.com/"

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


soup = get_soup(url)
text = soup.find_all(text=True)
div = soup.find_all('div')


def get_words(soup):
    div = soup.find_all("div")
    all_words = []
    iterations = {}
    iterations[1] = 1
    for c,element in enumerate(div):
        wordlist = []
        new_words = element_loop_1(element, wordlist)
        all_words.append(new_words)
    all_words = [item for sublist in all_words for item in sublist]
    return all_words





def element_loop_1(Element, wordlist):
    wordlist = wordlist
    elementlist = []
    for element in Element:
        if type(element) == bs4.element.NavigableString:
            if len(element) >= 1:
                wordlist.append(element)
        if type(element) == bs4.element.Tag:
            if len(element) >= 1:
                elementlist.append(element)
    neue_wordlist = element_loop_2(elementlist, wordlist)
    return neue_wordlist


def element_loop_2(elementlist, wordlist, limit = 0):
    #    print(wordlist)
    wordlist = wordlist
    if limit >= 100:
        print("=============================== LIMIT ==========================02)
        return wordlist
    limit += 1
    #    print(limit)
    neue_elementliste = []
    for listelement in elementlist:
        for c,element in enumerate(listelement):
            if type(element) == bs4.element.NavigableString:
                if len(element) >= 1:
                    wordlist.append(element)
            if type(element) == bs4.element.Tag:
                if len(neue_elementliste) >= 1:
                    neue_elementliste.append(element)
        return element_loop_2(neue_elementliste, wordlist, limit)
    else:
        return wordlist


words = get_words(soup)
