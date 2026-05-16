# -*- coding: utf-8 -*-
"""UK Security Map Generator

Generates an interactive world map showing UK security relationships.
"""

import folium
import json
import requests

# Example security data (DEFINE THIS FIRST, before using it)
new_security_data = {
    "Afghanistan": "Limited engagement",
    "Albania": "NATO ally",
    "Algeria": "Regional partner",
    "Andorra": "European partner",
    "Angola": "Regional partner",
    "Antigua and Barbuda": "Commonwealth partner",
    "Argentina": "Falklands dispute",
    "Armenia": "Regional partner",
    "Australia": "AUKUS ally",
    "Austria": "European partner",
    "Azerbaijan": "Energy partner",
    "Bahamas": "Commonwealth partner",
    "Bahrain": "Gulf partner",
    "Bangladesh": "Commonwealth partner",
    "Barbados": "Commonwealth partner",
    "Belarus": "Sanctions target",
    "Belgium": "NATO ally",
    "Belize": "Commonwealth partner",
    "Benin": "Regional partner",
    "Bhutan": "Development partner",
    "Bolivia": "Regional partner",
    "Bosnia and Herzegovina": "Stability partner",
    "Botswana": "Commonwealth partner",
    "Brazil": "Strategic partner",
    "Brunei": "Defence partner",
    "Bulgaria": "NATO ally",
    "Burkina Faso": "Fragile partner",
    "Burundi": "Development partner",
    "Cabo Verde": "Maritime partner",
    "Cambodia": "Regional partner",
    "Cameroon": "Commonwealth partner",
    "Canada": "Five Eyes",
    "Central African Republic": "Fragile partner",
    "Chad": "Regional partner",
    "Chile": "Defence partner",
    "China": "Systemic challenge",
    "Colombia": "Security partner",
    "Comoros": "Regional partner",
    "Congo": "Regional partner",
    "Costa Rica": "Regional partner",
    "Côte d'Ivoire": "Regional partner",
    "Croatia": "NATO ally",
    "Cuba": "Limited engagement",
    "Cyprus": "Bases partner",
    "Czechia": "NATO ally",
    "Democratic Republic of Congo": "Stabilisation partner",
    "Denmark": "NATO ally",
    "Djibouti": "Maritime partner",
    "Dominica": "Commonwealth partner",
    "Dominican Republic": "Regional partner",
    "Ecuador": "Regional partner",
    "Egypt": "Security partner",
    "El Salvador": "Regional partner",
    "Equatorial Guinea": "Limited engagement",
    "Eritrea": "Limited engagement",
    "Estonia": "NATO ally",
    "Eswatini": "Commonwealth partner",
    "Ethiopia": "Development partner",
    "Fiji": "Commonwealth partner",
    "Finland": "NATO ally",
    "France": "Defence ally",
    "Gabon": "Regional partner",
    "Gambia": "Commonwealth partner",
    "Georgia": "Strategic partner",
    "Germany": "NATO ally",
    "Ghana": "Commonwealth partner",
    "Greece": "NATO ally",
    "Grenada": "Commonwealth partner",
    "Guatemala": "Regional partner",
    "Guinea": "Regional partner",
    "Guinea-Bissau": "Regional partner",
    "Guyana": "Commonwealth partner",
    "Haiti": "Fragile partner",
    "Holy See": "Diplomatic partner",
    "Honduras": "Regional partner",
    "Hungary": "NATO ally",
    "Iceland": "NATO ally",
    "India": "Strategic partner",
    "Indonesia": "Indo-Pacific partner",
    "Iran": "Hostile actor",
    "Iraq": "Counterterror partner",
    "Ireland": "Security partner",
    "Israel": "Security partner",
    "Italy": "NATO ally",
    "Jamaica": "Commonwealth partner",
    "Japan": "Strategic partner",
    "Jordan": "Security partner",
    "Kazakhstan": "Regional partner",
    "Kenya": "Defence partner",
    "Kiribati": "Commonwealth partner",
    "Kosovo": "Stability partner",
    "Kuwait": "Gulf partner",
    "Kyrgyzstan": "Regional partner",
    "Laos": "Regional partner",
    "Latvia": "NATO ally",
    "Lebanon": "Stability partner",
    "Lesotho": "Commonwealth partner",
    "Liberia": "Development partner",
    "Libya": "Fragile partner",
    "Liechtenstein": "European partner",
    "Lithuania": "NATO ally",
    "Luxembourg": "NATO ally",
    "Madagascar": "Regional partner",
    "Malawi": "Commonwealth partner",
    "Malaysia": "Defence partner",
    "Maldives": "Commonwealth partner",
    "Mali": "Fragile partner",
    "Malta": "Commonwealth partner",
    "Marshall Islands": "Regional partner",
    "Mauritania": "Regional partner",
    "Mauritius": "Commonwealth partner",
    "Mexico": "Strategic partner",
    "Micronesia": "Regional partner",
    "Moldova": "Security partner",
    "Monaco": "European partner",
    "Mongolia": "Regional partner",
    "Montenegro": "NATO ally",
    "Morocco": "Security partner",
    "Mozambique": "Commonwealth partner",
    "Myanmar": "Sanctions target",
    "Namibia": "Commonwealth partner",
    "Nauru": "Commonwealth partner",
    "Nepal": "Defence partner",
    "Netherlands": "NATO ally",
    "New Zealand": "Five Eyes",
    "Nicaragua": "Limited engagement",
    "Niger": "Fragile partner",
    "Nigeria": "Security partner",
    "North Korea": "Sanctions target",
    "North Macedonia": "NATO ally",
    "Norway": "NATO ally",
    "Oman": "Gulf partner",
    "Pakistan": "Security partner",
    "Palau": "Regional partner",
    "Palestine": "Fragile engagement",
    "Panama": "Regional partner",
    "Papua New Guinea": "Commonwealth partner",
    "Paraguay": "Regional partner",
    "Peru": "Regional partner",
    "Philippines": "Maritime partner",
    "Poland": "NATO ally",
    "Portugal": "NATO ally",
    "Qatar": "Gulf partner",
    "Romania": "NATO ally",
    "Russia": "Hostile state",
    "Rwanda": "Commonwealth partner",
    "Saint Kitts and Nevis": "Commonwealth partner",
    "Saint Lucia": "Commonwealth partner",
    "Saint Vincent and the Grenadines": "Commonwealth partner",
    "Samoa": "Commonwealth partner",
    "San Marino": "European partner",
    "São Tomé and Príncipe": "Regional partner",
    "Saudi Arabia": "Gulf partner",
    "Senegal": "Regional partner",
    "Serbia": "Regional partner",
    "Seychelles": "Commonwealth partner",
    "Sierra Leone": "Commonwealth partner",
    "Singapore": "Defence partner",
    "Slovakia": "NATO ally",
    "Slovenia": "NATO ally",
    "Solomon Islands": "Commonwealth partner",
    "Somalia": "Stabilisation partner",
    "South Africa": "Commonwealth partner",
    "South Korea": "Strategic partner",
    "South Sudan": "Fragile partner",
    "Spain": "NATO ally",
    "Sri Lanka": "Commonwealth partner",
    "Sudan": "Fragile partner",
    "Suriname": "Regional partner",
    "Sweden": "NATO ally",
    "Switzerland": "European partner",
    "Syria": "Sanctions target",
    "Tajikistan": "Regional partner",
    "Tanzania": "Commonwealth partner",
    "Thailand": "Regional partner",
    "Timor-Leste": "Regional partner",
    "Togo": "Commonwealth partner",
    "Tonga": "Commonwealth partner",
    "Trinidad and Tobago": "Commonwealth partner",
    "Tunisia": "Security partner",
    "Türkiye": "NATO ally",
    "Turkmenistan": "Limited engagement",
    "Tuvalu": "Commonwealth partner",
    "Uganda": "Commonwealth partner",
    "Ukraine": "Security partner",
    "United Arab Emirates": "Gulf partner",
    "United States": "AUKUS ally",
    "Uruguay": "Regional partner",
    "Uzbekistan": "Regional partner",
    "Vanuatu": "Commonwealth partner",
    "Venezuela": "Limited engagement",
    "Vietnam": "Strategic partner",
    "Yemen": "Fragile partner",
    "Zambia": "Commonwealth partner",
    "Zimbabwe": "Limited engagement"
}

