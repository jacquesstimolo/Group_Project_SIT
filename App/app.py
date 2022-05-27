#--------------------------------------------
# LIBRARIES:
#--------------------------------------------
# Standard imports
from git import Reference
import numpy as np
import pandas as pd
import json

# matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

#plotly
import plotly.express as px
import plotly.graph_objects as go

import streamlit as st

# Google-maps:
from geopy.geocoders import GoogleV3
import geopy.distance
import googlemaps






#--------------------------------------------
# DataFrames:
#--------------------------------------------
migros = pd.read_csv('data/migros.csv')
migros = migros[['address', 'name', 'rating', 'nr_users_rating', 'lat', 'lng', 'Kreis_id']]
# st.dataframe(migros)


competition = pd.read_csv('data/competitors.csv')
competition = competition[['address', 'name_s', 'rating', 'users_rating_num', 'lat', 'lng', 'Kreis_id']]
# st.dataframe(competition)


people = pd.read_csv('data/population_workingclass.csv')
people = people[['Kreise', 'Count', 'id_Kreis']]
# st.dataframe(people)


# DP location Kreise:
# Source: https://latitudelongitude.org/ch/zuerich-kreis-12/
# ID : lon, lat
dict_coords = {
    1 : [47.37055, 8.54177],
    2 : [47.33756, 8.5211],
    3 : [47.35785, 8.50296],
    4 : [47.37752, 8.5212],
    5 : [47.38767, 8.52152],
    6 : [47.39223, 8.54381],
    7 : [47.37328, 8.58038],
    8 : [47.3548, 8.56097],
    9 : [47.38245, 8.47993],
    10 : [47.40773, 8.5005],
    11 : [47.42326, 8.52166],
    12 : [47.40372, 8.57608]
}

latid, longi, ids = [], [], []
for key, values in dict_coords.items():
    ids.append(key)
    latid.append(values[0])
    longi.append(values[1])

reference = pd.DataFrame()
reference['id'] = ids
reference['lat'] = latid
reference['lon'] = longi
reference['color'] = [1 for _ in range(12)]




#--------------------------------------------
# Open the API-File & add ID:
#--------------------------------------------
with open('stadtkreise.json') as json_file:
    stadtkreise = json.load(json_file)

def set_ID(kreis):
    for i in range(len(kreis['features'])):
        kreis['features'][i]['id'] = kreis['features'][i]['properties']['name']
    return kreis

stadtkreise = set_ID(stadtkreise)






#--------------------------------------------
# Plotting:
#--------------------------------------------
# Default Color:
default_color = pd.DataFrame()
default_color['id_Kreis'] = people.id_Kreis
default_color['color'] = [0 for _ in range(0,12)]




#-----------------------
# Only Migros:
#-----------------------
fig = go.Figure(go.Choroplethmapbox(geojson=stadtkreise, locations=default_color.id_Kreis, z=default_color.color,
                                    colorscale="greys", zmin=-10, zmax=10, 
                                    marker_opacity=0.5, marker_line_width=0,
                                    showscale=False,
                                    text = people['Kreise'],
                                    hovertemplate = "%{text}<extra></extra>",))

fig.add_scattermapbox(lat = migros.lat.tolist(),
                      lon = migros.lng.tolist(),
                      line_color = 'red',
                      mode="markers+text",
                      marker={"size": 5},
                      text=migros["address"],
                      customdata=migros[['rating', 'nr_users_rating', 'Kreis_id', 'name']],
                      hovertemplate = "%{customdata[3]} <br>%{text}<br>Kreis %{customdata[2]} <br>lat: %{lat:.2f}   lon: %{lon:.2f}<br>Rating: %{customdata[0]},  Nr Ratings: %{customdata[1]}<extra></extra>",)

fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=10.5, mapbox_center = {"lat": 47.377220, "lon": 8.539902})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.header("Location of all Migros in Zürich:")
st.plotly_chart(fig)




