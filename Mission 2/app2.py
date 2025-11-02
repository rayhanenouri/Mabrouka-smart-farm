from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
# Crucial for allowing your HTML to make requests to the API
CORS(app) 

# --- CONFIGURATION & GLOBAL STATE ---
# These two variables now represent the definitive state of the system
PUMP_STATUS = "OFF"
FLASH_MESSAGE = "System awaiting initial sensor data."

# THE GLOBAL DATA STORE (Stores the LATEST received reading)
LATEST_DATA = {
    "soil_moisture": 50.0, # Start with a good value
    "soil_status_text": "Initial Check (Good)", 
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}


# --- MISSION 1: DATA IN (Your friend's code POSTs to this) ---
@app.route('/api/sensor_in', methods=['POST'])
def receive_sensor_data():
    """
    Receives the latest soil status and moisture reading.
    CRITICALLY: This function now contains the full autonomous pump control logic.
    """
    global LATEST_DATA, PUMP_STATUS, FLASH_MESSAGE
    
    try:
        data = request.get_json()
        new_moisture = float(data.get('soil_moisture')) 
        # Normalize incoming status for reliable comparison
        new_status = data.get('status', 'Status not provided').strip().lower()
        
        # 1. Update the "database"
        LATEST_DATA["soil_moisture"] = round(new_moisture, 1)
        LATEST_DATA["soil_status_text"] = new_status
        LATEST_DATA["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 2. AUTONOMOUS PUMP LOGIC (The new requirement)
        if new_status == "water now" and PUMP_STATUS == "OFF":
            PUMP_STATUS = "ON"
            FLASH_MESSAGE = "✅ **Autonomous Action:** Your land needed water, so we opened the pump."
        elif new_status == "good" and PUMP_STATUS == "ON":
            PUMP_STATUS = "OFF"
            FLASH_MESSAGE = "💧 **Autonomous Action:** Your land is watered, so we closed the pump."
        # Keep the existing message if no state change occurred, but reflect current status
        elif new_status == "water now" and PUMP_STATUS == "ON":
            FLASH_MESSAGE = "Autonomous Monitoring: Pump remains ON as land still requires water."
        elif new_status == "good" and PUMP_STATUS == "OFF":
            FLASH_MESSAGE = "Autonomous Monitoring: Pump remains OFF as land is sufficiently watered."
        else:
            FLASH_MESSAGE = f"Autonomous Monitoring: Sensor status '{new_status}' received. No pump status change required."
        
        return jsonify({"message": "Sensor data updated successfully.", "pump_status": PUMP_STATUS}), 200
    except Exception as e:
        return jsonify({"error": f"Invalid data format or missing required fields: {e}"}), 400


# --- MISSION 2: COMMAND OUT (The Pump Hardware Client reads this) ---
@app.route('/api/pump_command', methods=['GET'])
def pump_command_endpoint():
    """Endpoint for the pump hardware client to read the final command."""
    return jsonify({
        "time": LATEST_DATA["time"],
        "pump_status": PUMP_STATUS, 
        "reason": FLASH_MESSAGE
    })


# --- MISSION 3: WEB DISPLAY STATUS (Consolidated endpoint for the Dashboard) ---
@app.route('/api/status', methods=['GET'])
def get_dashboard_status():
    """Returns a consolidated JSON object for the Web Dashboard to display."""
    
    return jsonify({
        "time": LATEST_DATA["time"],
        "pump_status": PUMP_STATUS,
        "soil_moisture": f"{LATEST_DATA['soil_moisture']:.1f}%",
        "reason": FLASH_MESSAGE, # Now directly serves the flash message
        "location": "Zaghouan, Tunisia"
    })

# --- START THE APP ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)