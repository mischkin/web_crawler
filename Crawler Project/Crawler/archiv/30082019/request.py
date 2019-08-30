import requests
import re
from bs4 import BeautifulSoup

def get_soup(url):
    count = {}
    count[0] = 1
    try:                                            # könnte auch Session einführen
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    if re.findall("Zu viele Abfragen", soup.get_text()) and count[0] <= 3:  # Spam Ausnahme
        time.sleep(10)
        print("10 Sekunden Pause, dann retry")
        get_soup(url)
        count[0] = count[0] +1
    return soup
