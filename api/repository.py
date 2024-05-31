from sqlalchemy.orm import Session
import models as models
import schemas as schemas
from utils import encrypt_data, decrypt_data

# Fonctions CRUD pour Continent
def create_continent(db: Session, continent: schemas.ContinentCreate):
    db_continent = models.Continent(**continent.dict())
    db.add(db_continent)
    db.commit()
    db.refresh(db_continent)
    return db_continent

def get_continent(db: Session, code: str):
    return db.query(models.Continent).filter(models.Continent.code == code).first()

def get_continents(db: Session):
    return db.query(models.Continent).all()

# Fonctions CRUD pour Country
def create_country(db: Session, country: schemas.CountryCreate):
    # Chiffrer la valeur du PIB avant de la stocker
    if country.pib:
        country.pib = encrypt_data(country.pib)
    db_country = models.Country(**country.dict())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

def get_country(db: Session, code: str):
    db_country = db.query(models.Country).filter(models.Country.code == code).first()
    if db_country and db_country.pib:
        # Déchiffrer la valeur du PIB avant de la retourner
        db_country.pib = decrypt_data(db_country.pib)
    return db_country

def get_countries(db: Session):
    countries = db.query(models.Country).all()
    for country in countries:
        if country.pib:
            country.pib = decrypt_data(country.pib)
    return countries

def get_countries_by_continent(db: Session, continent_code: str):
    countries = db.query(models.Country).filter(models.Country.continent_code == continent_code).all()
    for country in countries:
        if country.pib:
            country.pib = decrypt_data(country.pib)
    return countries

def get_countries_by_population(db: Session, min_population: int):
    countries = db.query(models.Country).filter(models.Country.population > min_population).all()
    for country in countries:
        if country.pib:
            country.pib = decrypt_data(country.pib)
    return countries

def delete_country(db: Session, code: str):
    db_country = db.query(models.Country).filter(models.Country.code == code).first()
    if db_country:
        db.delete(db_country)
        db.commit()
    return db_country

def get_symmetric_key(db: Session):
    return db.query(models.EncryptKey).first().key
