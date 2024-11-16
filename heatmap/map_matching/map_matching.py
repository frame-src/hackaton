import pandas as pd
import osmnx as ox
import ast

# Load the CSV file
data = pd.read_csv("data.csv")

# Load the different GraphML files for each mode of transport
walk_graph = ox.load_graphml("walk.graphml")
cycle_graph = ox.load_graphml("bicycle.graphml")
car_graph = ox.load_graphml("car.graphml")

# Limit to the first 500 rows
data = data.iloc[:2000]

# Function to map coordinates based on the mode of transport
def map_coordinates_to_network(row):
    print(f"Processing row {row.name}/{len(data)}")
    if row['Mode'] == 'car':
        graph = car_graph
    elif row['Mode'] == 'walk':
        graph = walk_graph
    elif row['Mode'] == 'bicycle':
        graph = cycle_graph
    else:
        return None  # Return None if mode is not recognized

    # Extract coordinates from the Geometry3_JSON column
    coordinates = ast.literal_eval(row['Geometry3_JSON'])["coordinates"]
    snapped_coords = []
    # Get the first set of coordinates (V33, V34, etc.)
    for coord in coordinates.values():  # This gets the list of lat/lon pairs
        lon, lat = coord
        # Find the nearest node in the graph
        snapped_node = ox.distance.nearest_nodes(graph, lon, lat)
        snapped_lat = graph.nodes[snapped_node]['y']
        snapped_lon = graph.nodes[snapped_node]['x']
        snapped_coords.append([snapped_lat, snapped_lon])
        # Return the snapped coordinates as a series
    return snapped_coords

# Apply the function to each row and add new columns for snapped coordinates
data['Snapped_Coords'] = data.apply(map_coordinates_to_network, axis=1)

# Save the updated DataFrame with all map-matched coordinates
data.to_csv("snapped_data.csv", index=False)

print("Map matching completed and saved to snapped_data.csv")
