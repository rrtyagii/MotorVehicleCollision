import streamlit as sl
import pandas as panda
import numpy as np
import pydeck as pdk

DATA_URL = ('C:\\IIT\\Research\\NYC_Collision\\Motor_Vehicle_Collisions_-_Crashes.csv')

sl.title("Motor Vehicle Collision in New York City")
sl.markdown("This application is a streamlit dashboard that can be used to analyse the motor vehicle collision in New York City 🚗💥🗽  ")

@sl.cache(persist=True)
def load_data(nrows):
    data = panda.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x:str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data


data = load_data(100000)

sl.header("Which places are more dangerous for people in NYC?")
injured_people = sl.slider("Number of persons injured in vehicle collisions", 0, 19)
sl.map( data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how='any'))

sl.header("How many collisions occur during a given time of day?")
hour = sl.slider("What hour you want to look at", 0, 23)
data = data[data['date/time'].dt.hour == hour]
sl.markdown("Vehicle collision between %i:00 and %i:00" %(hour, (hour+1)%24))

midpoints = (np.average(data['latitude']), np.average(data['longitude']) )

sl.write(pdk.Dec(
	map_style = "mapbox://styles/mapbox/light-v9", 
	initial_view_state = {
		"latitude" : midpoints[0],
		"longitude" : midpoints[1],
		"zoom": 11, 
		"pitch": 50, 
	},  
))



if sl.checkbox("I would like to see the raw data", False):
    sl.subheader("Raw Data")
    sl.write(data)