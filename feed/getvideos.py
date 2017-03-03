#these are for scraping
from lxml import html
from urllib.parse import urlparse
import requests
import shelve
import sys
import feedparser
import ssl 

##### Here's how we get the vids

def find_youtubes(address):
    """finds any embedded youtube addresses on the page"""
    page = requests.get(address)
    output = set()
    try:
        tree = html.fromstring(page.text)
        sources = tree.xpath('//a/@href')
        for source in sources:
            if "youtube.com" in source:
                parsed = urlparse(str(source))
                output.add(source)
    except html.etree.ParserError:
        pass
    return output
    

def get_sub_pages(mainaddress, domain, allowed_paths):
    """get address of all links from address along allowed paths, in domain"""
    page = requests.get(mainaddress, allow_redirects=False)
    tree = html.fromstring(page.text)
    links = tree.xpath('//attribute::href')
    output = []
    for link in links:
        parsed = urlparse(link)
        path = parsed.path.split('/')
        if (parsed.netloc == domain and len(path) >1 and path[1] in allowed_paths):
            output.append(link)
    return output

def get_rss_links(mainaddress):
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    dd = feedparser.parse(mainaddress)
    output = []
    for d in dd.entries: 
        output.append(d.link)
    return output

def catch_em_all(source):
    if source == 'stereogum':
        links = get_sub_pages('http://www.stereogum.com','www.stereogum.com',[str(x) for x in range(1920000, 1930000)])
    if source == 'slate':
        links = get_sub_pages('http://www.slate.com','www.slate.com',['articles', 'blogs'])
    if source == 'noisey':
        links = get_rss_links('http://noisey.vice.com/en_ca/rss')  
    youtubes = []
    for link in links:
        youtubes += find_youtubes(link)
    distinct = set()
    for youtube in youtubes:
        if source not in youtube:    #make sure we're not adding its own channel
            distinct.add(youtube)
    return distinct