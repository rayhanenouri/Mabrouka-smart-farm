import requests
from math import exp
from datetime import datetime
import time

# === CONFIG ===
API_KEY = "edb46e2a9c6cebe71bb21568df0fdc74"  # your valid OpenWeather key
LAT = 36.4
LON = 10.15
URL = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

# === Crop Parameters ===
CROP_PARAMS = {
    "tomato": {
        "seedling": {"root_depth_cm": 15, "kc": 0.6, "theta_crit": 0.20},
        "vegetative": {"root_depth_cm": 30, "kc": 0.9, "theta_crit": 0.18},
        "flowering": {"root_depth_cm": 40, "kc": 1.1, "theta_crit": 0.17},
    },
    "onion": {
        "seedling": {"root_depth_cm": 10, "kc": 0.7, "theta_crit": 0.22},
        "bulbing": {"root_depth_cm": 25, "kc": 1.0, "theta_crit": 0.20},
    },
    "mint": {
        "vegetative": {"root_depth_cm": 20, "kc": 1.0, "theta_crit": 0.25},
        "flowering": {"root_depth_cm": 25, "kc": 1.1, "theta_crit": 0.22},
    },
}

# === Helper physics functions ===
def sat_vapor_pressure(temp_C):
    """Saturation vapor pressure (kPa)"""
    return 0.6108 * exp((17.27 * temp_C) / (temp_C + 237.3))

def vpd_from_temp_rh(temp_C, rh_pct):
    """Vapor Pressure Deficit (kPa)"""
    es = sat_vapor_pressure(temp_C)
    ea = (rh_pct / 100.0) * es
    return max(es - ea, 0.0)

def et0_vpd_wind_proxy(temp_C, rh_pct, wind_m_s):
    """Simplified ET0 estimate (mm/day) using VPD, temperature and wind."""
    k = 5.0
    alpha_wind = 0.18
    vpd = vpd_from_temp_rh(temp_C, rh_pct)
    et0 = k * vpd * (temp_C + 20) / 25 * (1 + alpha_wind * wind_m_s)
    return max(0.0, min(et0, 25.0))

# === Weather data from OpenWeather ===
def get_weather():
    """Fetches current temperature, humidity, wind speed, and rain from OpenWeather."""
    try:
        r = requests.get(URL, timeout=10)
        if r.status_code == 200:
            data = r.json()
            city = data["name"]
            temp = data["main"]["temp"]
            hum = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            rain = data.get("rain", {}).get("3h", 0)
            return temp, hum, wind, rain
        else:
            print("⚠️ Weather API error:", r.status_code, r.text)
            return None, None, None, None
    except Exception as e:
        print("❌ Connection failed:", e)
        return None, None, None, None

# === Dryness logic ===
def dryness_status(crop, stage, temp, hum, wind, rain):
    """
    Determine dryness state based on weather factors.
    """
    p = CROP_PARAMS[crop][stage]
    theta_c = p["theta_crit"]
    root_depth_mm = p["root_depth_cm"] * 10
    kc = p["kc"]

    # Estimate evapotranspiration (ET0) and effective soil moisture
    et0_mm_day = et0_vpd_wind_proxy(temp, hum, wind)
    etc_mm_hr = kc * et0_mm_day / 24.0

    # Estimate soil moisture change based on rain & evap
    base_soil_m = 0.30
    capture_eff = 0.8
    rain_vol_frac = (rain * capture_eff) / root_depth_mm
    evap_vol_frac = et0_mm_day / root_depth_mm
    soil_m = max(0.05, min(0.45, base_soil_m + rain_vol_frac - evap_vol_frac))

    diff = soil_m - theta_c

    if diff <= 0:
        
        hours_until_dry = 0
    else:
        available_mm = diff * root_depth_mm
        if etc_mm_hr <= 0:
            hours_until_dry = float("inf")
        else:
            hours_until_dry = available_mm / etc_mm_hr

        if hours_until_dry >= 6:
            status = "🌱 The land does not need water"
            
        else:
            status = "🌤 The land needs water"
            
    


    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temp": temp,
        "humidity": hum,
        "wind": wind,
        "rain": rain,
        "soil_m_est": round(soil_m, 3),
        "status": status,
        "hours_until_dry": round(hours_until_dry, 1) if hours_until_dry != float("inf") else "∞",
    }

# === Main Loop ===

# Continuous monitoring loop
while True:
    temp, hum, wind, rain = get_weather()

    if temp is not None:
        # Create list of all crops and their growth stages
        crops_to_check = []
        for crop in CROP_PARAMS:
            for growth_stage in CROP_PARAMS[crop]:
                crops_to_check.append([crop, growth_stage])
        
        # Check each crop and growth stage combination
        for crop, growth_stage in crops_to_check:
            result = dryness_status(crop, growth_stage, temp, hum, wind, rain)
            
            # Display crop, growth stage, and status in one line
            print(f"{crop.capitalize()} - {growth_stage.capitalize()}: {result['status']}")
        
        print()  # Empty line between cycles
    
    else:
        print("⚠️ Skipping this cycle due to weather API issue.\n")

    # Wait 100 seconds before next update
    time.sleep(100)
   