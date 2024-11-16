import folium
import ast
import pandas as pd

# Load your CSV file
df = pd.read_csv('snapped_data.csv')

# Create a map with CartoDB positron background (a simple light map style)
initial_coords = ast.literal_eval(df["Snapped_Coords"][0])[0] if df["Snapped_Coords"][0] else [0, 0]
m = folium.Map(location=initial_coords, zoom_start=12, tiles='CartoDB positron', control_scale=True)

# Loop through all rows in the "Snapped_Coords" column
for _, row in df.iterrows():
    # Only draw lines where the mode is 'car'
    if row["Mode"] == "car" and row["Snapped_Coords"]:
        try:
            # Convert the string to a list of coordinates
            coords = ast.literal_eval(row["Snapped_Coords"])  # Safely convert string to list

            # Add the polyline to the map with adjusted styling
            if coords:  # Ensure that the list of coordinates is not empty
                folium.PolyLine(
                    coords,
                    color="#FF5733",  # A contrasting color that looks good on the light background
                    weight=10,  # Wider line
                    opacity=0.05  # Lower opacity for a softer look
                ).add_to(m)
        except (ValueError, SyntaxError):
            # Handle the case where the coordinates are not properly formatted
            print(f"Skipping invalid coordinates: {row['Snapped_Coords']}")

# Save the map as an HTML file
m.save('map_with_car_lines_new.html')
