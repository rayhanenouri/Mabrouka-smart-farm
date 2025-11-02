#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MABROUKA'S FRIENDLY WATERING HELPER
Morning: Tonight's plan
Evening/Night: Tomorrow's plan
Refreshes every minute
"""

import requests
import time
from datetime import datetime, timedelta
import os

# CONFIG
API_KEY = "edb46e2a9c6cebe71bb21568df0fdc74"
LAT, LON = 36.4, 10.15
FORECAST_URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

# Crop areas (m²)
AREA = {"tomatoes": 20, "onions": 15, "mint": 10}

# Water needs per stage (L/m²)
WATER_NEEDS = {
    "tomatoes": {"seedling": 2, "vegetative": 4, "flowering": 5},
    "onions":   {"seeding": 1.5, "bulbing": 3},
    "mint":     {"vegetative": 2, "flowering": 3},
}

# Current growth stage (CHANGE WHEN NEEDED)
STAGE = {
    "tomatoes": "vegetative",
    "onions": "bulbing",
    "mint": "vegetative",
}

# Fetch 5-day forecast
def get_forecast():
    try:
        r = requests.get(FORECAST_URL, timeout=10)
        if r.status_code == 200:
            return r.json()
        print(f"API error: {r.status_code}")
    except:
        pass
    return None

# Get tomorrow or tonight's weather (evening: 18:00–21:00)
def get_target_weather(forecast):
    if not forecast or "list" not in forecast:
        return None

    now = datetime.now()
    is_morning = now.hour < 12  # Before noon
    target_date = now.date() if is_morning else (now + timedelta(days=1)).date()
    evening_start = f"{target_date} 18:00:00"
    evening_end = f"{target_date} 21:00:00"

    evening_items = []
    for item in forecast["list"]:
        dt = item["dt_txt"]
        if evening_start <= dt <= evening_end:
            evening_items.append(item)

    if not evening_items:
        return None

    temps = [item["main"]["temp"] for item in evening_items]
    hums = [item["main"]["humidity"] for item in evening_items]
    rains = [item.get("rain", {}).get("3h", 0) for item in evening_items]
    pop = max(item.get("pop", 0) for item in evening_items)

    return {
        "avg_temp": sum(temps) / len(temps),
        "avg_hum": sum(hums) / len(hums),
        "total_rain": sum(rains),
        "rain_prob": pop,
    }

# Decide if crop needs water tonight/tomorrow
def needs_water(crop, weather):
    if not weather:
        return False, 0
    temp = weather["avg_temp"]
    hum = weather["avg_hum"]
    rain = weather["total_rain"]
    pop = weather["rain_prob"]

    need = WATER_NEEDS[crop][STAGE[crop]]
    litres = round(need * AREA[crop], 1)

    thirsty = (temp > 26 and hum < 65) or (temp > 28)
    rain_coming = rain > 0.5 or pop > 0.3

    if rain_coming:
        return False, 0
    if thirsty:
        return True, litres
    return False, 0

# Main loop
def main():
    print("Mabrouka's Watering Helper Starting... (refreshing every minute)\n")
    
    while True:
        forecast = get_forecast()
        weather = get_target_weather(forecast)

        now = datetime.now()
        is_morning = now.hour < 12
        time_word = "Tonight" if is_morning else "Tomorrow"
        icon = "Sun" if is_morning else "Moon"

        crops_to_water = []
        total_l = 0

        for crop in ["tomatoes", "onions", "mint"]:
            water, litres = needs_water(crop, weather)
            if water:
                name = crop.replace("tomatoes", "Tomatoes").replace("onions", "Onions").replace("mint", "Mint")
                crops_to_water.append(f"{name}: {litres}L")
                total_l += litres

        # Build friendly message
        if not weather:
            msg = f"{icon} No weather data yet... checking again!"
        elif crops_to_water:
            what = ", ".join(crops_to_water)
            msg = f"{icon} **{time_word}: WATER!**\nWater drop {what}\nTotal: {total_l}L"
        else:
            msg = f"{icon} **{time_word}: NO WATER NEEDED**\nLeaf All good! Rest or feed chickens."

        # Clear screen + print
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*50)
        print("     MABROUKA'S WATERING HELPER")
        print("="*50)
        print(f"   {datetime.now().strftime('%A, %I:%M %p')}")
        print()
        print(msg.replace("Water drop", "Water").replace("Leaf", "Leaf"))
        print()
        print("Refreshes every minute... Ctrl+C to stop")
        print("="*50)

        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nStopped. See you tomorrow, Mabrouka!")