#-----------------------
# Migros & Competition:
#-----------------------
fig = go.Figure(go.Choroplethmapbox(geojson=stadtkreise, locations=default_color.id_Kreis, z=default_color.color,
                                    colorscale="greys", zmin=-10, zmax=10, 
                                    marker_opacity=0.5, 
                                    marker_line_width=0,
                                    showscale=False,
                                    text = people['Kreise'],
                                    hovertemplate = "%{text}<extra></extra>",))

# Migros:
fig.add_scattermapbox(lat = migros.lat.tolist(),
                      lon = migros.lng.tolist(),
                      line_color = 'red',
                      mode="markers+text",
                      marker={"size": 5},
                      text=migros["address"],
                      customdata=migros[['rating', 'nr_users_rating', 'Kreis_id', 'name']],
                      hovertemplate = "%{customdata[3]} <br>%{text}<br>Kreis %{customdata[2]} <br>lat: %{lat:.2f}   lon: %{lon:.2f}<br>Rating: %{customdata[0]},  Nr Ratings: %{customdata[1]}<extra></extra>",)


# Competition:
fig.add_scattermapbox(lat = competition.lat.tolist(),
                    lon = competition.lng.tolist(),
                    line_color = 'blue',
                    mode="markers+text",
                    marker={"size": 5},
                    text=competition["address"],
                    customdata=competition[['rating', 'users_rating_num', 'Kreis_id', 'name_s']],
                    hovertemplate = "%{customdata[3]} <br>%{text}<br>Kreis %{customdata[2]} <br>lat: %{lat:.2f}   lon: %{lon:.2f}<br>Rating: %{customdata[0]},  Nr Ratings: %{customdata[1]}<extra></extra>",)



# Competition:
fig.add_scattermapbox(lat = competition.lat.tolist(),
                    lon = competition.lng.tolist(),
                    line_color = 'blue',
                    mode="markers+text",
                    marker={"size": 5},
                    text=competition["address"],
                    customdata=competition[['rating', 'users_rating_num', 'Kreis_id', 'name_s']],
                    hovertemplate = "%{customdata[3]} <br>%{text}<br>Kreis %{customdata[2]} <br>lat: %{lat:.2f}   lon: %{lon:.2f}<br>Rating: %{customdata[0]},  Nr Ratings: %{customdata[1]}<extra></extra>",)


fig.update(layout_showlegend=False)
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=10.5, mapbox_center = {"lat": 47.377220, "lon": 8.539902})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.header("Location of all Migros and Competitors in Zürich:")
st.plotly_chart(fig)






#-----------------------
# Rating of Migros:
#-----------------------
fig = go.Figure(go.Choroplethmapbox(geojson=stadtkreise, locations=default_color.id_Kreis, z=default_color.color,
                                    colorscale="greys",
                                    marker_opacity=0.5, 
                                    marker_line_width=0,
                                    showscale=False))

fig.add_scattermapbox(lat = migros.lat.tolist(),
                      lon = migros.lng.tolist(),
                      line_color = 'red',
                      mode="markers+text",
                      marker=go.scattermapbox.Marker(size= np.log(migros.nr_users_rating)*1.5), 
                      text=migros["address"],
                      customdata=migros[['rating', 'nr_users_rating', 'Kreis_id']],
                      hovertemplate = "MIGROS <br>%{text}<br>Kreis %{customdata[2]} <br>Lat: %{lat:.2f}   Lon: %{lon:.2f}<br>Rating: %{customdata[0]},  Nr Ratings: %{customdata[1]}<extra></extra>")

df_coop = competition[competition.name_s == 'Coop']

fig.add_scattermapbox(lat = df_coop.lat.tolist(),
                      lon = df_coop.lng.tolist(),
                      line_color = 'green',
                      mode="markers+text",
                      marker=go.scattermapbox.Marker(size= np.log(df_coop.users_rating_num)*1.5), 
                      text=df_coop["address"],
                      customdata=df_coop[['rating', 'users_rating_num', 'Kreis_id']],
                      hovertemplate = "COOP <br>%{text}<br>Kreis %{customdata[2]} <br>Lat: %{lat:.2f}   Lon: %{lon:.2f}<br>Rating: %{customdata[0]},  Nr Ratings: %{customdata[1]}<extra></extra>")

list_stores_names = ['Denner', 'Aldi', 'Lidl', 'Spar']

