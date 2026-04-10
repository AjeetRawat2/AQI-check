
# Dependencies:
#     pip install Flask Flask-SQLAlchemy

# Run:
#     python app.py


from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

# Initialize App & Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///air_quality.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Model ---
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(100))
    aqi = db.Column(db.Integer)
    pm25 = db.Column(db.Float)
    pm10 = db.Column(db.Float)
    source = db.Column(db.String(50)) # Tags data as 'Real Hardware' or 'Simulated'

# Create database tables
with app.app_context():
    db.create_all()

# --- Routes ---

@app.route('/')
def dashboard():
    """Renders the main dashboard UI."""
    locations = ["Sector 29, Gurugram", "Cyber City", "Udyog Vihar", "Golf Course Road"]
    return render_template('index.html', locations=locations)

@app.route('/api/data/<location_name>')
def get_data(location_name):
    """Fetches the latest 20 readings for the charts."""
    data = SensorData.query.filter_by(location=location_name).order_by(SensorData.timestamp.desc()).limit(20).all()

    # Reverse the data so it plots left-to-right chronologically
    data = data[::-1]

    return jsonify({
        'timestamps': [d.timestamp.strftime("%H:%M:%S") for d in data],
        'aqi': [d.aqi for d in data],
        'pm25': [d.pm25 for d in data],
        'latest': {
            'aqi': data[-1].aqi if data else 0,
            'pm25': data[-1].pm25 if data else 0,
            'pm10': data[-1].pm10 if data else 0,
            'source': data[-1].source if data else "No Data"
        }
    })

@app.route('/api/ingest', methods=['POST'])
def ingest_real_data():
    """Receives REAL data from the ESP32/Arduino via HTTP POST."""
    payload = request.get_json()

    new_reading = SensorData(
        location=payload.get('location', 'Unknown Node'),
        aqi=payload.get('aqi', 0),
        pm25=payload.get('pm25', 0.0),
        pm10=payload.get('pm10', 0.0),
        source='Real Hardware' # Tagged as real hardware
    )
    db.session.add(new_reading)
    db.session.commit()

    return jsonify({"status": "success", "message": "Real data saved!"})

@app.route('/api/simulate', methods=['POST'])
def generate_simulated_data():
    """Generates FAKE data when the UI Simulation toggle is active."""
    payload = request.get_json()
    location = payload.get('location', 'Unknown Node')

    # Generate realistic random data
    new_reading = SensorData(
        location=location,
        aqi=random.randint(50, 180),
        pm25=round(random.uniform(20.0, 80.0), 1),
        pm10=round(random.uniform(40.0, 120.0), 1),
        source='Simulated' # Tagged as simulated
    )
    db.session.add(new_reading)
    db.session.commit()

    return jsonify({"status": "success", "message": "Simulated data saved!"})

if __name__ == '__main__':
    # host='0.0.0.0' allows devices on your local Wi-Fi to send data to the server
    app.run(host='0.0.0.0', debug=True, port=5000)
