document.getElementById('getAllCountries').addEventListener('click', async () => {
    const response = await fetch('http://localhost:8000/countries');
    const data = await response.json();
    document.getElementById('allCountriesResult').textContent = JSON.stringify(data, null, 2);
});

document.getElementById('getCountryByCode').addEventListener('click', async () => {
    const code = document.getElementById('countryCode').value;
    const response = await fetch(`http://localhost:8000/countries/${code}`);
    const data = await response.json();
    document.getElementById('countryByCodeResult').textContent = JSON.stringify(data, null, 2);
});

document.getElementById('createCountryForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const newCountry = {
        code: document.getElementById('newCountryCode').value,
        name: document.getElementById('newCountryName').value,
        continent: {
            code: document.getElementById('newCountryContinentCode').value,
            name: document.getElementById('newCountryName').value,
            latitude: document.getElementById('newCountryLatitude').value,
            longitude: document.getElementById('newCountryLongitude').value,
            nameEs: document.getElementById('newCountryNameEs').value,
            nameFr: document.getElementById('newCountryNameFr').value
        },
        latitude: document.getElementById('newCountryLatitude').value,
        longitude: document.getElementById('newCountryLongitude').value,
        nameEs: document.getElementById('newCountryNameEs').value,
        nameFr: document.getElementById('newCountryNameFr').value,
        nameNative: document.getElementById('newCountryNameNative').value,
        population: document.getElementById('newCountryPopulation').value
    };
    const response = await fetch('http://localhost:8000/countries', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newCountry)
    });
    const data = await response.json();
    document.getElementById('createCountryResult').textContent = JSON.stringify(data, null, 2);
});
