import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import requests

st.set_page_config(
    layout = 'wide',
    page_title = 'MFT'
)

# with st.sidebar:
selected = option_menu(
    menu_title= None,
    options=["Home", "Maps", "Achievments"],
    icons=["house", "book", "activity"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

def copyAndFill(toFill:any, toFillWith:any):
    copyToFillWith = toFillWith.copy()
    copyToFillWith ['CO2_kg'] = 0
    new = pd.concat([toFill,], ignore_index=True)
    return new


# HOME
if selected == "Home":
    """
    # Welcome to MFT 

    EDIT INFO:

    """
    # df = pd.DataFrame('ID_163')
    df = pd.read_csv("./content/ID_163.csv")
    # df = pd.DataFrame({'ID': ['ID_163']})
    df['StartedAt_Timestamp'] = pd.to_datetime(df['StartedAt_Timestamp'])

    car_data = df[df['Mode'] == "car"]
    non_car_data = df[df['Mode'] != "car"]
    filled_car_data = copyAndFill(car_data, non_car_data)
    filled_non_car_data = copyAndFill(non_car_data, car_data)

    st.write(filled_car_data)
    non_car_data = df[df['Mode'] != "car"]
    # st.write(non_car_data)


    # Align the 'CO2_kg' values with their respective timestamps
    car_data = car_data[['StartedAt_Timestamp', 'CO2_kg']].set_index('StartedAt_Timestamp')
    non_car_data = non_car_data[['StartedAt_Timestamp', 'CO2_kg']].set_index('StartedAt_Timestamp')


    data = pd.DataFrame(
        {
        "col1": df[df['Mode']=="car"],
        "col2": df[df['Mode']!="car"],
		}
    )
    # chart_data = pd.DataFrame(df,columns=("StartedAt_Timestamp", "CO2_kg"))
    # st.area_chart(data, x="StartedAt_Timestamp", y="CO2_kg")
    st.area_chart(df[['StartedAt_Timestamp', 'CO2_kg']], x="StartedAt_Timestamp", y="CO2_kg")

    


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

