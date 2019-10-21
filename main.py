from neo4j import GraphDatabase, basic_auth
from bs4 import BeautifulSoup
import urllib3

http = urllib3.PoolManager()
driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "root"))
session = driver.session()


def get_soup(url) -> BeautifulSoup:
    r = http.request('GET', url)
    soup = BeautifulSoup(r.data.decode("utf-8"), features="html.parser")
    return soup


def get_animal_details(url: str):
    pass


first_page = get_soup('https://oceana.ca/en/marine-life/canadian-marine-life-encyclopedia')
articles = first_page.find_all("article")
for article in articles:
    article_url = article.find_next("a")
    print(article_url)

