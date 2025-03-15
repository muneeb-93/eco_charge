from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///charging_stationsfin.db'

db = SQLAlchemy(app)

class ChargingStation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    charger_types = db.relationship('ChargerType', backref='charging_station', lazy=True)

class ChargerType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cost_per_kwh = db.Column(db.Float, nullable=False)
    charging_rate = db.Column(db.Float, nullable=False)  
    station_id = db.Column(db.Integer, db.ForeignKey('charging_station.id'), nullable=False)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    battery_capacity = db.Column(db.Float, nullable=False)

def create_default_data(station_data):
    if not ChargingStation.query.all():
        vehicles_data = [
            {'battery_capacity': 60},
            {'battery_capacity': 75},
        ]

        for vehicle_info in vehicles_data:
            vehicle = Vehicle(battery_capacity=vehicle_info['battery_capacity'])
            db.session.add(vehicle)

        for station_info in station_data:
            station = ChargingStation(name=station_info['name'], location=station_info['location'])
            for charger_info in station_info['chargers']:
                charger_type = ChargerType(
                    name=charger_info['name'], 
                    cost_per_kwh=charger_info['cost_per_kwh'], 
                    charging_rate=charger_info['charging_rate'], 
                    charging_station=station
                )
                db.session.add(charger_type)
            db.session.add(station)
        db.session.commit()

@app.route('/')
def index():
    charging_stations = ChargingStation.query.all()
    return render_template('practice.html', charging_stations=charging_stations)

@app.route('/find_charging_stations', methods=['POST'])
def find_charging_stations():
    location = request.form.get('location')
    charging_stations = ChargingStation.query.filter(ChargingStation.location.ilike(f'%{location}%')).all() if location else []
    return render_template('practice.html', charging_stations=charging_stations, entered_location=location)

@app.route('/select_charger/<int:station_id>', methods=['GET', 'POST'])
def select_charger(station_id):
    station = ChargingStation.query.get_or_404(station_id)
    if request.method == 'POST':
        charger_type_id = request.form['charger_type']
        units = float(request.form['units'])
        battery_capacity = float(request.form['battery_capacity'])
        charger_type = ChargerType.query.get_or_404(charger_type_id)
        charging_cost = units * charger_type.cost_per_kwh
        charging_time = (battery_capacity * 60) / charger_type.charging_rate
        return render_template('charging_cost.html', station=station, charger_type=charger_type, units=units, charging_cost=charging_cost, charging_time=charging_time)
    return render_template('select_charger.html', station=station)

@app.route('/charger_details')
def charger_details():
    return render_template('charger_details.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_data([
            {
                'name': 'Tata Power Charging Station',
                'location': 'Banjara Hills',
                'chargers': [
                    {'name': 'CHAdemo', 'cost_per_kwh': 18, 'charging_rate': 50},
                    {'name': 'AC', 'cost_per_kwh': 6, 'charging_rate': 20}
                ]
            },
            {
                'name': 'Tata Charging Station',
                'location': 'Somajiguda',
                'chargers': [
                    {'name': 'CCS', 'cost_per_kwh': 20, 'charging_rate': 60},
                    {'name': 'AC', 'cost_per_kwh': 7, 'charging_rate': 25}
                ]
            },
            {
                'name': 'Charge And Drive Charging Station',
                'location': 'Attapur',
                'chargers': [
                    {'name': 'CCS', 'cost_per_kwh': 20, 'charging_rate': 60},
                    {'name': 'AC', 'cost_per_kwh': 7, 'charging_rate': 25}
                ]
            }
        ])
    app.run(debug=True)
