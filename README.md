# Eco Charge

## Overview
Eco Charge is a Flask-based web application designed to help users locate electric vehicle (EV) charging stations, calculate charging costs, and navigate to stations using interactive maps. The project integrates Flask, SQLite, Leaflet.js, and Google Maps for an intuitive user experience.

## Features
- **EV Charging Station Locator**: Find nearby charging stations based on location.
- **Charging Cost Estimation**: Select a charger type and enter units to calculate cost.
- **Interactive Map**: Displays charging stations and allows selection.
- **Google Maps Integration**: Navigate to the selected charging station.
- **Database Management**: Stores charging station details using Flask-SQLAlchemy.

## Project Structure
```
EcoCharge/

│-- backend.py             # Main Flask application
│-- templates/
│   │-- index.html         # Home page with map and search functionality
│   │-- charger.html       # Select charger type and input units
│   │-- charging_cost.html # Displays calculated charging cost and time
│   │-- charger_details.html # Charger information page
│-- static/
│   │-- image.jpeg         # Logo and other static assets
│-- ecocharge_project.docx # Mini project report
│-- README.md              # Project documentation
│-- requirements.txt       # Python dependencies
```

## Installation
### Prerequisites
- Python 3.x
- Flask
- Flask-SQLAlchemy
- SQLite
- Leaflet.js (CDN included in HTML)

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/ecocharge.git
   cd ecocharge
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python app.py
   ```
4. Open a browser and go to:
   ```sh
   http://127.0.0.1:5000/
   ```

## Usage
- **Search for charging stations** by entering a location in the search bar.
- **Select a charger type** and enter units to calculate cost.
- **View estimated cost and time** before proceeding to charge.
- **Click on "Get Directions"** to navigate using Google Maps.

## Technologies Used
- **Flask** (Backend framework)
- **SQLite** (Database management)
- **Flask-SQLAlchemy** (ORM for database interaction)
- **Leaflet.js** (Interactive map integration)
- **HTML, CSS, JavaScript** (Frontend UI/UX)
- **Google Maps API** (Navigation support)

## Future Enhancements
- User authentication for personalized experiences.
- Real-time station availability updates.
- Mobile app version.
- EV trip planner



## Contributors
- Mohammed Nomaan
- Mohammed Muneeb Ur Rahaman
- Kogooru Bhargavi
