from pydantic import BaseModel
from typing import List

class ContinentBase(BaseModel):
    code: str
    latitude: str
    longitude: str
    name: str
    nameEs: str
    nameFr: str

class ContinentCreate(ContinentBase):
    pass

class Continent(ContinentBase):
    countries: List['Country'] = []

    class Config:
        orm_mode = True

class CountryBase(BaseModel):
    code: str
    continent_code: str
    latitude: str
    longitude: str
    name: str
    nameEs: str
    nameFr: str
    nameNative: str
    population: int

class CountryCreate(CountryBase):
    pass

class Country(CountryBase):
    class Config:
        orm_mode = True
