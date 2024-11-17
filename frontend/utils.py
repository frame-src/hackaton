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

import random

def foodAmountForCalories(km: float):
    # Calories burned per km (assuming walking)
    calories_per_km = 50
    total_calories = km * calories_per_km
    
    # Calorie content per 100g for different foods (in kcal)
    foods = {
        "Apple": 52,  # kcal per 100g
        "Banana": 89,  # kcal per 100g
        "Chocolate": 546,  # kcal per 100g
        "Carrot": 41,  # kcal per 100g
        "Pizza": 266  # kcal per 100g
    }
    
    # Randomly select a food
    selected_food = random.choice(list(foods.keys()))
    
    # Calculate the amount of selected food based on calories burned
    food_calories = foods[selected_food]
    amount_in_grams = (total_calories / food_calories) * 100
    
    return f"You can eat {amount_in_grams:.2f} grams of {selected_food} after walking {km} km."


def hoursOutdoors(km: float, avg_speed: float):
    # avg_speed is the average speed in km/h
    hours = km / avg_speed
    return hours

def caloriesBurned(km: float):
    # Average calories burned per km, assuming walking (around 50 kcal per km)
    calories_per_km = 50  
    total_calories = km * calories_per_km
    return total_calories

