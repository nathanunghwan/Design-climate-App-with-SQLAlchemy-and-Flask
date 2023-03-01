import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Design-climate-App-with-SQLAlchemy-and-Flask/SurfsUp/Resources/hawaii.sqlite")
#sqlite:////Users/unghwanahn/git/Design-climate-App-with-SQLAlchemy-and-Flask/SurfsUp/Resources/hawaii.sqlite
# windows--//Users/unghwanahn/git/Design-climate-App-with-SQLAlchemy-and-FlaskSurfsUp/Resources/hawaii.sqlite

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
## WORK NEEDED HERE ##
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

## WORK NEEDED HERE ##
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br>"
        f"Temperature (Time of observation): /api/v1.0/tobs<br>"
        f"Temperature stat from the start date: /api/v1.0/temp/<start><br>"
        f"Temperature stat from start to end dates: /api/v1.0/temp/<start>/<end>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    session.close()
    # Dict with date as the key and prcp as the value
    date_prcp={}
    for date, prcp in precipitation:
        date_prcp[date]=prcp 
    
    return jsonify(date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    ##stations = list(np.ravel(results))
    # create a list of dictionaries with station info using for loop 
    stations=[]
    for station, name in results:
        station_data={}
        station_data[station]=name
        stations.append(station_data)
    
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    # Identify the most active station
    most_active_st= session.query(Measurement.station, func.count(Measurement.station)).\
                                  order_by(func.count(Measurement.station).desc()).\
                                  group_by(Measurement.station).\
                                  first()[0]

    """Return the temperature observations (tobs) for previous year."""
    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the primary station for all tobs from the last year
    results_tobs = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_st).\
        filter(Measurement.date >= prev_year).all()

    session.close()
    # Unravel results into a 1D array and convert to a list
    ##temps = list(np.ravel(results_tobs))
    # create a list of dictionaries with tob info using for loop 
    temps=[]
    for station, date, tobs in results_tobs:
        tobs_data={}
        tobs_data[station]={'date': date, 'tobs':tobs}
        temps.append(tobs_data)
    
    # Return the results
    return jsonify(temps)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start, end=None):
    """Return TMIN, TAVG, TMAX."""

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        # start = dt.datetime.strptime(start, "%m/%d/%Y")
        # # calculate TMIN, TAVG, TMAX for dates greater than start
        # results = session.query(*sel).\
        #     filter(Measurement.date >= start).all()
        # # Unravel results into a 1D array and convert to a list
        # temps = list(np.ravel(results))
        # return jsonify(temps)

        start = str(start)
        end= session.query(func.max(Measurement.date)).\
                scalar()
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()

        session.close()
        # # Unravel results into a 1D array and convert to a list
        #temps = list(np.ravel(results))
        # create a list of dictionaries with statics info using for loop . It lead us to understand easy
        temps=[]
        for tmin, tavg, tmax in results:
            static_data={}
            static_data['TMIN'] = tmin
            static_data['TAVG'] = tavg
            static_data['TMAX'] = tmax
            temps.append(static_data)

        return jsonify(temps)

    # calculate TMIN, TAVG, TMAX with start and stop
    

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    #temps = list(np.ravel(results))
    # create a list of dictionaries with statics info using for loop . It lead us to understand easy
    temps_st_end=[]
    for tmin, tavg, tmax in results:
        static_data={}
        static_data['TMIN'] = tmin
        static_data['TAVG'] = tavg
        static_data['TMAX'] = tmax
        temps_st_end.append(static_data)

    return jsonify(temps_st_end)

if __name__ == '__main__':
    app.run(debug=True)
    
