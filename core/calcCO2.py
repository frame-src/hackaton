import pandas as pd

median_co2_g_km = 120 

# Apply the calc_co2 function to each row of the DataFrame

def calcCO2(df):
  for rows in df.iterrows():
    co2_kg = (rows['Length']) * (median_co2_g_km) / 1000
  
  df['CO2_kg'] = df.apply(calcCO2, axis=1) 
  return df


### https://colab.research.google.com/drive/1fZDtLZBprzKM26kI7w6EjbaYyUPX6byD?usp=sharing