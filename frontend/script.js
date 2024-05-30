document.getElementById('getAllCountries').addEventListener('click', async () => {
    try {
        const response = await axios.get('http://localhost:8000/countries');
        const countries = response.data;
        const resultContainer = document.getElementById('allCountriesResult');
        resultContainer.innerHTML = '';

        countries.forEach(country => {

            const continentName = country.continent?.name || 'N/A';
            const population = country.population || 'N/A';
            const latitude = country.latitude || 'N/A';
            const longitude = country.longitude || 'N/A';

            const countryCard = `
                <div class="col-md-4 mb-4">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">${country.name} <img
                            src="https://flagcdn.com/192x144/${country.code}.png"
                            width="192"
                            height="144"
                            alt="Flag of ${country.name}"></h5>
                            <p class="card-text">
                                <strong>Continent:</strong> ${continentName}<br>
                                <strong>Population:</strong> ${population}<br>
                                <strong>Latitude:</strong> ${latitude}<br>
                                <strong>Longitude:</strong> ${longitude}
                            </p>
                        </div>
                    </div>
                </div>
            `;
            resultContainer.insertAdjacentHTML('beforeend', countryCard);
        });
    } catch (error) {
        console.error(error);
    }
});


document.getElementById('getCountryByCode').addEventListener('click', async () => {
    const countryCode = document.getElementById('countryCode').value;
    try {
        const response = await axios.get(`http://localhost:8000/countries/${countryCode}`);
        const country = response.data;
        const resultContainer = document.getElementById('countryByCodeResult');

        const continentName = country.continent?.name || 'N/A';
        const population = country.population || 'N/A';
        const latitude = country.latitude || 'N/A';
        const longitude = country.longitude || 'N/A';

        resultContainer.innerHTML = `
            <div class="card mt-4">
                <div class="card-header">
                    <h5 class="card-title">${country.name} <img
                    src="https://flagcdn.com/192x144/${country.code}.png"
                    width="192"
                    height="144"
                    alt="Flag of ${country.name}"></h5></h5>
                </div>
                <div class="card-body">
                    <p class="card-text">
                        <strong>Continent:</strong> ${continentName}<br>
                        <strong>Population:</strong> ${population}<br>
                        <strong>Latitude:</strong> ${latitude}<br>
                        <strong>Longitude:</strong> ${longitude}
                    </p>
                </div>
            </div>
        `;
    } catch (error) {
        console.error(error);
    }
});

document.getElementById('createCountryForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const newCountry = {
        code: document.getElementById('newCountryCode').value,
        name: document.getElementById('newCountryName').value,
        continentCode: document.getElementById('newCountryContinentCode').value,
        latitude: document.getElementById('newCountryLatitude').value,
        longitude: document.getElementById('newCountryLongitude').value,
        nameEs: document.getElementById('newCountryNameEs').value,
        nameFr: document.getElementById('newCountryNameFr').value,
        nameNative: document.getElementById('newCountryNameNative').value,
        population: parseInt(document.getElementById('newCountryPopulation').value),
    };

    try {
        const response = await axios.post('http://localhost:8000/countries', newCountry);
        const resultContainer = document.getElementById('createCountryResult');
        resultContainer.innerHTML = `Country created: ${response.data.name}`;
    } catch (error) {
        console.error(error);
    }
});
