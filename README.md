# 🏙️ Urban Equity Analyzer

### SDG 11 (Sustainable Cities) + SDG 16 (Institutions & Justice)

A geospatial web application that analyzes institutional infrastructure
distribution and proximity-based equity within U.S. cities.

This tool generates a spatial justice snapshot by mapping:

-   📊 **Infrastructure Density (Infra / km²)**
-   ⚖️ **Justice Equity Score (density × accessibility)**

The goal is to highlight potential disparities in access to essential
public institutions.

------------------------------------------------------------------------

## 🚀 Features

-   Interactive state & city selection
-   Dynamic city loading via backend API
-   Infrastructure extraction from OpenStreetMap
-   1 km × 1 km spatial grid generation
-   Institutional density calculation
-   Proximity-based accessibility modeling
-   Equity score computation
-   Server-side map rendering
-   Clean responsive frontend

------------------------------------------------------------------------

## 🧠 How It Works

### 1️⃣ Boundary Resolution

City boundaries are resolved using OpenStreetMap geocoding via OSMnx.
The city polygon is projected into EPSG:3857 for accurate area and
distance calculations.

------------------------------------------------------------------------

### 2️⃣ Infrastructure Extraction

The following infrastructure types are fetched dynamically:

-   Hospitals
-   Police stations
-   Courthouses
-   Town halls
-   Parks

Each feature is converted to a centroid point for spatial analysis.

------------------------------------------------------------------------

### 3️⃣ Grid-Based Density Calculation

The city is divided into:

> 1 km × 1 km grid cells

For each grid cell:

Infrastructure Density = Number of infrastructure points inside the cell

Since each cell is 1 km², the count directly represents density.

------------------------------------------------------------------------

### 4️⃣ Accessibility Modeling

For each grid cell:

-   Distance to nearest hospital is calculated
-   Euclidean distance is adjusted (×1.4) to approximate walking
    distance

Proximity factor:

proximity_factor = 1 / (distance_km + 1)

------------------------------------------------------------------------

### 5️⃣ Justice Equity Score

Final score:

equity_score = infrastructure_density × proximity_factor

This rewards: - Higher institutional presence
- Shorter walking distances

------------------------------------------------------------------------

## 🖥️ Tech Stack

### Backend

-   Flask
-   OSMnx
-   GeoPandas
-   NumPy
-   SciPy
-   Shapely
-   Matplotlib
-   us (state metadata)
-   zipcodes (city extraction)

### Data Source

-   OpenStreetMap (via OSMnx)

### Frontend

-   HTML5
-   CSS3
-   Vanilla JavaScript
-   Fetch API

------------------------------------------------------------------------

## 📦 Installation

### 1️⃣ Clone the repository

``` bash
git clone <your-repo-url>
cd <repo-name>
```

### 2️⃣ Create a virtual environment

``` bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

``` bash
pip install -r requirements.txt
```

If you do not yet have a requirements.txt file, create one with:

    flask
    osmnx
    geopandas
    numpy
    matplotlib
    scipy
    shapely
    us
    zipcodes

### 4️⃣ Run the app

``` bash
python app.py
```

Then visit:

    http://127.0.0.1:5000

------------------------------------------------------------------------

## 📊 Output

The application generates two maps:

1.  Infrastructure Density (Infra / km²)
2.  Justice Equity Score

The maps are rendered server-side and embedded as a Base64 image in the
frontend.

------------------------------------------------------------------------

## 🏗️ Project Structure

    app.py              → Flask routes & API
    logic.py            → Geospatial analysis engine
    templates/
        index.html      → Frontend UI
    static/
        style.css       → Styling
        app.js          → Dynamic city loading

------------------------------------------------------------------------

## 🔬 Design Decisions

-   EPSG:3857 projection for accurate meter-based calculations
-   1 km grid resolution for interpretability
-   Area constraint to prevent excessive computation
-   LRU caching for optimized city lookup
-   Server-side rendering for a lightweight frontend

------------------------------------------------------------------------

## 📈 Future Improvements

-   Population-normalized density
-   Road-network distance instead of Euclidean
-   Demographic overlays (income, race, etc.)
-   Interactive map visualization (Leaflet / Mapbox)
-   Downloadable PDF or CSV reports
-   Multi-country support

------------------------------------------------------------------------

## 🎯 Hackathon Context

This project was built during our first hackathon.

Our objective was to explore how spatial data can be used to analyze
institutional equity in urban environments.

Rather than building a simple CRUD app, we focused on:

-   Geospatial computation
-   Quantitative modeling
-   Policy-relevant insights

------------------------------------------------------------------------

## 📜 License

MIT License 
