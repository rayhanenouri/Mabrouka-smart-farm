import pandas as pd

# === 1. LOAD CSV ===
file_path = "zaghouan_historical_raw.csv"
df = pd.read_csv(file_path, skiprows=10, header=None)  # No header

# === 2. DEBUG: Show raw data ===
print("Raw data preview:")
print(df.head(2))
print(f"Columns count: {len(df.columns)}")

# === 3. ASSIGN COLUMNS MANUALLY (7 columns) ===
df.columns = [
    'timestamp_raw', 'temperature', 'precipitation', 'basel', 
    'humidity', 'wind_direction', 'cloud_cover'
]

# === 4. CONVERT TIMESTAMP ===
df['timestamp'] = pd.to_datetime(df['timestamp_raw'], format='%Y%m%dT%H%M', errors='coerce')
df = df.dropna(subset=['timestamp'])

# === 5. KEEP ONLY NEEDED ===
df = df[['timestamp', 'temperature', 'humidity', 'precipitation']]
df = df.rename(columns={'precipitation': 'rain_mm'})

# === 6. CLEAN NUMERIC ===
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')
df['rain_mm'] = pd.to_numeric(df['rain_mm'], errors='coerce')
df = df.dropna()

# === 7. ADD LABEL: water_needed (simplified — no wind speed) ===
df['water_needed'] = (
    (df['temperature'] > 25) &
    (df['humidity'] < 60) &
    (df['rain_mm'] == 0)
).astype(int)

# === 8. SAVE ===
df.to_csv("zaghouan_clean.csv", index=False)
print("\nCLEANING SUCCESS!")
print(f"Rows: {len(df)} | Water needed: {df['water_needed'].sum()} times")
print(df.head())