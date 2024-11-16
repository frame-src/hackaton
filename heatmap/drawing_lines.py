import folium
import ast
import pandas as pd

# Load your CSV file
df = pd.read_csv('snapped_data.csv')

# Create a map with CartoDB positron background
initial_coords = ast.literal_eval(df["Snapped_Coords"][0])[0] if df["Snapped_Coords"][0] else [0, 0]
m = folium.Map(location=initial_coords, zoom_start=12, tiles='CartoDB positron', control_scale=True)

# Create FeatureGroups for each mode of transport
car_layer = folium.FeatureGroup(name="Car", overlay=True)
walk_layer = folium.FeatureGroup(name="Walk", overlay=True)
bicycle_layer = folium.FeatureGroup(name="Bicycle", overlay=True)

# Loop through all rows in the dataframe
for _, row in df.iterrows():
    if row["Snapped_Coords"]:
        try:
            # Convert the string to a list of coordinates
            coords = ast.literal_eval(row["Snapped_Coords"])  # Safely convert string to list

            # Ensure that the list of coordinates is not empty
            if coords:
                # Add to the appropriate layer based on the mode
                if row["Mode"] == "car":
                    folium.PolyLine(
                        coords, color="#2196F3", weight=10, opacity=0.03
                    ).add_to(car_layer)
                elif row["Mode"] == "walk":
                    folium.PolyLine(
                        coords, color="#4CAF50", weight=10, opacity=0.05
                    ).add_to(walk_layer)
                elif row["Mode"] == "bicycle":
                    folium.PolyLine(
                        coords, color="#FFC107", weight=10, opacity=0.05
                    ).add_to(bicycle_layer)
        except (ValueError, SyntaxError):
            print(f"Skipping invalid coordinates: {row['Snapped_Coords']}")

# Add the FeatureGroups to the map
m.add_child(car_layer)
m.add_child(walk_layer)
m.add_child(bicycle_layer)

# Add LayerControl to toggle the layers
folium.LayerControl(collapsed=False).add_to(m)

# Save the map as an HTML file
m.save('map_with_interactive_layers.html')
