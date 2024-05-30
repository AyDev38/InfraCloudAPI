import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
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

def test_create_country():
    response = client.post("/countries", json={
        "code": "jp",
        "continent": {
            "code": "as",
            "latitude": "35.652832",
            "longitude": "139.839478",
            "name": "Asia",
            "nameEs": "Asia",
            "nameFr": "Asie"
        },
        "latitude": "35.652832",
        "longitude": "139.839478",
        "name": "Japan",
        "nameEs": "Japón",
        "nameFr": "Japon",
        "nameNative": "日本",
        "population": 125800000
    })
    assert response.status_code == 200
    assert response.json()["code"] == "jp"

