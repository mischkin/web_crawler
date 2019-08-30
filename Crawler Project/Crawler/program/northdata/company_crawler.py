from request import get_soup

def company_crawler(url): # exports a Dic of all subsites in website
    website_links_list = []
    print(url)
    RawCompanyLinks = GetLinks(url)
    WebsiteLinks = GetWebsiteLinks(url, RawCompanyLinks)
    website_links_list = WebsiteLinks
    #print(website_links_list[company])
    return website_links_list


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

def GetWebsiteLinks(Startseite, urls):
    WebsiteLinks = []
    StartseiteVariations = GetUrlVariations(Startseite)
    for link in urls:
        if any(Startseite in link for Startseite in StartseiteVariations):
            WebsiteLinks.append(link)
    return WebsiteLinks

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

