from program.request import get_soup


def GetLinks(url):
    RawLinks = []
    soup = get_soup(url)
    links_html = soup.find_all('a')
    for link_html in links_html:
        link = str(link_html.get('href'))
        if len(link) >= 4:
            if link[0:4] == 'http':
                RawLinks.append(link)
    RawLinks = list(set(RawLinks))
    #print(RawLinks)
    return RawLinks

def GetRegExpr(url):
    pos1 = 'http://www.'
    reg1 = 'http://[\w-]+\.[\w-]+\.[\w-]+'
    pos2 = 'https://www.'
    reg2 = 'https://[\w-]+\.[\w-]+\.[\w-]+'
    pos3 = 'http://'
    reg3 = 'http://[\w-]+\.[\w-]+'
    pos4 = 'https://'
    reg4 = 'https://[\w-]+\.[\w-]+'
    if url[0:11] == pos1:
        return(reg1, pos1)
    if url[0:12] == pos2:
        return(reg2, pos2)
    if url[0:7] == pos3 and url[0:11] != pos1:
        return(reg3, pos3)
    if url[0:8] == pos4 and url[0:12] != pos2:
        return(reg4, pos4)
    else:
        return(None, None)

def GetUrlVariations(url):
    UrlVariations = []
    UrlVariations.append(url)
    if GetRegExpr(url)[1] == 'http://www.':
        UrlVariations.append(url.split('http://')[0] + url.split('www.')[1])
    if GetRegExpr(url)[1] == 'http://':
        UrlVariations.append(url.split('http://')[0] + 'www.' + url.split('http://')[1])
    if url[-1] != '/':
        UrlVariations.append(url + '/')
    if url[-1] == '/':
        UrlVariations.append(url[0:-1])
    return UrlVariations


def GetCategoryLinks(url):
    CatLinks = []
    RawLinks = GetLinks(url)
    for c,link in enumerate(RawLinks):
        print("{}/{} RawLinks".format(c,len(RawLinks)))
        if link.find('wpbdp_category') != -1:
            CatLinks.append(link)
    CatLinks = list(set(CatLinks))
    return CatLinks

def GetWebsiteLinks(Startseite, urls):
    WebsiteLinks = []
    StartseiteVariations = GetUrlVariations(Startseite)
    for link in urls:
        if any(Startseite in link for Startseite in StartseiteVariations):
            WebsiteLinks.append(link)
    return WebsiteLinks


def GetStartseiteLinks(url):
    StartLinks = []
    RawLinks = GetLinks(url)
    for c,link in enumerate(RawLinks):
        print("{}/{} RawLinks".format(c,len(RawLinks)))
        regexp = GetRegExpr(str(link))[0]
        #print("regex: " + str(regexp))
        if regexp != None:
            reg = re.findall(regexp, link)
            if len(reg) >= 1:
                print(str(link) + " vs " + str(reg[0]))
                if str(link) == str(reg[0]) or str(link) == str(reg[0] + "/"):
                    StartLinks.append(link)
    print("vorher" + str(StartLinks))
    StartLinks = list(set(StartLinks))
    print("nachher" + str(StartLinks))
    return StartLinks


def cat_crawler(url):
    # Dic mit allen Links
    LinkDic = {}
    # Startup Urls sammeln
    print("===================================")
    print("get all category links")
    print("===================================")

    CatLinks = GetCategoryLinks(url)
    # Startseiten Urls sammeln
    print("===================================")
    print("get Startseite Links for each category Link")
    print("===================================")
    for c,catlink in enumerate(CatLinks):
        print("{}/{} CatLinks".format(c,len(CatLinks)))
        print("\ngetting Starseite Links for {}\n".format(catlink))
        StartLinks = GetStartseiteLinks(catlink)
        print("Liste für: " + str(catlink) + str(StartLinks))
        LinkDic[catlink] = StartLinks
    LinkList = [item for sublist in list(LinkDic.values()) for item in sublist]
    return LinkDic, LinkList

def company_crawler(url): # exports a Dic of all subsites in website
    WebsiteLinksDic = {}
    print(url)
    RawCompanyLinks = GetLinks(url)
    WebsiteLinks = GetWebsiteLinks(url, RawCompanyLinks)
    WebsiteLinksDic[url] = WebsiteLinks
    #print(WebsiteLinksDic[company])
    return WebsiteLinksDic

