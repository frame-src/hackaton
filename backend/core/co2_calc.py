median_co2_g_km = 120 

data = '/content/data.csv'
df = pd.read_csv(data)

# Apply the calc_co2 function to each row of the DataFrame
df['CO2_kg'] = df.apply(calc_co2, axis=1) 

def calc_co2(rows):
  if rows['Mode'] in ['walk', 'bicycle']:
    co2_kg = -1 * (rows['Length']) * (median_co2_g_km) / 1000
  else:
    co2_kg = (rows['Length']) * (median_co2_g_km) / 1000
  
  return round(co2_kg, 2)


### https://colab.research.google.com/drive/1fZDtLZBprzKM26kI7w6EjbaYyUPX6byD?usp=sharing