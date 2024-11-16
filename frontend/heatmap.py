import folium
import ast
import pandas as pd


def createMap():
    df = pd.read_csv('./content/snapped_data.csv')


    # initial_point = (49.141720, 9.218849)
    # southwest = [49.0914, 9.1419]
    # northeast = [49.1920, 9.2957]
    # bounds = [southwest, northeast]
    MIN_LAT = 49.1030
    MAX_LAT = 49.1920
    MIN_LON = 9.1419
    MAX_LON = 9.2957
    initial_point = (49.141720, 9.218849)
    m = folium.Map(location=initial_point,max_lat=MAX_LAT, min_lat=MIN_LAT, max_lon=MAX_LON, min_lon =MIN_LON,  zoom_start=13, max_zoom=19, min_zoom=13, max_bounds=True, tiles='CartoDB positron', control_scale=True)


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

    custom_css = """
    .leaflet-control-layers-toggle {
        display: none;  /* Hide the title */
    }
    """

    # Inject the custom CSS into the map
    style = folium.Element(f'<style>{custom_css}</style>')
    m.get_root().html.add_child(style)

    # Add LayerControl
    folium.LayerControl(collapsed=False, position='bottomright').add_to(m)
    return m