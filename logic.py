import osmnx as ox
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import box
from scipy.spatial.distance import cdist
import io
import base64

# Set OSMnx settings
ox.settings.use_cache = True

def get_equity_analysis(place_name):
    try:
        # --- 1. DATA FETCHING ---
        city_gdf = ox.geocode_to_gdf(place_name)
        poly_4326 = city_gdf.geometry.iloc[0]
        poly_3857 = gpd.GeoSeries([poly_4326], crs="EPSG:4326").to_crs(3857).iloc[0]

        tags = {"amenity": ["police", "courthouse", "hospital", "townhall"], "leisure": "park"}
        pois = ox.features_from_polygon(poly_4326, tags).copy()
        pois['geometry'] = pois.geometry.centroid
        inst_pts = pois.dropna(subset=["geometry"]).to_crs(3857)

        # --- 2. GRID GENERATION (1000m) ---
        cell_size_m = 1000 
        minx, miny, maxx, maxy = poly_3857.bounds
        xs = np.arange(minx, maxx, cell_size_m)
        ys = np.arange(miny, maxy, cell_size_m)
        cells = [box(x, y, x + cell_size_m, y + cell_size_m) for x in xs for y in ys]
        grid = gpd.GeoDataFrame({"cell_id": range(len(cells))}, geometry=cells, crs="EPSG:3857")
        grid = gpd.overlay(grid, gpd.GeoDataFrame(geometry=[poly_3857], crs="EPSG:3857"), how="intersection")

        # --- 3. FAST PROXIMITY CALC ---
        grid_centers = np.array([(geom.centroid.x, geom.centroid.y) for geom in grid.geometry])
        hospitals = inst_pts[inst_pts['amenity']=='hospital']
        
        if not hospitals.empty:
            hosp_coords = np.array([(geom.x, geom.y) for geom in hospitals.geometry])
            distances = cdist(grid_centers, hosp_coords, 'euclidean')
            grid["walk_dist_m"] = np.min(distances, axis=1) * 1.4 
        else:
            grid["walk_dist_m"] = 5000 

        # --- 4. SCORING ---
        joined = gpd.sjoin(inst_pts, grid, how="left", predicate="intersects")
        grid["inst_count"] = grid["cell_id"].map(joined.groupby("cell_id").size()).fillna(0)
        
        # We'll use a placeholder population density or logic here
        grid["proximity_factor"] = 1 / (grid["walk_dist_m"] / 1000 + 1)
        grid["equity_score"] = grid["inst_count"] * grid["proximity_factor"]

        # --- 5. IMAGE GENERATION ---
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        grid.plot(ax=ax[0], column="inst_count", cmap="YlOrRd", legend=True)
        ax[0].set_title("Infrastructure Density")
        grid.plot(ax=ax[1], column="equity_score", cmap="RdYlGn", legend=True)
        ax[1].set_title("Justice Equity Score")
        
        for a in ax: a.set_axis_off()
        plt.tight_layout()

        # Convert to Base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode('utf-8')

    except Exception as e:
        print(f"Error in logic: {e}")
        return None