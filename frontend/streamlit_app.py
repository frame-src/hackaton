import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import requests
from utils import lengthCalculator,moneySavedPetrol, moneySavedElectric, caloriesBurned, hoursOutdoors, foodAmountForCalories
from datetime import datetime, timedelta

st.set_page_config(
    layout='wide',
    page_title='MFT'
)

# with st.sidebar:
selected = option_menu(
    menu_title=None,
    options=["Home", "Maps", "Activity"],
    icons=["house", "book", "activity"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

df = pd.read_csv("./content/ID_363.csv")
length = round(lengthCalculator(df))
petrol_consumption =  round(moneySavedPetrol(length))
electric_consumption = round(moneySavedElectric(length))
cal = round( caloriesBurned(length))
hours = round( hoursOutdoors(length, 19))
food = foodAmountForCalories(length)

# HOME
if selected == "Home":
	st.markdown("<h1 style='text-align: center; color: grey;'>Welcome to MFT</h1>", unsafe_allow_html=True)

	# Read the CSV file

	st.markdown(f"<h5 style='text-align: center; color: lightcoral;'>Consuption of CO2 : </h4>", unsafe_allow_html=True)
    
	df['StartedAt_Timestamp'] = pd.to_datetime(df['StartedAt_Timestamp'])

	# Change the CO2 values depending on the mode
	for _, row in df.iterrows():
		if row['Mode'] == 'car':
			df.at[_, 'CO2_kg'] = row['CO2_kg']
		else:
			df.at[_, 'CO2_kg'] = row['CO2_kg'] * -1

	# Get the minimum and maximum timestamps for the whole day
	min_timestamp = df['StartedAt_Timestamp'].min().replace(hour=1, minute=0, second=1)
	max_timestamp = df['StartedAt_Timestamp'].max().replace(hour=23, minute=59, second=59)

    # Add an initial row with a timestamp just before the first data point and set the CO2_kg value to 0
	first_data_timestamp = df['StartedAt_Timestamp'].min()
	initial_row = pd.DataFrame({'StartedAt_Timestamp': [first_data_timestamp - timedelta(seconds=1)],
                                'CO2_kg': [0], 'Mode': ['initial']})
	df = pd.concat([initial_row, df], ignore_index=True)

    # Add rows at the beginning and end with the same Mode as the first and last data points
	start_row = pd.DataFrame({'StartedAt_Timestamp': [min_timestamp],
                              'CO2_kg': [0], 'Mode': ['initial']})
	end_row = pd.DataFrame({'StartedAt_Timestamp': [max_timestamp],
                            'CO2_kg': [df.iloc[-1]['CO2_kg']], 'Mode': [df.iloc[-1]['Mode']]})
	df = pd.concat([start_row, df, end_row], ignore_index=True)

    # Ensure the timestamp columns are of type datetime64[ns]
	df['StartedAt_Timestamp'] = pd.to_datetime(df['StartedAt_Timestamp'])

    # Define the color scale based on the Mode column
	color_scale = alt.Scale(
        domain=['car', 'train', 'tram', 'bus', 'bike', 'walk'],
        range=['#FF0000', '#00FF00', '#00FF00', '#00FF00', '#00FF00', '#00FF00']
    )

    # Create a simplified Altair area chart to ensure data is being plotted
	area_chart = alt.Chart(df).mark_area().encode(
        x='StartedAt_Timestamp:T',
        y=alt.Y('CO2_kg:Q', scale=alt.Scale(domain=(0.5, -0.5))),
        color=alt.Color('Mode:N', scale=color_scale),
        tooltip=['StartedAt_Timestamp', 'CO2_kg', 'Mode']
    ).properties(
        width=700,
        height=400
    ).interactive()
	rule = alt.Chart(pd.DataFrame({'y': [-0.35]})).mark_rule(color='lightgreen').encode(
		y='y:Q'
	)
	text = alt.Chart(pd.DataFrame({'y': [-0.35], 'text': ['Your daily goal of CO2 reduction']})).mark_text(
		align='right', dx=5, dy=-5, color='grey'
	).encode(
		y='y:Q',
		text='text:N'
	)
	chart = alt.layer(area_chart, rule, text)
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

rendered_map = "./map.html"
with open(rendered_map, "r") as file:
    map_ready = file.read()

# Inject the CSS into the Streamlit app
# st_folium.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# MAPS
if selected == "Maps":
    m = createMap()
    st_folium(m, width=430)



#PROFILE or ACTIVITIES or ACHIEVMENTS
if selected == "Activity":

	# Title and description
    st.title("Eco Challenges: Be a Green Transport Hero!")
    st.subheader("Join the movement to save the planet while having fun 🌍")

	# User inputs
    username = "Tomek"
    if username:
       st.success(f"Welcome, {username}! Ready for some eco challenges?")

	# Challenges Menu
    "Select Your Challenge"
    challenge = st.radio("Pick one challenge:", 
								["EcoHero Dash", "Penguin Saver Marathon", "Carbon Ninja Challenge", "Mode Switch Master"])

	# EcoHero Dash
    if challenge == "EcoHero Dash":
        st.header("🏆 EcoHero Dash")
        st.write("""
        🌟 **Objective:** Use green transportation (bike, bus, walk, etc.) to collect eco-points.  
        🚴 Earn 10 points per green trip, 20 points for carpooling!  
        """)
        
        trips = []
        for modes in df['Mode']:
            if modes != 'car':
                trips.append(modes)

        st.write(f"Number of green trips you completed:{len(trips)}")
        # carpool = st.number_input("Number of carpool trips you participated in:", 0, 100, step=1)
        
        eco_points = len(trips) * 10 
        # + carpool * 20
        st.metric("Your EcoHero Points", eco_points)

        # Penguin Saver Marathon
    elif challenge == "Penguin Saver Marathon":
        st.header("🐧 Penguin Saver Marathon")
        st.write("""
        🐧 **Objective:** Save penguins by reducing your carbon footprint.  
        🌟 Walk, bike, or take public transport to save the ice caps!  
        """)

        distance = lengthCalculator(df)

        st.write(f"Total eco-friendly distance traveled (in km):{distance / 5}")
        penguins_saved = int(distance / 5)  # Each 5 km saves 1 penguin
        st.metric("Penguins Saved", penguins_saved)

    # Carbon Ninja Challenge
    elif challenge == "Carbon Ninja Challenge":
        st.header("🥷 Carbon Ninja Challenge")
        st.write("""
        🥷 **Objective:** Become a stealthy Carbon Ninja by leaving the smallest footprint.  
        🌟 Combine modes creatively to minimize CO₂ emissions!  
        """)
        
        modes = df['Mode'].unique()
        car_mode_count = 0
        if 'car' in modes:
            car_mode_count = 1
        amount_of_modes = len(modes) - car_mode_count
        amount_of_modes
        
        st.write("🌟 Modes Used:", ", ".join(amount_of_modes))
        carbon_score = len(amount_of_modes) * 10  # 10 points per mode
        st.metric("Carbon Ninja Score", amount_of_modes)

    # Mode Switch Master
    elif challenge == "Mode Switch Master":
        st.header("🤸 Mode Switch Master")
        st.write("""
        🤸 **Objective:** Use as many eco modes as possible in a single day or week.  
        🚴 Earn badges for creative and frequent switches!  
        """)
        
        switches = st.number_input("Number of mode switches in your trips today:", 0, 50, step=1)
        st.metric("Mode Switch Count", switches)
        
        if switches >= 3:
            st.success("🏅 You've unlocked the **Eco-Gymnast Badge**!")

        # Footer
        st.sidebar.title("About")
        st.sidebar.info("This app promotes eco-friendly transportation. Track your progress and compete with friends!")




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

