import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import requests
from utils import lengthCalculator,moneySavedPetrol, moneySavedElectric
st.set_page_config(
    layout = 'wide',
    page_title = 'MFT'
)


# with st.sidebar:
selected = option_menu(
    menu_title= None,
    options=["Home", "Maps", "Activity"],
    icons=["house", "book", "activity"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

# HOME
if selected == "Home":
	st.markdown("<h1 style='text-align: center; color: grey;'>Welcome to MFT</h1>", unsafe_allow_html=True)

	# Read the CSV file
	df = pd.read_csv("./content/ID_163.csv")
	length = round(lengthCalculator(df))
	petrol_consumption =  round(moneySavedPetrol(length))
	electric_consumption = round(moneySavedElectric(length))
	st.markdown(f"<h5 style='text-align: center; color: lightcoral;'>Consuption of CO2 : </h4>", unsafe_allow_html=True)
    
	df['StartedAt_Timestamp'] = pd.to_datetime(df['StartedAt_Timestamp'])
	for _, row in df.iterrows():
		if row['Mode'] == 'car':
			df.at[_, 'CO2_kg'] = row['CO2_kg'] * -1
		else:
			df.at[_, 'CO2_kg'] = row['CO2_kg'] * 10

	start_row = pd.DataFrame({'StartedAt_Timestamp': [df['StartedAt_Timestamp'].min().replace(hour=0, minute=0, second=0)],
                              'CO2_kg': [0], 'Mode': ['']})
	end_row = pd.DataFrame({'StartedAt_Timestamp': [df['StartedAt_Timestamp'].max().replace(hour=23, minute=59, second=59)],
                            'CO2_kg': [0], 'Mode': ['']})
	df = pd.concat([start_row, df, end_row], ignore_index=True)

	#Color depending on the mode
	color_scale = alt.Scale(
		domain=['car', 'train', 'tram', 'bus', 'bike', 'walk'],
		range=['#FF0000', '#90EE90', '#90EE90', '#90EE90', '#90EE90', '#90EE90']
		)

	# Create an Altair area chart
	chart = alt.Chart(df).mark_area().encode(
		x=alt.X('StartedAt_Timestamp:T', title='Time'),
		y='CO2_kg:Q',
		color=alt.Color('Mode:N', scale=color_scale),
		tooltip=['StartedAt_Timestamp', 'CO2_kg', 'Mode']
	).transform_filter(
		alt.datum.Mode != ''
	).properties(
		width=700,
		height=400
	).interactive()

	st.altair_chart(chart, use_container_width=True)
	st.markdown(f"""
    <div style="text-align: center;">
        <span style='color: grey; font-size: 21px;'>Today you saved: </span>
        <span style='color: lightcoral; font-size: 21px;'>{petrol_consumption}€ </span>
        <span style='color: grey; font-size: 21px;'>in Gas, or </span>
        <span style='color: lightcoral; font-size: 21px;'>{electric_consumption}€ </span>
        <span style='color: grey; font-size: 21px;'>in Electric over {length}km </span>
    </div> """, unsafe_allow_html=True)

from heatmap import createMap
from streamlit_folium import st_folium

# MAPS
if selected == "Maps":
    m = createMap()
    st_folium(m, width=430)






#PROFILE or ACTIVITIES or ACHIEVMENTS
if selected == "Activity":
    st.title("PROFILE")



# CHART HERE:

# try:
#     response = requests.get('http://localhost:8000/Test', headers={'accept': 'application/json'})    
#     if response.status_code == 200:
#         data = response.json()
#         st.success('Endpoint called successfully!')
#         st.json(data)  # Display the response data in JSON format
#     else:
#         st.error(f'Error: {response.status_code}')
#         st.text(response.text)  # Display the raw response text
# except Exception as e:
#         st.error('Failed to call the endpoint')
#         st.exception(e)


# num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
# num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

# indices = np.linspace(0, 1, num_points)
# theta = 2 * np.pi * num_turns * indices
# radius = indices

# x = radius * np.cos(theta)
# y = radius * np.sin(theta)

# df = pd.DataFrame({
#     "x": x,
#     "y": y,
#     "idx": indices,
#     "rand": np.random.randn(num_points),
# })



# st.altair_chart(alt.Chart(df, height=700, width=700)
#     .mark_point(filled=True)
#     .encode(
#         x=alt.X("x", axis=None),
#         y=alt.Y("y", axis=None),
#         color=alt.Color("idx", legend=None, scale=alt.Scale()),
#         size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
#     ))

