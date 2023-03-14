# 1. import Flask
from flask import Flask,jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
import numpy as np
import datetime as dt

# 2. Create an app, being sure to pass __name__


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

Measurement=Base.classes.measurement
Station=Base.classes.station

session = Session(engine)
app = Flask(__name__)


@app.route("/")
def home():
    print("test home")
    return "this is the home page test1"

@app.route("/test")
def test():   
    testresult=session.query(Measurement.date).order_by(desc(Measurement.date)).first()
    session.close()
    return jsonify (list(testresult))

@app.route("/api/v1.0/stations")
def stationname():
    stname=session.query(Measurement.station).group_by(Measurement.station).all()
    session.close()
    stname=np.ravel(stname)
    return jsonify (list(stname))


@app.route("/api/v1.0/precipitation")
def precipitation(): 
    my_date = dt.date(2017, 8, 23)-dt.timedelta(days=365)  
    precip=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>= my_date).all()
    session.close()
    precip=np.ravel(precip)
    return jsonify (list(precip))
   


@app.route("/api/v1.0/tobs")
def activestation():
    my_date = dt.date(2017, 8, 23)-dt.timedelta(days=365)  
    ActiveStationCount=session.query(Measurement.station,func.count(Measurement.date)).group_by(Measurement.station).order_by(desc(func.count(Measurement.date))).first()
    ActiveStationID = list(ActiveStationCount)[0]
    act12=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date> my_date).filter(Measurement.station==ActiveStationID).all()
    session.close()
    act12=np.ravel(act12)
    return jsonify (list(act12))

@app.route("/api/v1.0/temp/<start>")
def startdate(start):    
    start=dt.datetime.strptime(start,"%m%d%Y")
    selectdate=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start).all()
    s=list(np.ravel(selectdate))
    session.close()
    return jsonify(s)

@app.route("/api/v1.0/temp/<start>/<end>")
def startenddate(start,end): 
    start=dt.datetime.strptime(start,"%m%d%Y")
    end=dt.datetime.strptime(end,"%m%d%Y")
    selectdateend=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    stend=list(np.ravel(selectdateend))
    session.close()
    return jsonify(stend)
    

if __name__ == '__main__':
    app.run(port=5001)

    

