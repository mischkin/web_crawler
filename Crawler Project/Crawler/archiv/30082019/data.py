from program.request import get_soup
from program.get_values import get_firma, get_telefon, get_email

def get_words(url, source):

    if source == "northdata":
        get_words.soup_north = get_soup(url)
        # Block
        soup = get_words.soup_north
        data_dic = {}
        div_1 = soup.find_all("dv", iclass_ = "column")[2].find_all("p")
        keys_1 = ["Name", "Handelsregister", "Adresse", "Gegenstand"]
        for i in range(0,len(keys_1)):
            text = div_1[i].get_text().strip()
            data_dic[keys_1[i]] = text

        data_dic["owner"] = get_owner()
        data_dic["foundation"] = get_foundation()
        #print(" ========== " + str(data_dic["foundation"]))
        # Historie

        #        history_list = []
        #        for c,element in enumerate(div_2): # Zeiten müssen noch chronologisch geordnet werden
        #            event = element["text"]
        #            time = element["time"]
        #            history_list.append(time)
        #            history_list.append(event)
        #        # Jahresabschluss
        #        div_3 = json.loads(soup.find_all("div", class_ = "drill-downs charts ui grey segment")[0].find_all("div", class_ = "tab-content")[0].get("data-data"))
        #        # Bilanzsumme
        #        div_4 = json.loads(soup.find_all("div", class_ = "tab-content has-bar-charts")[0].get("data-data").strip().replace("\n", "").replace("false", '"false"'))
        return(data_dic) #, div_2, div_3, div_4
    elif source == "impressum":
        rechtsformen = [" GmbH "] #, " GmbH ", " GbR ", " OHG ", " KG ", " AG ", " GmbH & Co KG "]
        firma = []
        #for elem in soup(text=re.compile('.+?(?={})'.format(rechtsformen))): #'/^(.*?){}/'
        #firma.append(elem)
        elemlist = ["platzhalter"]
        for c,elem in enumerate(soup.find_all("div")):
            #print(c)
            elemlist[0] = elem
            elem2 = elem.find_all("div")
            for elem2a in elem2:
                try:
                    if any(x in elem2a.get_text() for x in rechtsformen):
                        elemlist[0] = elem2
                        elem3 = elem2.find_all("div")
                        for elem3a in elem3:
                            try:
                                if any(x in elem3a.get_text() for x in rechtsformen):
                                    elemlist[0] = elem3
                                else:
                                    continue
                            except(TypeError, AttributeError):
                                print("TypeError")
                    else:
                        continue
                except(TypeError, AttributeError):
                    print("TypeError")
            #print(elemlist)
            try:
                if any(x in elemlist[0].get_text() for x in rechtsformen):
                    firma.append(re.findall('.+?(?={})'.format(rechtsformen), elemlist[0].get_text()))
                else:
                    continue
            except(TypeError, AttributeError):
                print("TypeError")
        #print("firma name LISTE ist: " + str(    ))
        firma = str(firma[0])
        print("firma name ist: " + str(firma))
        return firma
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






def north_data(company_name):
    base_url = "https://www.northdata.de/"
    name_split = company_name.split(" ")
    name_split_string = [""]
    for i in range(0,len(name_split)):
        name_split_string[0] = str(name_split_string[0])  + str(name_split[i]) + "+"
    name_split_string[0] = name_split_string[0][:-1]
    search_url = str(base_url) + str(name_split_string[0])
    print(search_url)
    north_dic = get_words(search_url, "northdata")
    return north_dic

def get_impressum_soup(WebsiteLinksDic):
    soup = []
    for company in WebsiteLinksDic:
        for link in WebsiteLinksDic[company]:
            if "impressum" in link.lower():
                soup.append(get_soup(link))
    return soup[0]


def get_data(WebsiteLinksDic, soup_impressum):
    Word_Dic = {}
    for c,company in enumerate(WebsiteLinksDic): # für jede company
        print(company + " beginnt: " + str(c) + "/" + str(len(WebsiteLinksDic)))
        Word_Dic[company] = {}
        for c,link in enumerate(WebsiteLinksDic[company]):  # für jede Seite einer Website
            print(str(c)+ "/" + str(len(WebsiteLinksDic[company])))
            print(link)
            if "impressum" in link.lower():
                Word_Dic[company]["firma"] = {}
                Word_Dic[company]["firma"] = get_firma(soup_impressum)
                Word_Dic[company]["telefon"] = {}
                Word_Dic[company]["telefon"] = get_telefon(soup_impressum)
                Word_Dic[company]["email"] = {}
                Word_Dic[company]["email"] = get_email(soup_impressum)
            else:
                continue
        #                Word_Dic[company][link] = get_words(link, "anystring")                  ## AKTIVIEREN für alle Worte
        Word_Dic[company]["northdata"] = {}
        #print("northdata url: " + str(north_data(Word_Dic[company]["firma"])))
        Word_Dic[company]["northdata"] = north_data(Word_Dic[company]["firma"])
        print(company + " fertig ")
    return(Word_Dic)

