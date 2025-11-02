import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# === 1. LOAD CLEAN DATA ===
df = pd.read_csv("zaghouan_clean.csv")
print(f"Loaded {len(df)} rows")

# === 2. FEATURES & TARGET ===
X = df[['temperature', 'humidity', 'rain_mm']]  # Input
y = df['water_needed']                          # Output

# === 3. SPLIT DATA ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === 4. TRAIN MODEL ===
model = LogisticRegression()
model.fit(X_train, y_train)

# === 5. EVALUATE ===
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nMODEL ACCURACY: {accuracy:.2%}")

print("\nWhen it predicts 'water':")
print(classification_report(y_test, y_pred))

# === 6. SAVE MODEL ===
joblib.dump(model, "irrigation_model.pkl")
print("\nMODEL SAVED → irrigation_model.pkl")