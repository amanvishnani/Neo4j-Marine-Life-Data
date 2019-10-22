from bs4 import BeautifulSoup
import urllib3

http = urllib3.PoolManager()

def get_soup(url) -> BeautifulSoup:
    r = http.request('GET', url)
    soup = BeautifulSoup(r.data.decode("utf-8"), features="html.parser")
    return soup
