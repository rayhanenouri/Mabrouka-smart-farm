# 🌱 Mabrouka's Smart Farm - WiEmpower 2.0

## Smart Irrigation System for Small-Scale Farmers

### Team Members
- [FaraTech]
- [Rayhane Nouri]
- [Maram Hammami]
- [Asma Hmaied]
- [Rayen Romdhane]
- [Ouday Bouazzi]

### Problem Statement
Helping small-scale farmers like Mabrouka manage water efficiently through IoT simulation and AI prediction.

| Feature | Description |
|-------|-----------|
| 📊**Real-time Monitoring** | Soil moisture, hours until dry, pump status |
| **Weather Integration** | OpenWeatherMap API (temp, humidity, wind, rain) |
| 🔮**Smart Forecast** | "Tonight: WATER!" or "All good!" |
| **Auto Pump Control** | Turns ON/OFF based on soil & weather |
| **Pro Alerts** | Top-right animated banner: "The land needs water" |
| **Crop Selection** | Click Tomato / Onion / Mint |
| 🌐**Droplet Animations** | Rain effect when pump is ON |
| **Responsive Design** | Works on mobile & desktop |
| 🔮**Test Page** | `/test` – simulate sensor input |

### Tech Stack
- **Backend:** Python, Flask, SQLite
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **AI/ML:** Scikit-learn, Pandas
- **Database:** SQLite

### Project Structure
```
mabrouka-smart-farm/
├── backend/
│   ├── sensor_simulator.py
│   ├── pump_controller.py
│   ├── app.py
│   └── predictor.py
│   ├── index.html
├── docs/
└── README.md
```
## How It Works

1. **Weather API** → gets current + forecast
2. **ET₀ Model** → calculates water loss
3. **Soil Simulation** → estimates moisture
4. **Decision Engine** → "Need water?" → Pump ON
5. **Frontend** → updates every 10s
### Installation
```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/mabrouka-smart-farm.git
cd mabrouka-smart-farm

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the sensor simulator
python backend/sensor_simulator.py

# Run the web server
python backend/app.py
```

### Missions Completed
- ✅ Mission 1: Soil Moisture Monitoring
- ✅ Mission 2: Smart Pump Control
- ✅ Mission 3: Remote Dashboard
- ✅ Mission 4: AI Predictions

### Demo
[Link to demo video - Coming soon]

### WiEmpower 2.0 Hackathon
Event: November 1-2, 2025  
Location: SUP'COM, Technopole El Ghazela  
Organized by: IEEE WIE Affinity Group Sup'Com