for store in list_stores_names:
    df_aux = competition[competition.name_s == store]
    fig.add_scattermapbox(lat = df_aux.lat.tolist(),
                        lon = df_aux.lng.tolist(),
                        line_color = 'blue',
                        mode="markers+text",
                        marker=go.scattermapbox.Marker(size= np.log(df_aux.users_rating_num)*1.5), 
                        text=df_aux["address"],
                        customdata=df_aux[['rating', 'users_rating_num', 'Kreis_id', 'name_s']],
                        hovertemplate = "%{customdata[3]} <br>%{text}<br>Kreis %{customdata[2]} <br>lat: %{lat:.2f}   lon: %{lon:.2f}<br>Rating: %{customdata[0]},  Nr Ratings: %{customdata[1]}<extra></extra>",)

fig.update(layout_showlegend=False)
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=10.5, mapbox_center = {"lat": 47.377220, "lon": 8.539902})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)








#-----------------------
# Location of Migros:
#-----------------------
df_count = pd.DataFrame()
df_count['Kreis_id'] = [id for id in range(1, 13)]

count = []
for id in range(1, 13):
    count.append(len(migros[migros['Kreis_id'] == id]))
    
df_count['Count'] = count


fig = go.Figure(go.Choroplethmapbox(geojson=stadtkreise, locations=df_count.Kreis_id, z=df_count.Count,
                                    colorscale="Viridis",
                                    marker_opacity=0.5, 
                                    marker_line_width=0,
                                    text = df_count[['Kreis_id', 'Count']],
                                    hovertemplate = "Kreis %{text[0]}<br>Number of stores: %{text[1]}<extra></extra>"
                                    ))

fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=10.5, mapbox_center = {"lat": 47.377220, "lon": 8.539902})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.header("Where are Migros stores concentrated?")
st.plotly_chart(fig)




#-----------------------
# Location of Competition:
#-----------------------
df_count = pd.DataFrame()
df_count['Kreis_id'] = [id for id in range(1, 13)]

count = []
for id in range(1, 13):
    count.append(len(competition[competition['Kreis_id'] == id]))
    
df_count['Count'] = count


fig = go.Figure(go.Choroplethmapbox(geojson=stadtkreise, locations=df_count.Kreis_id, z=df_count.Count,
                                    colorscale="Viridis",
                                    marker_opacity=0.5, 
                                    marker_line_width=0,
                                    text = df_count[['Kreis_id', 'Count']],
                                    hovertemplate = "Kreis %{text[0]}<br>Number of stores: %{text[1]}<extra></extra>"
                                    ))

fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=10.5, mapbox_center = {"lat": 47.377220, "lon": 8.539902})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.header("Where is the Competition concentrated?")
st.plotly_chart(fig)




#-----------------------
# Reference coords API:
#-----------------------
fig = go.Figure(go.Choroplethmapbox(geojson=stadtkreise, locations=reference.id, z=reference.color,
                                    colorscale="greys",
                                    showscale=False,
                                    text = reference['id'],
                                    hovertemplate = "Kreis %{text}<extra></extra>",
                                    marker_opacity=0.5, marker_line_width=0))

fig.add_scattermapbox(lat = reference.lat.tolist(),
                      lon = reference.lon.tolist(),
                      line_color = 'black',
                      mode="markers+text",
                      hovertemplate = "Lat: %{lat}°  Lon: %{lon}°<extra></extra>",
                      marker={"size": 5})

fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=10.5, mapbox_center = {"lat": 47.377220, "lon": 8.539902})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.header("Reference points for googlemaps-API:")
st.dataframe(reference[['id', 'lat', 'lon']])
st.plotly_chart(fig)




#-----------------------
# Google-Maps API:
#-----------------------

travel_modes = ['walking', 'driving', 'bicycling', 'transit']
mode = st.selectbox('Choose the type:', travel_modes)


API = 'AIzaSyAYJBfeZxsN05Pkc1aoU60oL2VZpMn9b2g'
gmap = googlemaps.Client(key=API)

dict_duration = dict()

