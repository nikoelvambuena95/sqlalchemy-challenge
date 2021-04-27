import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
dbPath = "Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{dbPath}")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/MM-DD-YYYY/<br/>"
        f"/api/v1.0/MM-DD-YYYY/MM-DD-YYYY>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server access precipitation data")
    s = Session(engine)
    
    # Precipitation query
    results =  s.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date.between('2016-08-23', '2017-08-23')).\
    order_by('date').all()

    s.close()

    # Create dictionary from the data and append to list 'prcp_data'
    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def station():
    print("Server access stations data")
    s = Session(engine)

    # Station query
    results = s.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()

    s.close()

    # Create dictionary from the data and append to list 'station_data'
    station_data = []
    for station, count in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["count"] = count
        station_data.append(station_dict)
    
    return jsonify(station_data)

# @app.route("/api/v1.0/tobs")
# def temperature():
#     return (
#         print("Server access temperature data")
#     )

if __name__ == '__main__':
    app.run(debug=True)
