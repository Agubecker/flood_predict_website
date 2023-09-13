import streamlit as st
import folium
from streamlit_folium import folium_static
import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt

TALAGANTE_LAT = -33.714913
TALAGANTE_LON= -70.957909

url = 'https://flood-pred-intel-idtyvgmhca-vp.a.run.app/forecast'

response = requests.get(url).json()
result = response['forecast']

def plot_creation(df):
    plt.style.context('dark_background')

    fig, ax = plt.subplots(figsize=(10, 5))

    # plotting the river flow with a line until today and a dotted line for the forecast
    ax.plot(df.index[:8], df['flow(m3/s)'][:8], label='river flow', color='#4285f4', alpha=1)
    ax.plot(df.index[7:], df['flow(m3/s)'][7:], label='forecast', color='#4285f4', alpha=1, linestyle='--')
    ax.fill_between(df.index, df['flow(m3/s)'], color='#4285f4', alpha=0.3)

    # adding threshold
    ax.axhline(250, color='red', linestyle='-', label='level of danger', alpha=0.5)

    # adding vertical line in today's date
    today = datetime.datetime.now()
    today = today.strftime('%m-%d')
    ax.axvline(today, color='gray', linestyle='--', label='today', alpha=0.5)

    # deleting the y axis
    ax.axes.yaxis.set_visible(False)

    # taking out last day from the x axis and showing every 2 days in the x axis
    ax.set_xticks(df.index[::2])

    # adding black lines to each day
    ax.xaxis.set_tick_params(which='major', size=10, width=1, direction='out', color='white')

    # remarking the x axis line with black color
    ax.tick_params(axis='x', colors='white', labelsize=10)

    # choosing position for the legend
    ax.legend(loc='center left')

    return fig

'''
# Flood Forecasting 🏞️ - Chile
'''

'''
Website dedicated to forecasting floods in Chile

Just follow the steps below and you'll get a flood's forecast in your area
'''

st.write('---')

'''
## In which areas do we forecast?💭
'''

# creating map of New York
m = folium.Map(location=[TALAGANTE_LAT, TALAGANTE_LON], zoom_start=10)

# adding markers to the map
pickup_marker = folium.Marker(
    location=[TALAGANTE_LAT, TALAGANTE_LON],
    tooltip="Talagante",
    icon=folium.Icon(color="blue"),
)
pickup_marker.add_to(m)

# control layer
folium.LayerControl().add_to(m)

# showing the map
folium_static(m)

st.write('---')

'''
## Forecast in your area!🌊
'''
'''
Just click the button below and let us do the rest 😉
'''

# creating 3 cols layout in order to display the button in the middle
columns = st.columns(3)

# creating the button
button = columns[1].button('Click here to forecast', use_container_width=True)

if button:
    f'''
    ## {result}
    '''
else:
    st.write('')

st.write('---')
