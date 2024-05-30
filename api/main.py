from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

# Crée une instance de l'application FastAPI
app = FastAPI()

# Configuration de CORS
origins = [
    "http://localhost:3000",  # Remplacez par les origines que vous souhaitez autoriser
    "http://127.0.0.1:3000",
    # Ajoutez d'autres origines si nécessaire
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les en-têtes
)

# Modèles de données
class Continent(BaseModel):
    code: str
    latitude: str
    longitude: str
    name: str
    nameEs: str
    nameFr: str

class Country(BaseModel):
    code: str
    continent_code: str
    latitude: str
    longitude: str
    name: str
    nameEs: str
    nameFr: str
    nameNative: str
    population: int

# Fonction pour obtenir une connexion à la base de données
def get_db_connection():
    connection = sqlite3.connect('../bdd/countries.db')
    connection.row_factory = sqlite3.Row
    return connection

# Route pour lire tous les pays
@app.get("/countries", response_model=List[Country])
def read_countries():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM countries")
    countries = cursor.fetchall()
    connection.close()
    return [Country(**dict(country)) for country in countries]

# Route pour lire un pays par code
@app.get("/countries/{code}", response_model=Country)
def read_country(code: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM countries WHERE code = ?", (code,))
    country = cursor.fetchone()
    connection.close()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return Country(**dict(country))

# Route pour créer un nouveau pays
@app.post("/countries", response_model=Country)
def create_country(country: Country):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO countries (code, continent_code, latitude, longitude, name, nameEs, nameFr, nameNative, population) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (country.code, country.continent_code, country.latitude, country.longitude, country.name, country.nameEs, country.nameFr, country.nameNative, country.population)
    )
    connection.commit()
    connection.close()
    return country

# Route pour mettre à jour un pays
@app.put("/countries/{code}", response_model=Country)
def update_country(code: str, country_update: Country):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE countries SET code = ?, continent_code = ?, latitude = ?, longitude = ?, name = ?, nameEs = ?, nameFr = ?, nameNative = ?, population = ? WHERE code = ?",
        (country_update.code, country_update.continent_code, country_update.latitude, country_update.longitude, country_update.name, country_update.nameEs, country_update.nameFr, country_update.nameNative, country_update.population, code)
    )
    connection.commit()
    connection.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Country not found")
    return country_update

# Route pour supprimer un pays
@app.delete("/countries/{code}", response_model=Country)
def delete_country(code: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM countries WHERE code = ?", (code,))
    connection.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Country not found")
    connection.close()
    return {"detail": "Country deleted"}

# Route pour rechercher des pays par nom
@app.get("/countries/search/by-name", response_model=List[Country])
def search_countries_by_name(name: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM countries WHERE name LIKE ?", ('%' + name + '%',))
    countries = cursor.fetchall()
    connection.close()
    if not countries:
        raise HTTPException(status_code=404, detail="No countries found with the given name")
    return [Country(**dict(country)) for country in countries]

# Route pour rechercher des pays par code de continent
@app.get("/countries/search/by-continent-code", response_model=List[Country])
def search_countries_by_continent_code(continent_code: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM countries WHERE continent_code = ?", (continent_code,))
    countries = cursor.fetchall()
    connection.close()
    if not countries:
        raise HTTPException(status_code=404, detail="No countries found in the given continent")
    return [Country(**dict(country)) for country in countries]

# Route pour rechercher des pays par population supérieure à un chiffre donné
@app.get("/countries/search/by-population", response_model=List[Country])
def search_countries_by_population(min_population: int = Query(..., alias="minPopulation")):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM countries WHERE population > ?", (min_population,))
    countries = cursor.fetchall()
    connection.close()
    if not countries:
        raise HTTPException(status_code=404, detail="No countries found with population greater than the given number")
    return [Country(**dict(country)) for country in countries]

# Définition d'une route GET de base avec les différentes commandes de l'API
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Countries API",
        "endpoints": {
            "GET /countries": "Read all countries",
            "GET /countries/{code}": "Read a country by code",
            "POST /countries": "Create a new country",
            "PUT /countries/{code}": "Update a country by code",
            "DELETE /countries/{code}": "Delete a country by code",
            "GET /countries/search/by-name": "Search countries by name (query param: name)",
            "GET /countries/search/by-continent-code": "Search countries by continent code (query param: continent_code)",
            "GET /countries/search/by-population": "Search countries by population greater than a given number (query param: minPopulation)"
        }
    }
