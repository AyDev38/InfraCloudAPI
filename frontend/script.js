let currentPage = 1;
const itemsPerPage = 10;

document.getElementById('getAllCountries').addEventListener('click', () => {
    currentPage = 1;
    getCountries();
});

document.getElementById('prevPage').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        getCountries();
    }
});

document.getElementById('nextPage').addEventListener('click', () => {
    currentPage++;
    getCountries();
});

document.addEventListener('DOMContentLoaded', async () => {
    await populateContinentCodes();
});

async function populateContinentCodes() {
    try {
        const response = await axios.get('http://localhost:8000/continents');
        const continents = response.data;
        const continentSelect = document.getElementById('newCountryContinentCode');
        
        continents.forEach(continent => {
            const option = document.createElement('option');
            option.value = continent.code;
            option.textContent = continent.code;
            continentSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error fetching continents:', error);
    }
}

async function getCountries() {
    try {
        const response = await axios.get(`http://localhost:8000/countries`);
        const countries = response.data;
        const resultContainer = document.getElementById('allCountriesResult');
        resultContainer.innerHTML = '';

        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const countriesToDisplay = countries.slice(startIndex, endIndex);

        for (const country of countriesToDisplay) {
            const continentCode = country.continent_code || 'N/A';
            const continent = await axios.get(`http://localhost:8000/continents/${continentCode}`);
            const continentName = continent.data.name;
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
                            <button class="btn btn-danger delete-country" data-code="${country.code}">Delete</button>
                            <button class="btn btn-success edit-country" data-code="${country.code}">Edit</button>
                        </div>
                    </div>
                    <div class="edit-form" style="display: none;">
                        <div class="form-group">
                            <input type="text" class="form-control" value="${country.code}" data-field="code" placeholder="Code" readonly>
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control" value="${country.name}" data-field="name" placeholder="Name">
                        </div>
                        <div class="form-group">
                            <input type="hidden" class="form-control" value="${continentCode}" data-field="continent_code">
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control" value="${latitude}" data-field="latitude" placeholder="Latitude">
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control" value="${longitude}" data-field="longitude" placeholder="Longitude">
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control" value="${country.nameEs}" data-field="nameEs" placeholder="Name (ES)">
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control" value="${country.nameFr}" data-field="nameFr" placeholder="Name (FR)">
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control" value="${country.nameNative}" data-field="nameNative" placeholder="Native Name">
                        </div>
                        <div class="form-group">
                            <input type="number" class="form-control" value="${population}" data-field="population" placeholder="Population">
                        </div>
                        <button class="btn btn-primary save-country" data-code="${country.code}">Save</button>
                        <button class="btn btn-secondary cancel-edit" data-code="${country.code}">Cancel</button>
                    </div>
                </div>
            `;
            resultContainer.insertAdjacentHTML('beforeend', countryCard);
        }

        document.getElementById('pageNumber').textContent = `Page ${currentPage}`;

        // Disable previous button if on the first page
        document.getElementById('prevPage').disabled = currentPage === 1;

        // Disable next button if on the last page
        document.getElementById('nextPage').disabled = endIndex >= countries.length;

        // Add event listeners for the delete buttons
        document.querySelectorAll('.delete-country').forEach(button => {
            button.addEventListener('click', async (event) => {
                const code = event.target.getAttribute('data-code');
                await deleteCountry(code);
            });
        });

        // Add event listeners for the edit buttons
        document.querySelectorAll('.edit-country').forEach(button => {
            button.addEventListener('click', (event) => {
                const card = event.target.closest('.col-md-4');
                const editForm = card.querySelector('.edit-form');
                editForm.style.display = editForm.style.display === 'none' ? 'block' : 'none';
            });
        });

        // Add event listeners for the save buttons
        document.querySelectorAll('.save-country').forEach(button => {
            button.addEventListener('click', async (event) => {
                const card = event.target.closest('.col-md-4');
                const code = event.target.getAttribute('data-code');
                const updatedCountry = {};
                card.querySelectorAll('[data-field]').forEach(input => {
                    updatedCountry[input.getAttribute('data-field')] = input.value;
                });
                updatedCountry.population = parseInt(updatedCountry.population); // Convert population to number
                await updateCountry(code, updatedCountry);
            });
        });

        // Add event listeners for the cancel buttons
        document.querySelectorAll('.cancel-edit').forEach(button => {
            button.addEventListener('click', (event) => {
                const card = event.target.closest('.col-md-4');
                const editForm = card.querySelector('.edit-form');
                editForm.style.display = 'none';
            });
        });

    } catch (error) {
        console.error(error);
    }
}

async function deleteCountry(code) {
    try {
        await axios.delete(`http://localhost:8000/countries/${code}`);
        getCountries(); // Refresh the list after deletion
    } catch (error) {
        console.error(error);
    }
}

async function updateCountry(code, updatedCountry) {
    try {
        await axios.put(`http://localhost:8000/countries/${code}`, updatedCountry);
        getCountries(); // Refresh the list after update
    } catch (error) {
        console.error(error);
    }
}

document.getElementById('getCountryByCode').addEventListener('click', async () => {
    const countryCode = document.getElementById('countryCode').value;
    try {
        const response = await axios.get(`http://localhost:8000/countries/${countryCode}`);
        const country = response.data;
        const resultContainer = document.getElementById('countryByCodeResult');

        const continentCode = country.continent_code || 'N/A';
        const continent = await axios.get(`http://localhost:8000/continents/${continentCode}`);
        const continentName = continent.data.name;
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
        continent_code: document.getElementById('newCountryContinentCode').value,
        latitude: document.getElementById('newCountryLatitude').value,
        longitude: document.getElementById('newCountryLongitude').value,
        name: document.getElementById('newCountryName').value,
        nameEs: document.getElementById('newCountryNameEs').value,
        nameFr: document.getElementById('newCountryNameFr').value,
        nameNative: document.getElementById('newCountryNameNative').value,
        population: parseInt(document.getElementById('newCountryPopulation').value)
    };

    try {
        const response = await axios.post('http://localhost:8000/countries', newCountry);
        const resultContainer = document.getElementById('createCountryResult');
        resultContainer.innerHTML = `Country created: ${response.data.name}`;
        getCountries(); // Refresh the list after creation
    } catch (error) {
        console.error(error);
    }
});
