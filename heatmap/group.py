import pandas as pd
import json
import folium

data = pd.read_csv("../content/data.csv")

def extract_coordinates(json_str):
    try:
    
        parsed_json = json.loads(json_str)
    
        return [[coord[1], coord[0]] for coord in parsed_json['coordinates'].values()]
    except (json.JSONDecodeError, KeyError, TypeError):
    
        return []

data['Coordinates'] = data['Geometry3_JSON'].apply(extract_coordinates)

data = data[data['Coordinates'].apply(len) > 0]

car_data = data[data['Mode'] == 'car']

map_center = [49.15, 9.22] 
line_map = folium.Map(location=map_center, zoom_start=12, tiles="CartoDB positron")

for route_coords in car_data['Coordinates']:
    if route_coords: 
        folium.PolyLine(
            locations=route_coords, 
            color="blue",          
            weight=3,              
            opacity=0.3            
        ).add_to(line_map)

line_map.save("car_routes_map.html")

print("Routes map with simple tiles has been generated and saved as 'car_routes_map.html'")
