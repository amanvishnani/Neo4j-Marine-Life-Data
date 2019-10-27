from typing import Dict, List
from bs4 import BeautifulSoup
import requests
from neo4j import GraphDatabase, basic_auth
from utils import *

try:
    driver = GraphDatabase.driver("bolt://localhost:11002", auth=basic_auth("neo4j", "root"))
    session = driver.session()
except Exception as e:
    print(e)
    print("DB Connection Failed")

base_url = 'https://oceana.ca';
def get_soup(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_animal_details(url: str) -> Dict:
    animal_soup = get_soup(url)
    animal = dict()
    name = animal_soup.find("div", class_="subpage-header-inner").find("h1").get_text().strip()
    habitat = animal_soup.find("h2", string="Ecosystem/Habitat").find_next('p').get_text().strip()
    feeding_habits = animal_soup.find("h2", string="Feeding Habits").find_next('p').get_text().strip()
    conservation_status = animal_soup.find("h2", string="Conservation Status")
    if conservation_status is not None:
        conservation_status = conservation_status.find_next('p').get_text().strip()
    if conservation_status is None:
        conservation_status = "NA"
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

def createNode(m_animal):
    createQry = "CREATE(`"+ m_animal['name'] +"`:Animal{name:'"+m_animal['name']+"', habitat:'" + m_animal['habitat']+"', conservtnStatus:'"+ m_animal['conservation_status']+"'})"
    return createQry

# ################## MAIN #######################

# Get all Animals
marine_animals = get_all_animals()
# Process all Animals
cqlCreate = ""
relationshipCql = ""
for m_animal in marine_animals:
  # cqlCreate += createNode(m_animal)
  # relationshipCql += "CREATE (`"+ m_animal['name']+"`)-[:Identical_Feeding_habits]->(`"+m_animal['feeding_habits']+"`)"

  # Create Animal node
  session.run(createNode(m_animal))
  
  # Create feeding habit node 
  session.run("MERGE (`"+ m_animal['feeding_habits']+"`:feeding_habits{name:'"+m_animal['feeding_habits']+"'})") 

  # Create relationship with animal node and feeding habit node
  session.run("MATCH (a:Animal),(b:feeding_habits) WHERE a.name = '"+ m_animal['name']+"' and b.name = '"+m_animal['feeding_habits']+"' CREATE (a)-[:Identical_Feeding_habits]->(b)")

#Relationship with animal nodes with same habitats and delete self relationships
session.run("MATCH (a:Animal), (b:Animal) WHERE a.habitat = b.habitat create (a)-[relationship:neighbor]->(b)")
session.run("MATCH (a:Animal)-[relationship:neighbor]->(a) delete relationship")
print("done")
