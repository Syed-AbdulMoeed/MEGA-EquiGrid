const stateSelect = document.getElementById("state");
const citySelect = document.getElementById("city");
let currentCities = [];
let requestToken = 0;

function setCityPlaceholder(text) {
    citySelect.innerHTML = "";
    const option = document.createElement("option");
    option.value = "";
    option.textContent = text;
    citySelect.appendChild(option);
}

function renderCities(cities, selectedCity = "") {
    citySelect.innerHTML = "";
    const first = document.createElement("option");
    first.value = "";
    first.textContent = cities.length ? "Select city" : "No cities found";
    citySelect.appendChild(first);

    for (const city of cities) {
        const option = document.createElement("option");
        option.value = city;
        option.textContent = city;
        if (selectedCity && city === selectedCity) {
            option.selected = true;
        }
        citySelect.appendChild(option);
    }
}

async function loadCities(stateAbbr, selectedCity = "") {
    const token = ++requestToken;
    currentCities = [];

    if (!stateAbbr) {
        citySelect.disabled = true;
        setCityPlaceholder("Select state first");
        return;
    }

    citySelect.disabled = true;
    setCityPlaceholder("Loading cities...");

    try {
        const resp = await fetch(`/api/cities?state=${encodeURIComponent(stateAbbr)}`);
        const payload = await resp.json();
        if (token !== requestToken) {
            return;
        }

        currentCities = Array.isArray(payload.cities) ? payload.cities : [];
        renderCities(currentCities, selectedCity);
    } catch (err) {
        if (token !== requestToken) {
            return;
        }
        currentCities = [];
        setCityPlaceholder("Unable to load cities");
    } finally {
        if (token === requestToken) {
            citySelect.disabled = false;
        }
    }
}

stateSelect.addEventListener("change", () => {
    loadCities(stateSelect.value);
});

loadCities(stateSelect.value, citySelect.dataset.selected || "");
