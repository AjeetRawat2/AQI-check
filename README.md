# 🌍 AQI Check | Air Quality Monitoring System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask">
  <img src="https://img.shields.io/badge/SQLite-Database-07405E?logo=sqlite&logoColor=white">
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-red">
  <img src="https://img.shields.io/badge/ESP32-Hardware-green">
</p>

<p align="center">
  A Flask-based <b>Air Quality Monitoring System</b> designed to collect, store, and visualize AQI and particulate matter readings from real hardware or simulated sensor data.
</p>

---

## 🌱 About The Project

**AQI Check** is an air-quality monitoring application built using **Python, Flask, Flask-SQLAlchemy, and SQLite**.

The system is designed to receive environmental readings from hardware such as an **ESP32/Arduino**, store those readings in a database, and provide the latest data to a web dashboard through REST API endpoints.

It also includes a **simulation mode**, allowing the application to generate sample AQI data without requiring physical hardware.

This makes it useful for both:

* 🔌 Real hardware testing
* 💻 Software development without sensors

---

## ✨ Features

* 🌍 Monitor Air Quality Index (AQI)
* 🌫️ Track PM2.5 readings
* 💨 Track PM10 readings
* 📍 Monitor multiple locations
* 🔌 Receive real sensor data through HTTP POST
* 🧪 Built-in simulated sensor data
* 🗄️ Store readings using SQLite
* ⚡ REST API powered by Flask
* 📊 Fetch latest 20 readings for visualization
* 🕐 Automatic timestamp generation
* 🏷️ Distinguishes real and simulated readings

---

## 🛠️ Tech Stack

| Technology          | Purpose                          |
| ------------------- | -------------------------------- |
| 🐍 Python           | Backend programming              |
| 🌶️ Flask           | Web application & REST API       |
| 🗄️ SQLite          | Air-quality data storage         |
| 🔗 Flask-SQLAlchemy | Database ORM                     |
| 📡 ESP32 / Arduino  | Sensor data source               |
| 🌐 HTTP / JSON      | Hardware-to-server communication |

---

## 🏗️ System Architecture

```text
        ┌─────────────────────┐
        │   ESP32 / Arduino   │
        │      + Sensors      │
        └──────────┬──────────┘
                   │
                   │ HTTP POST / JSON
                   ▼
        ┌─────────────────────┐
        │    Flask Server     │
        │                     │
        │   /api/ingest       │
        │   /api/simulate     │
        │   /api/data         │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │       SQLite        │
        │   air_quality.db    │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │    Web Dashboard    │
        │ AQI • PM2.5 • PM10  │
        └─────────────────────┘
```

---

## 📊 Data Collected

Each sensor reading contains:

| Field       | Description                    |
| ----------- | ------------------------------ |
| `id`        | Unique database ID             |
| `timestamp` | Time when reading was recorded |
| `location`  | Sensor/node location           |
| `aqi`       | Air Quality Index              |
| `pm25`      | PM2.5 concentration            |
| `pm10`      | PM10 concentration             |
| `source`    | `Real Hardware` or `Simulated` |

---

## 📍 Available Locations

The current dashboard configuration contains:

```text
Sector 29, Gurugram
Cyber City
Udyog Vihar
Golf Course Road
```

Additional locations can easily be added to the Flask application.

---

# 🚀 Getting Started

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/AjeetRawat2/AQI-check.git
```

Move into the project directory:

```bash
cd AQI-check
```

---

## 2️⃣ Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install Flask Flask-SQLAlchemy
```

Or create a `requirements.txt` containing:

```text
Flask
Flask-SQLAlchemy
```

Then install everything with:

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run the Application

```bash
python app.py
```

The development server runs on:

```text
http://localhost:5000
```

Because the Flask application uses:

```python
app.run(host='0.0.0.0', debug=True, port=5000)
```

devices connected to the same network can communicate with the server using the computer's local IP address.

---

# 🔌 API Endpoints

## 🏠 Dashboard

```http
GET /
```

Renders the main AQI dashboard.

---

## 📊 Get Air Quality Data

```http
GET /api/data/<location_name>
```

