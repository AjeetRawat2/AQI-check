from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# --- IN-MEMORY SENSOR DATA STORE ---
# For production, replace this with a database like Azure SQL or PostgreSQL.
# Adding some initial mock data so the charts look good immediately.
sensor_data_store = []
now = datetime.now()
for i in range(10, 0, -1):
    time_str = (now - timedelta(minutes=i*5)).strftime("%H:%M")
    sensor_data_store.append({
        "aqi": 110 + (i % 3) * 5, 
        "pm25": 40 + i, 
        "temp": 24.5, 
        "timestamp": time_str
    })

@app.route('/')
def index():
    """Render the main dashboard UI."""
    return render_template('index.html')

@app.route('/api/external-aqi')
def get_external_aqi():
    """
    Fetch AQI data from an external API (e.g., WAQI - World Air Quality Index).
    You can pass the city as a query parameter: /api/external-aqi?city=London
    """
    city = request.args.get('city', 'Delhi')
    # Use environment variables to store your API keys securely in Azure
    token = os.environ.get('WAQI_TOKEN', 'demo') 
    
    # If using the default 'demo' token, we'll return mock data so the app doesn't crash 
    # while you are testing without a real API key.
    if token == 'demo':
        return jsonify({
            "status": "success",
            "source": "Mock API (No Token Provided)",
            "data": {
                "aqi": 152,
                "city": city,
                "pm25": 56,
                "pm10": 90,
                "temp": 26,
                "humidity": 55
            }
        })

    # Real API Call Logic
    url = f"https://api.waqi.info/feed/{city}/?token={token}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        waqi_data = response.json()
        
        # Parse the WAQI response into our unified format
        if waqi_data.get('status') == 'ok':
            return jsonify({
                "status": "success",
                "source": "WAQI API",
                "data": {
                    "aqi": waqi_data['data']['aqi'],
                    "city": waqi_data['data']['city']['name'],
                    "pm25": waqi_data['data']['iaqi'].get('pm25', {}).get('v', 'N/A'),
                    "pm10": waqi_data['data']['iaqi'].get('pm10', {}).get('v', 'N/A'),
                    "temp": waqi_data['data']['iaqi'].get('t', {}).get('v', 'N/A'),
                    "humidity": waqi_data['data']['iaqi'].get('h', {}).get('v', 'N/A')
                }
            })
        else:
            return jsonify({"status": "error", "message": "City not found or invalid token"}), 404
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/sensor', methods=['GET', 'POST'])
def handle_sensor_data():
    """
    Endpoint for physical IoT sensors to push data (POST) 
    and for the frontend to retrieve historical data (GET).
    """
    if request.method == 'POST':
        data = request.json
        if not data or 'aqi' not in data:
            return jsonify({"status": "error", "message": "Invalid data format"}), 400
            
        data['timestamp'] = datetime.now().strftime("%H:%M")
        sensor_data_store.append(data)
        
        # Keep only the latest 50 readings in memory to prevent overflow
        if len(sensor_data_store) > 50:
            sensor_data_store.pop(0)
            
        return jsonify({"status": "success", "message": "Sensor data recorded successfully"}), 201
        
    else:
        # GET request: return the data for charts
        return jsonify({
            "status": "success", 
            "data": sensor_data_store,
            "latest": sensor_data_store[-1] if sensor_data_store else None
        })

if __name__ == '__main__':
    # Run locally on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)