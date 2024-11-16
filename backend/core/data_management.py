import pandas as pd
import json



def loadData():
    df = pd.read_csv('/content/data.csv')

    # Parse the 'Geometry3_JSON' column (convert it from a JSON string to a Python dictionary)
    # df['Geometry3_JSON'] = df['Geometry3_JSON'].apply(json.loads)

    # # Optional: Extract 'coordinates' and 'type' into separate columns
    # df['coordinates'] = df['Geometry3_JSON'].apply(lambda x: x['coordinates'])
    # df['geometry_type'] = df['Geometry3_JSON'].apply(lambda x: x['type'])

    # # Drop 'Geometry3_JSON' column if it's not needed anymore
    # df.drop(columns=['Geometry3_JSON'], inplace=True)

    return(df.head())