for id in range(1, 13):
    df_aux = migros[migros['Kreis_id'] == id]
    
    addresses = df_aux['address'].tolist()

    coords = zip(df_aux['lat'].tolist(), df_aux['lng'].tolist())

    ref_lat = dict_coords[id][0]
    ref_lon = dict_coords[id][1]

    # print(ref_lat, ref_lon)
    pos = 0
    for coord in coords:
        d_goog = gmap.distance_matrix((ref_lat, ref_lon), coord, mode=mode)
        duration = new_d = d_goog['rows'][0]['elements'][0]['duration']['text']
        dict_duration[addresses[pos]] = duration
        pos += 1
    

df = pd.DataFrame(dict_duration.items(), columns=['address', 'Duration'])

get_duration = lambda x: int(x.split(' ')[0])

df['duration_val'] = df.Duration.apply(get_duration)

# Merge Migros and Distance dataframe:
migros_dist = pd.merge(migros, df)

st.dataframe(migros_dist[['Kreis_id', 'address', 'Duration']])



fig = go.Figure(go.Choroplethmapbox(geojson=stadtkreise, locations=default_color.id_Kreis, z=default_color.color,
                                    colorscale="greys", zmin=-10, zmax=10,
                                    marker_opacity=0.5, marker_line_width=0,
                                    showscale=False,
                                    text = people['Kreise'],
                                    hovertemplate = "%{text}<extra></extra>",))

fig.add_scattermapbox(lat = migros_dist.lat.tolist(),
                      lon = migros_dist.lng.tolist(),
                      line_color = 'red',
                      mode="markers+text",
                      marker={"size": 5},
                      text=migros_dist["address"],
                      customdata=migros_dist[['rating', 'nr_users_rating', 'Kreis_id', 'name', 'Duration']],
                      hovertemplate = "DURATION: %{customdata[4]} <br>%{customdata[3]} <br>%{text}<br>Kreis %{customdata[2]} <br>lat: %{lat:.2f}   lon: %{lon:.2f}<br>Rating: %{customdata[0]},  Nr Ratings: %{customdata[1]}<extra></extra>",)


fig.add_scattermapbox(lat = reference.lat.tolist(),
                      lon = reference.lon.tolist(),
                      line_color = 'black',
                      mode="markers+text",
                      hovertemplate = "REFERENCE: <br>Lat: %{lat}°  Lon: %{lon}°<extra></extra>",
                      marker={"size": 5})

fig.update(layout_showlegend=False)
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=10.5, mapbox_center = {"lat": 47.377220, "lon": 8.539902})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.header(f"Travelling Time to Migros by {mode.upper()}:")
st.plotly_chart(fig)



#-----------------------
# Calculate avarage duration:
#-----------------------
nr_stores = migros_dist.groupby('Kreis_id').duration_val.count().tolist()
durations = migros_dist.groupby('Kreis_id').duration_val.sum().tolist()

average = []
vals = list(zip(durations, nr_stores))
for val in vals:
    d, nr = val
    average.append(round(d/nr, 1))

df1 = pd.DataFrame()
df1['id'] = [i for i in range(1, 13)]
df1['average'] = average




st.header("Average travel time to Migros:")

fig = go.Figure()
    
for id in range(1, 13):
    df_aux = migros_dist[migros_dist['Kreis_id'] == id]
    
    y = df_aux['duration_val']
    fig.add_trace(go.Box(y=y, name='Kreis '+str(id)))


fig.update_yaxes(title={"text": "Travel-Time to Migros", "font": {"size": 18}})
fig.update_xaxes(title={"text": "Stadtkreise", "font": {"size": 18}})

st.plotly_chart(fig)




fig = go.Figure(go.Choroplethmapbox(geojson=stadtkreise, locations=df1.id, z=df1.average,
                                    colorscale="Viridis",
                                    marker_opacity=0.5, marker_line_width=0,
                                    text = df1['id'],
                                    customdata = df1[['id','average']],
                                    hovertemplate = "Kreis %{customdata[0]}<br>Average travel Time: %{customdata[1]} min<extra></extra>"))

fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=10.5, mapbox_center = {"lat": 47.377220, "lon": 8.539902})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig)












