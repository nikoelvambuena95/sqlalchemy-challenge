import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from dateutil import parser

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
        f"/api/v1.0/'Starting Date'"
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
    results = s.query(Station.station).all()

    s.close()

    # Convert list of tuples into normal list
    station_data = list(np.ravel(results))

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def temperature():
    print("Server access temperature data")
    s = Session(engine)

    # Temperature query
    results = s.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281', Measurement.date.between('2016-08-23', '2017-08-23')).\
    order_by('date').all()

    s.close()

    # Create dictionary from the data and append to list 'tobs_data'
    tobs_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start_date>")
def temp_date(start_date):

    for x in start_date.splitlines():
        date = parser.parse(x)
        mod_date = date.strftime("%Y-%m-%d")

    s = Session(engine)
    
    sel = [Measurement.date,
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.avg(Measurement.tobs)]
       
    results = s.query(*sel).filter(Measurement.date >= mod_date).group_by(Measurement.date).all()

    s.close()

    tempDate_list = []
    for date, min, max, avg in results:
        tempDate_dict = {}
        tempDate_dict["date"] = date
        tempDate_dict["min"] = min
        tempDate_dict["max"] = max
        tempDate_dict["avg"] = avg
        tempDate_list.append(tempDate_dict)
    
    return jsonify(tempDate_list)

if __name__ == '__main__':
    app.run(debug=True)
