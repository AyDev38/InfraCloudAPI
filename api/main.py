from typing import List
from fastapi import FastAPI, Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import repository as repository
import models as models
import schemas as schemas
from models import SessionLocal, engine
from utils import encrypt_data, decrypt_data

# Créer les tables dans la base de données
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuration de CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dépendance pour obtenir la session de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route pour lire tous les pays
@app.get("/countries", response_model=List[schemas.Country])
def read_countries(db: Session = Depends(get_db)):
    countries = repository.get_countries(db)
    return countries

# Route pour lire un pays par code et déchiffrer le PIB
@app.get("/countries/{code}", response_model=schemas.Country)
def read_country(code: str, db: Session = Depends(get_db)):
    country = repository.get_country(db, code)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

# Route pour créer un nouveau pays
@app.post("/countries", response_model=schemas.Country)
def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    new_country = repository.create_country(db=db, country=country)
    if new_country.pib:
        new_country.pib = decrypt_data(new_country.pib)
    return new_country


# Route pour mettre à jour un pays
@app.put("/countries/{code}", response_model=schemas.Country)
def update_country(code: str, country_update: schemas.CountryCreate, db: Session = Depends(get_db)):
    existing_country = repository.get_country(db, code)
    if not existing_country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    existing_country.code = country_update.code
    existing_country.continent_code = country_update.continent_code
    existing_country.latitude = country_update.latitude
    existing_country.longitude = country_update.longitude
    existing_country.name = country_update.name
    existing_country.nameEs = country_update.nameEs
    existing_country.nameFr = country_update.nameFr
    existing_country.nameNative = country_update.nameNative
    existing_country.population = country_update.population
    
    if country_update.pib:
        existing_country.pib = encrypt_data(country_update.pib)
    
    db.commit()
    db.refresh(existing_country)

    if existing_country.pib:
        existing_country.pib = decrypt_data(existing_country.pib)

    return existing_country



# Route pour supprimer un pays
@app.delete("/countries/{code}", response_model=schemas.Country)
def delete_country(code: str, db: Session = Depends(get_db)):
    country = repository.delete_country(db, code)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

# Route pour rechercher des pays par nom
@app.get("/countries/search/by-name", response_model=List[schemas.Country])
def search_countries_by_name(name: str, db: Session = Depends(get_db)):
    countries = db.query(models.Country).filter(models.Country.name.like(f"%{name}%")).all()
    if not countries:
        raise HTTPException(status_code=404, detail="No countries found with the given name")
    return countries

# Route pour rechercher des pays par code de continent
@app.get("/countries/search/by-continent-code", response_model=List[schemas.Country])
def search_countries_by_continent_code(continent_code: str, db: Session = Depends(get_db)):
    countries = repository.get_countries_by_continent(db, continent_code)
    if not countries:
        raise HTTPException(status_code=404, detail="No countries found in the given continent")
    return countries

# Route pour rechercher des pays par population supérieure à un chiffre donné
@app.get("/countries/search/by-population", response_model=List[schemas.Country])
def search_countries_by_population(min_population: int = Query(..., alias="minPopulation"), db: Session = Depends(get_db)):
    countries = repository.get_countries_by_population(db, min_population)
    if not countries:
        raise HTTPException(status_code=404, detail="No countries found with population greater than the given number")
    return countries


# Route pour inserer un pib dans un pays
@app.put("/countries/{code}/pib/{data}", response_model=schemas.Country)
def update_country_pib(code: str, data: int, db: Session = Depends(get_db)):
    existing_country = repository.get_country(db, code)
    if not existing_country:
        raise HTTPException(status_code=404, detail="Country not found")
    # Encryper la data
    data = encrypt_data(data)
    existing_country.pib = data
    
    db.commit()
    db.refresh(existing_country)
    return existing_country


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
            "GET /countries/search/by-population": "Search countries by population greater than a given number (query param: minPopulation)",
            "GET /continents/": "Read all continents",
            "GET /continents/{code}": "Read a continent by code"
        }
    }

# Router for continents
continent_router = APIRouter()

# Route to read a continent by code
@continent_router.get("/continents/{code}", response_model=schemas.Continent)
def read_continent(code: str, db: Session = Depends(get_db)):
    continent = repository.get_continent(db, code)
    for country in continent.countries:
        if country.pib:
            country.pib = decrypt_data(country.pib)
    if continent is None:
        raise HTTPException(status_code=404, detail="Continent not found")
    return continent

# Route to read all continents
@continent_router.get("/continents", response_model=List[schemas.Continent])
def read_continents(db: Session = Depends(get_db)):
    continents = repository.get_continents(db)
    for continent in continents:
        for country in continent.countries:
            if country.pib:
                country.pib = decrypt_data(country.pib)
    return continents

# Include continent_router in the main app
app.include_router(continent_router)