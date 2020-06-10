import streamlit as sl
import pandas as panda
import numpy as np
import pydeck as pdk
import plotly.express as plotlyx

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

sl.write(pdk.Deck(
	map_style = "mapbox://styles/mapbox/light-v9", 
	initial_view_state = {
		"latitude" : midpoints[0],
		"longitude" : midpoints[1],
		"zoom": 11, 
		"pitch": 50, 
	},
	layers =[
		pdk.Layer(
		"HexagonLayer",
		data = data[['date/time', 'latitude', 'longitude']], 
		get_position = ['longitude', 'latitude'], 
		radius =100, 
		extruded = True,
		pickable = True,
		elevation_scale = 4,
		elevation_range=[0, 1000],
		get_fill_color = [180,0,200,14], 
		),
	],	
))

sl.subheader("Breakdown by minute between %i:00 and %i:00" %(hour, (hour+1)%24))
filtered = data[
	(data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0,60))[0]
chart_data = panda.DataFrame({'minute': range(60), 'crashes':hist})
fig = plotlyx.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
sl.write(fig)

sl.header("Top 5 dangerous streets by afftected type")
select = sl.selectbox("Affected type of People",['Pedestrians','Cyclists','Motorists'])

if select == 'Pedestrians':
	st.write(original_data.query('injured_pedestrians >= 1')[['on_street_name','injured_pedestrians']].sort_values(by = ['injured_pedestrians'], ascending = False).dropna(how='any')[:5]

elif select == 'Cyclists':
	st.write(original_data.query('injured_cyclists >= 1')[['on_street_name','injured_cyclists']].sort_values(by = ['injured_cyclists'], ascending = False).dropna(how='any')[:5]

else:
	st.write(original_data.query('injured_motorists >= 1')[['on_street_name','injured_motorists']].sort_values(by = ['injured_motorists'], ascending = False).dropna(how='any')[:5]

if sl.checkbox("I would like to see the raw data", False):
    sl.subheader("Raw Data")
    sl.write(data)