from neo4j import GraphDatabase, basic_auth
from utils import *
import networkx as nx


# not to use this
try:
    driver = GraphDatabase.driver("bolt://localhost:11002", auth=basic_auth("neo4j", "root"))
    session = driver.session()
    result = session.run("MATCH (a:Animal) WHERE a.conservtnStatus =~ '.*Endangered.*' return a")

    graph = result.get_graph()
    plt.figure(figsize=(6,4));
    nx.draw(g)
except Exception as e:
    print(e)
    print("DB Connection Failed")


