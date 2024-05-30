from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
from pathlib import Path

# Crée une instance de l'application FastAPI
app = FastAPI()

# Chemin vers le fichier JSON
DATA_FILE = Path("countries_data.json")

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
    continent: Continent
    latitude: str
    longitude: str
    name: str
    nameEs: str
    nameFr: str
    nameNative: str
    population: int

# Initialiser le fichier JSON si vide ou inexistant
def initialize_data_file():
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)

# Fonction pour charger les données du fichier JSON
def load_data() -> List[Country]:
    initialize_data_file()
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        countries_raw = json.load(file)
        return [Country(**country) for country in countries_raw]

# Fonction pour sauvegarder les données dans le fichier JSON
def save_data(countries: List[Country]):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump([country.dict() for country in countries], file, ensure_ascii=False, indent=4)

# Charger les données initiales
countries_db: List[Country] = load_data()

# Route pour lire tous les pays
@app.get("/countries", response_model=List[Country])
def read_countries():
    return countries_db

# Route pour lire un pays par code
@app.get("/countries/{code}", response_model=Country)
def read_country(code: str):
    country = next((c for c in countries_db if c.code == code), None)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

# Route pour créer un nouveau pays
@app.post("/countries", response_model=Country)
def create_country(country: Country):
    new_country = Country(
        code=country.code,
        continent=country.continent,
        latitude=country.latitude,
        longitude=country.longitude,
        name=country.name,
        nameEs=country.nameEs,
        nameFr=country.nameFr,
        nameNative=country.nameNative,
        population=country.population
    )
    countries_db.append(new_country)
    save_data(countries_db)
    return new_country

# Route pour mettre à jour un pays
@app.put("/countries/{code}", response_model=Country)
def update_country(code: str, country_update: Country):
    existing_country = next((c for c in countries_db if c.code == code), None)
    if existing_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    
    # Vérifiez si le nouveau code existe déjà dans la base de données
    if code != country_update.code and any(c for c in countries_db if c.code == country_update.code):
        raise HTTPException(status_code=400, detail="New country code already exists")
    
    existing_country.code = country_update.code
    existing_country.continent = country_update.continent
    existing_country.latitude = country_update.latitude
    existing_country.longitude = country_update.longitude
    existing_country.name = country_update.name
    existing_country.nameEs = country_update.nameEs
    existing_country.nameFr = country_update.nameFr
    existing_country.nameNative = country_update.nameNative
    existing_country.population = country_update.population
    
    save_data(countries_db)
    return existing_country

# Route pour supprimer un pays
@app.delete("/countries/{code}", response_model=Country)
def delete_country(code: str):
    global countries_db
    country = next((c for c in countries_db if c.code == code), None)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    countries_db = [c for c in countries_db if c.code != code]
    save_data(countries_db)
    return country

# Route pour rechercher des pays par nom
@app.get("/countries/search/by-name", response_model=List[Country])
def search_countries_by_name(name: str):
    results = [country for country in countries_db if name.lower() in country.name.lower()]
    if not results:
        raise HTTPException(status_code=404, detail="No countries found with the given name")
    return results

# Route pour rechercher des pays par code de continent
@app.get("/countries/search/by-continent-code", response_model=List[Country])
def search_countries_by_continent_code(continent_code: str):
    results = [country for country in countries_db if country.continent.code == continent_code]
    if not results:
        raise HTTPException(status_code=404, detail="No countries found in the given continent")
    return results

# Route pour rechercher des pays par nom de continent
@app.get("/countries/search/by-continent-name", response_model=List[Country])
def search_countries_by_continent_name(continent_name: str):
    results = [country for country in countries_db if country.continent.name.lower() == continent_name.lower()]
    if not results:
        raise HTTPException(status_code=404, detail="No countries found in the given continent")
    return results

# Route pour rechercher des pays par population supérieure à un chiffre donné
@app.get("/countries/search/by-population", response_model=List[Country])
def search_countries_by_population(min_population: int = Query(..., alias="minPopulation")):
    results = [country for country in countries_db if country.population > min_population]
    if not results:
        raise HTTPException(status_code=404, detail="No countries found with population greater than the given number")
    return results

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
            "GET /countries/search/by-continent-name": "Search countries by continent name (query param: continent_name)",
            "GET /countries/search/by-population": "Search countries by population greater than a given number (query param: minPopulation)"
        }
    }
