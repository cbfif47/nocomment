#these are for scraping
from lxml import html
from urllib.parse import urlparse
import requests


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