# Define the GeoJSON URL for world countries
geojson_url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"

# Create a Folium Map with dark tiles for a black background
world_map_interactive = folium.Map(location=[0, 0], zoom_start=2, tiles='CartoDB darkmatter')

# Fetch world countries GeoJSON data
response = requests.get(geojson_url)
response.raise_for_status()
world_geojson = json.loads(response.text.strip())

# Add security relationship to GeoJSON properties
for feature in world_geojson['features']:
    country_name = feature['properties']['name']
    feature['properties']['security_relationship_with_uk'] = new_security_data.get(country_name, 'No Specific Relationship Data')

# Define neon green color
NEON_GREEN = '#39FF14'

# Define style function for default country appearance
def style_function(feature):
    return {
        'fillColor': '#000000',
        'color': NEON_GREEN,
        'weight': 1,
        'fillOpacity': 0.1
    }

# Define highlight function for hover effect
def highlight_function(feature):
    return {
        'fillColor': NEON_GREEN,
        'color': NEON_GREEN,
        'weight': 3,
        'fillOpacity': 1
    }

# Add the GeoJSON layer to the map with custom styling and tooltips
folium.GeoJson(
    world_geojson,
    name='World Countries',
    tooltip=folium.GeoJsonTooltip(
        fields=['name', 'security_relationship_with_uk'],
        aliases=['Country:', 'UK Security Relationship:'],
        localize=True
    ),
    style_function=style_function,
    highlight_function=highlight_function
).add_to(world_map_interactive)

# Save the interactive map to an HTML file
output_file = 'index.html'
world_map_interactive.save(output_file)
print(f"Map saved to {output_file}")
