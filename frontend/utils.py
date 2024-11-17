import pandas as pd

def lengthCalculator(df: pd.DataFrame):
    length = (df['Length'].sum())/1000
    return length

def moneySavedPetrol(length: float):
    convert_gas = (length * 12 * 1.74)/100
    return convert_gas

def moneySavedElectric(length: float):
    convert_energy = length * 0.18 * 0.79
    return convert_energy