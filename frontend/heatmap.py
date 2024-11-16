import folium
import ast
import pandas as pd


def createMap():
    df = pd.read_csv('./content/snapped_data.csv')


    initial_coords = ast.literal_eval(df["Snapped_Coords"][0])[0] if df["Snapped_Coords"][0] else [0, 0]
    m = folium.Map(location=initial_coords, zoom_start=12, tiles='CartoDB positron', control_scale=True)


    car_layer = folium.FeatureGroup(name="Car", overlay=True)
    walk_layer = folium.FeatureGroup(name="Walk", overlay=True)
    bicycle_layer = folium.FeatureGroup(name="Bicycle", overlay=True)


    for _, row in df.iterrows():
        if row["Snapped_Coords"]:
            try:
            
                coords = ast.literal_eval(row["Snapped_Coords"]) 
            
                if coords:
                
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

    m.add_child(car_layer)
    m.add_child(walk_layer)
    m.add_child(bicycle_layer)

    folium.LayerControl(collapsed=False).add_to(m)
    return m