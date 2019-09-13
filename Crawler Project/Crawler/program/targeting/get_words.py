# Ziel2: Zufällige Seite als Input --> Entscheidung ob es in Kategorie fällt (startups)
import bs4


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
            if len(element.strip()) >= 1:
                wordlist.append(element)
        if type(element) == bs4.element.Tag:
            if len(element.strip()) >= 1:
                elementlist.append(element)
    neue_wordlist = element_loop_2(elementlist, wordlist)
    return neue_wordlist


def element_loop_2(elementlist, wordlist, limit = 0):
    #    print(wordlist)
    wordlist = wordlist
    if limit >= 100:
        return wordlist
    limit += 1
    #    print(limit)
    neue_elementliste = []
    for listelement in elementlist:
        for c,element in enumerate(listelement):
            if type(element) == bs4.element.NavigableString:
                if len(element.strip()) >= 1:
                    wordlist.append(element)
            if type(element) == bs4.element.Tag:
                if len(neue_elementliste) >= 1:
                    neue_elementliste.append(element)
        return element_loop_2(neue_elementliste, wordlist, limit)
    else:
        return wordlist


# def get_nltk(urllist):
#     for url in urllist:
#         text = soup.find_all(text=True)
#         text = []
#         for item in text_html:
#             text.append(item.get_text())
#         text_string = ''.join(text)
#         tokenizer = RegexpTokenizer('\w+')
#         tokens = tokenizer.tokenize(text_string)
#         words = []
#         for word in tokens:
#             words.append(word.lower())
#         sw = nltk.corpus.stopwords.words('english') # all words that are not stopwordsr = requests.get
#         words_ns = []
#         for word in words:
#             if word not in sw:
#                 words_ns.append(word.lower())
#         return words_ns


