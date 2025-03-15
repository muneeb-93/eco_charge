from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///charging_stations.db'

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
    station_id = db.Column(db.Integer, db.ForeignKey('charging_station.id'), nullable=False)

def create_default_data():
    if ChargingStation.query.filter_by(name='Tata Power Charging Station', location='Banjara Hills').first() is None:
        station1 = ChargingStation(name='Tata Power Charging Station', location='Banjara Hills')
        charger_type1 = ChargerType(name='CCS', cost_per_kwh=18, charging_station=station1)
        charger_type2 = ChargerType(name='AC', cost_per_kwh=6, charging_station=station1)

        station2 = ChargingStation(name='Tata Charging Station', location='Somajiguda')
        charger_type3 = ChargerType(name='CCS', cost_per_kwh=20, charging_station=station2)
        charger_type4 = ChargerType(name='AC', cost_per_kwh=7, charging_station=station2)

        db.session.add_all([station1, charger_type1, charger_type2, station2, charger_type3, charger_type4])
        db.session.commit()

@app.route('/')
def index():
    charging_stations = ChargingStation.query.all()
    return render_template('index_leaf.html', charging_stations=charging_stations)

@app.route('/find_charging_stations', methods=['POST'])
def find_charging_stations():
    location = request.form.get('location')
    charging_stations = ChargingStation.query.filter(ChargingStation.location.ilike(f'%{location}%')).all() if location else []
    return render_template('index_leaf.html', charging_stations=charging_stations, entered_location=location)

@app.route('/select_charger/<int:station_id>', methods=['GET', 'POST'])
def select_charger(station_id):
    station = ChargingStation.query.get_or_404(station_id)
    if request.method == 'POST':
        charger_type_id = request.form['charger_type']
        units = request.form['units']
        charger_type = ChargerType.query.get_or_404(charger_type_id)
        charging_cost = float(units) * charger_type.cost_per_kwh
        return render_template('charging_cost.html', station=station, charger_type=charger_type, units=units, charging_cost=charging_cost)
    return render_template('select_charger.html', station=station)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_data()
    app.run(debug=True)
