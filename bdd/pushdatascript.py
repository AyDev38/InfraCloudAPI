import json
import sqlite3
from pathlib import Path

# Chemin vers le fichier JSON
DATA_FILE = Path("C:/Users/Aymeric/Documents/LiveCampus/InfraCloud/Module3/bdd/countries_data.json")

# Charger les données JSON
with open(DATA_FILE, "r", encoding="utf-8") as file:
    countries_data = json.load(file)

# Connexion à la base de données SQLite
connection = sqlite3.connect('countries.db')
cursor = connection.cursor()

# Créer les tables si elles n'existent pas déjà
cursor.execute('''
CREATE TABLE IF NOT EXISTS continents (
    code TEXT PRIMARY KEY,
    latitude TEXT,
    longitude TEXT,
    name TEXT,
    nameEs TEXT,
    nameFr TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS countries (
    code TEXT PRIMARY KEY,
    continent_code TEXT,
    latitude TEXT,
    longitude TEXT,
    name TEXT,
    nameEs TEXT,
    nameFr TEXT,
    nameNative TEXT,
    population INTEGER,
    FOREIGN KEY (continent_code) REFERENCES continents (code)
)
''')

# Insérer les données dans la table continents
continent_codes = set()
for country in countries_data:
    continent = country["continent"]
    if continent["code"] not in continent_codes:
        continent_codes.add(continent["code"])
        cursor.execute(
            "INSERT INTO continents (code, latitude, longitude, name, nameEs, nameFr) VALUES (?, ?, ?, ?, ?, ?)",
            (continent["code"], continent["latitude"], continent["longitude"], continent["name"], continent["nameEs"], continent["nameFr"])
        )

# Insérer les données dans la table countries
for country in countries_data:
    cursor.execute(
        "INSERT INTO countries (code, continent_code, latitude, longitude, name, nameEs, nameFr, nameNative, population) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (country["code"], country["continent"]["code"], country["latitude"], country["longitude"], country["name"], country["nameEs"], country["nameFr"], json.dumps(country["nameNative"]), country["population"])
    )

# Commit des transactions et fermer la connexion
connection.commit()
connection.close()
