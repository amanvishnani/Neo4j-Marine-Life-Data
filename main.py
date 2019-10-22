from typing import Dict, List

from neo4j import GraphDatabase, basic_auth
from util import *

try:
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "root"))
    session = driver.session()
except Exception as e:
    print(e)
    print("DB Connection Failed")


base_url = 'https://oceana.ca';


def get_animal_details(url: str) -> Dict:
    animal_soup = get_soup(url)
    animal = dict()
    name = animal_soup.find("div", class_="subpage-header-inner").find("h1").get_text().strip()
    habitat = animal_soup.find("h2", string="Ecosystem/Habitat").find_next('p').get_text().strip()
    feeding_habits = animal_soup.find("h2", string="Feeding Habits").find_next('p').get_text().strip()
    conservation_status = animal_soup.find("h2", string="Conservation Status")
    if conservation_status is not None:
        conservation_status = conservation_status.find_next('p').get_text().strip()
    animal["name"] = name
    animal["habitat"] = habitat
    animal["feeding_habits"] = feeding_habits
    animal["conservation_status"] = conservation_status

    return animal


def get_all_animals() -> List[Dict]:
    animals = list()
    first_page = get_soup('{}/en/marine-life/canadian-marine-life-encyclopedia'.format(base_url))
    articles = first_page.find_all("article")
    for article in articles:
        article_url = article.find_next("a").get("href")
        animal = get_animal_details('{}{}'.format(base_url, article_url))
        animals.append(animal)
    return animals


marine_animals = get_all_animals()
print(marine_animals)