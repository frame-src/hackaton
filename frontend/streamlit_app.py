import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta

st.set_page_config(
    layout='wide',
    page_title='MFT'
)

# with st.sidebar:
selected = option_menu(
    menu_title=None,
    options=["Home", "Maps", "Achievments"],
    icons=["house", "book", "activity"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

def copyAndFill(toFill: any, toFillWith: any):
    copyToFillWith = toFillWith.copy()
    copyToFillWith['CO2_kg'] = 0
    new = pd.concat([toFill,], ignore_index=True)
    return new

# HOME
if selected == "Home":
    """
    # Welcome to MFT
    """

    # Read the CSV file
    df = pd.read_csv("./content/ID_163.csv")
    df['StartedAt_Timestamp'] = pd.to_datetime(df['StartedAt_Timestamp'])

    # Adjust CO2_kg for 'car' mode
    for _, row in df.iterrows():
        if row['Mode'] == 'car':
            df.at[_, 'CO2_kg'] = row['CO2_kg'] 
        else:
            df.at[_, 'CO2_kg'] = row['CO2_kg'] * -15

    # Get the minimum and maximum timestamps for the whole day
    min_timestamp = df['StartedAt_Timestamp'].min().replace(hour=4, minute=0, second=1)
    max_timestamp = df['StartedAt_Timestamp'].max().replace(hour=20, minute=59, second=59)

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
		align='left', dx=5, dy=-5, color='black'
	).encode(
		y='y:Q',
		text='text:N'
	)
    chart = alt.layer(area_chart, rule, text)
    st.altair_chart(chart, use_container_width=True)

# MAPS
if selected == "Maps":
    st.title("MAPS")





#PROFILE or ACTIVITIES or ACHIEVMENTS
if selected == "Achievments":
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

