import requests
import re
from bs4 import BeautifulSoup
import sys
import time

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
