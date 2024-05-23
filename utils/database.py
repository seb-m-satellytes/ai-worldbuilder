import os
from dotenv import load_dotenv
from neo4j import GraphDatabase, basic_auth

load_dotenv()

username = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv(
    "NEO4J_PASSWORD", "")
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
database = os.getenv("NEO4J_DATABASE", "neo4j")
driver = GraphDatabase.driver(URI, auth=basic_auth(username, password))
