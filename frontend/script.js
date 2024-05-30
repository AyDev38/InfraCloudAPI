import axios from 'axios';

document.getElementById('getAllCountries').addEventListener('click', async () => {
    try {
        const response = await axios.get('http://localhost:8000/countries');
        const data = response.data;
        console.log(data);
        document.getElementById('allCountriesResult').textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error(error);
    }
});

document.getElementById('getCountryByCode').addEventListener('click', async () => {
    const code = document.getElementById('countryCode').value;
    try {
        const response = await axios.get(`http://localhost:8000/countries/${code}`);
        const data = response.data;
        document.getElementById('countryByCodeResult').textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error(error);
    }
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
    try {
        const response = await axios.post('http://localhost:8000/countries', newCountry, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = response.data;
        document.getElementById('createCountryResult').textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error(error);
    }
});
