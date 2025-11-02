import requests
import json
import time

API_URL = "http://localhost:5000/api/sensor_in"

# --- Test Data ---
DRY_DATA = {
    "soil_moisture": 15.0,
    "status": "water now"
}

WET_DATA = {
    "soil_moisture": 75.0,
    "status": "Good"
}

def send_test_data(data, test_name):
    """Sends POST request to Flask and prints the result."""
    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        
        # FIX: Directly log the intended action (what we sent) instead of relying on
        # the pump_status key in the server's immediate confirmation response.
        sent_status = "ON" if data['status'] == 'water now' else "OFF"
        
        print(f"[{time.strftime('%H:%M:%S')}] {test_name}: Sent {data['status']}, Pump command SENT: {sent_status}")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ CONNECTION ERROR: Failed to reach {API_URL}. Ensure 'python app.py' is running.")
        print(f"   Error details: {e}")
        # Stop the script if connection fails
        exit()

# --- Looping Execution ---
if __name__ == "__main__":
    print("Starting Autonomous State-Holding Cycle Test...")
    
    # 0. Initial State: Force Pump OFF
    print("\n--- INITIALIZING: Ensuring pump is OFF before starting. ---")
    send_test_data(WET_DATA, "Initial State (Force OFF)")
    time.sleep(15)
    
    # 1. PHASE: Water Now (Dry) - Pump turns ON and stays ON
    print("\n\n--- PHASE 1: SIMULATING PROLONGED DROUGHT ('water now' for a while) ---")
    print("   PUMP SHOULD TURN ON on the first cycle and remain ON.")
    
    for i in range(1, 4):
        send_test_data(DRY_DATA, f"DRY CYCLE {i}/3: Send 'water now'")
        time.sleep(15)
        
    print("\nFinished 3 dry cycles. Pump should now be confirmed ON on the dashboard.")
    time.sleep(15)
    
    # 2. PHASE: Good (Wet) - Pump turns OFF and stays OFF
    print("\n\n--- PHASE 2: SIMULATING IRRIGATION COMPLETE ('Good' for a while) ---")
    print("   PUMP SHOULD TURN OFF on the first cycle and remain OFF.")
    
    for i in range(1, 4):
        send_test_data(WET_DATA, f"WET CYCLE {i}/3: Send 'Good'")
        time.sleep(15)
        
    print("\nFinished 3 wet cycles. Pump should now be confirmed OFF on the dashboard.")
    
    print("\nTest sequence complete. Run the script again to repeat the full cycle.")
