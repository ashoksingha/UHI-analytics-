import streamlit as st
import ee
import geemap.foliumap as geemap

# Initialize Google Earth Engine
ee.Initialize()

st.title("Urbanization & Climate Impact App: Bhubaneswar")
st.sidebar.title("Controls")

# Dropdown Menu for Indices [cite: 95, 136]
index_choice = st.sidebar.selectbox(
    "Select Index to Visualize",
    ("Land Surface Temperature (LST)", "Vegetation Index (NDVI)", "Built-up Index (NDBI)", "LULC Classification")
)

# Year Selection for Decadal Comparison [cite: 102]
year = st.sidebar.slider("Select Year", 2000, 2026, 2020)

# Define Bhubaneswar Region [cite: 57]
roi = ee.Geometry.Point([85.8245, 20.2961]).buffer(15000)

def get_landsat(year):
    # Select Landsat collection based on year [cite: 66]
    if year < 2013:
        img = ee.ImageCollection("LANDSAT/LE07/C02/T1_L2").filterBounds(roi).filterDate(f'{year}-01-01', f'{year}-12-31').median()
    else:
        img = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2").filterBounds(roi).filterDate(f'{year}-01-01', f'{year}-12-31').median()
    return img

img = get_landsat(year)

# 3. Processing Functions
def calculate_indices(image):
    # NDVI Calculation [cite: 96]
    ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
    # NDBI Calculation [cite: 97]
    ndbi = image.normalizedDifference(['SR_B6', 'SR_B5']).rename('NDBI')
    return ndvi, ndbi

ndvi, ndbi = calculate_indices(img)

# 4. Map Display
Map = geemap.Map(center=[20.2961, 85.8245], zoom=12)

if index_choice == "Vegetation Index (NDVI)":
    Map.addLayer(ndvi, {'min': 0, 'max': 1, 'palette': ['red', 'yellow', 'green']}, "NDVI")
elif index_choice == "Land Surface Temperature (LST)":
    # Simplified LST visualization [cite: 137]
    lst = img.select('ST_B10').multiply(0.00341802).add(149.0).subtract(273.15)
    Map.addLayer(lst, {'min': 20, 'max': 45, 'palette': ['blue', 'yellow', 'red']}, "LST (°C)")
elif index_choice == "Built-up Index (NDBI)":
    Map.addLayer(ndbi, {'min': -1, 'max': 1, 'palette': ['white', 'blue']}, "NDBI")

Map.to_streamlit(height=600)

# 5. Impact Insights [cite: 138, 171]
st.subheader(f"Insights for Bhubaneswar in {year}")
st.write("Based on the methodology of Thomas et al. (2026):")
st.info("Reduction in vegetation cover directly correlates with a 3°C to 5°C rise in surface temperature[cite: 16, 191].")
if __name__ == "__main__":
    main()
