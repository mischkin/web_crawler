# Ziel2: Zufällige Seite als Input --> Entscheidung ob es in Kategorie fällt (startups)

#
#
#
#
#
#
#


def get_words(url, source):
    if source == "impressum":
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


