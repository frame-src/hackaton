import pandas as pd
import json

from core.co2_calc import calc_co2

async def loadData():
    df = pd.read_csv('./content/data.csv')
    df['Geometry3_JSON'] = df['Geometry3_JSON'].apply(json.loads)
    # calculation(df)
    df = df.drop(index=df.index[0]).reset_index(drop=True)
    result = calc_co2(df)
    return result
    print(df.head(3))
    return df.head(3).to_dict(orient='records')
    return(df.head())