Returns the latest **20 readings** for a particular location.

### Example

```http
GET /api/data/Cyber%20City
```

### Example Response

```json
{
  "timestamps": [
    "12:30:01",
    "12:30:10"
  ],
  "aqi": [
    95,
    102
  ],
  "pm25": [
    42.5,
    45.1
  ],
  "latest": {
    "aqi": 102,
    "pm25": 45.1,
    "pm10": 72.4,
    "source": "Real Hardware"
  }
}
```

---

# 📡 Sending Real Hardware Data

Real sensor readings are received through:

```http
POST /api/ingest
```

The ESP32/Arduino can send JSON data such as:

```json
{
  "location": "Cyber City",
  "aqi": 105,
  "pm25": 46.2,
  "pm10": 78.5
}
```

The backend automatically tags this data as:

```text
Real Hardware
```

and stores it inside the SQLite database.

---

# 🧪 Simulation Mode

Don't have the hardware connected?

No problem. AQI Check includes a built-in simulation endpoint.

```http
POST /api/simulate
```

Send:

```json
{
  "location": "Cyber City"
}
```

The server generates simulated values in the ranges used by the application:

```text
AQI     → 50 - 180
PM2.5   → 20.0 - 80.0
PM10    → 40.0 - 120.0
```

These readings are stored with:

```text
source = Simulated
```

This allows the dashboard and database functionality to be tested without connecting physical sensors. 🧪

---

# 🗄️ Database

The project uses **SQLite** through Flask-SQLAlchemy.

Database configuration:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///air_quality.db'
```

The database tables are automatically created when the application starts:

```python
with app.app_context():
    db.create_all()
```

### SensorData Model

```python
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(100))
    aqi = db.Column(db.Integer)
    pm25 = db.Column(db.Float)
    pm10 = db.Column(db.Float)
    source = db.Column(db.String(50))
```

---

# 📂 Suggested Project Structure

```text
AQI-check/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── script.js
│
└── instance/
    └── air_quality.db
```

Your exact structure may differ depending on where your frontend files are stored.

---

# 🔄 Application Flow

```text
Air Quality Sensor
        ↓
ESP32 / Arduino
        ↓
Create AQI / PM2.5 / PM10 Reading
        ↓
HTTP POST
        ↓
Flask API
        ↓
Flask-SQLAlchemy
        ↓
SQLite Database
        ↓
GET /api/data/<location>
        ↓
Web Dashboard
        ↓
AQI Visualization 📊
```

---

## 🧪 Testing Without Hardware

You can test the simulation endpoint using `curl`:

```bash
curl -X POST http://localhost:5000/api/simulate \
-H "Content-Type: application/json" \
-d "{\"location\":\"Cyber City\"}"
```

Then retrieve the stored readings:

```bash
curl "http://localhost:5000/api/data/Cyber%20City"
```

---

## 🔮 Future Improvements

* 📈 Real-time AQI graphs
* 🔄 Automatic dashboard updates
* 🗺️ Interactive pollution map
* 🌡️ Temperature and humidity monitoring
* 📱 Mobile responsive dashboard
* 🔔 Dangerous AQI alerts
* 📡 Multiple ESP32 sensor nodes
* ☁️ Cloud database integration
* 🔐 API authentication
* 📊 Historical AQI analytics
* 📥 CSV data export
* 🤖 AQI forecasting using Machine Learning

---

## ⚠️ Development Note

The current application runs Flask with:

```python
debug=True
```

This is convenient during development but should be disabled when deploying the project publicly.

---

## 👨‍💻 Author

**Ajeet Rawat**

GitHub: [@AjeetRawat2](https://github.com/AjeetRawat2)

Repository: [AQI-check](https://github.com/AjeetRawat2/AQI-check)

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Commit your changes
5. Push your branch
6. Open a Pull Request

---

## ⭐ Support

If you found this project useful or interesting, consider giving it a **⭐ Star** on GitHub.

<p align="center">
  🌱 Monitor the air. Understand the data. Breathe smarter.
</p>

<p align="center">
  Made with ❤️ using Python, Flask & ESP32
</p>
