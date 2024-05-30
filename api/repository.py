from sqlalchemy.orm import Session
import models as models
import schemas as schemas

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
    db_country = models.Country(**country.dict())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

def get_country(db: Session, code: str):
    return db.query(models.Country).filter(models.Country.code == code).first()

def get_countries(db: Session):
    return db.query(models.Country).all()

def get_countries_by_continent(db: Session, continent_code: str):
    return db.query(models.Country).filter(models.Country.continent_code == continent_code).all()

def get_countries_by_population(db: Session, min_population: int):
    return db.query(models.Country).filter(models.Country.population > min_population).all()

def delete_country(db: Session, code: str):
    db_country = db.query(models.Country).filter(models.Country.code == code).first()
    if db_country:
        db.delete(db_country)
        db.commit()
    return db_country
