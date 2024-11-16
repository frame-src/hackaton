import pandas as pd

MEDIAN_CO2_G_KM = 120 



def calc_co2(rows: pd.DataFrame) -> pd.Series:
    co2_kg_values = []
    for _, row in rows.iterrows():        
        if row['Mode'] in ['walk', 'bicycle']:
            co2_kg = -1 * (row['Length']) * (MEDIAN_CO2_G_KM) / 1000
        else:
            co2_kg = (row['Length']) * (MEDIAN_CO2_G_KM) / 1000
        
        co2_kg_values.append(round(co2_kg, 2))

    return co2_kg_values

### https://colab.research.google.com/drive/1fZDtLZBprzKM26kI7w6EjbaYyUPX6byD?usp=sharing