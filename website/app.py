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

def get_past_floods() -> pd.DataFrame:
    base_url_flood = "https://flood-api.open-meteo.com/v1/flood"

    params_flood = {
        "latitude": TALAGANTE_LAT,
        "longitude": TALAGANTE_LON,
        "daily": "river_discharge",
        "past_days": "4",
        "forecast_days": "1",
        "models": "seamless_v4"
    }

    response_flood = requests.get(base_url_flood, params=params_flood)

    raw_data_flood = response_flood.json()

    df_flood = pd.DataFrame(data= raw_data_flood, columns=['date','flood'])

    df_flood['date'] = raw_data_flood['daily']['time']
    # transforming dates into '%m-%d' format
    df_flood['date'] = pd.to_datetime(df_flood['date'], format='%Y-%m-%d').dt.strftime('%m-%d')
    df_flood['flood'] = raw_data_flood['daily']['river_discharge']
    df_flood.set_index('date', inplace=True)

    # df_flood = df_flood.iloc[:-1,:]

    return df_flood

def plot_creation(df):
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0e1117')

    ax.set_facecolor("#0e1117")

    # plotting the river flow with a line until today and a dotted line for the forecast
    ax.plot(df.index[:-1], df['flood'][:-1], label='river flow', color='#4285f4', alpha=1)

    # plot the forecast as a single dotted line
    ax.plot(df.index[-2:], df['flood'][-2:], label='forecast', color='#4285f4', alpha=1, linestyle=':')

    # fill bellow the line
    ax.fill_between(df.index, df['flood'], color='#4285f4', alpha=0.3)

    # adding threshold danger
    ax.axhline(200, color='red', linestyle='-', label='danger level', alpha=0.5)

    # adding threshold warning
    ax.axhline(150, color='yellow', linestyle='-', label='warning level', alpha=0.5)

    # adding vertical line in today's date
    yesterday = datetime.datetime.now() + datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%m-%d')
    ax.axvline(yesterday, color='gray', linestyle='--', label='tommorrow', alpha=0.5)

    # deleting the y axis
    ax.axes.yaxis.set_visible(False)

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
Just click the button below and let AI do the rest
'''

# creating 3 cols layout in order to display the button in the middle
columns = st.columns(3)

# creating the button
button = columns[1].button('Click here to forecast', use_container_width=True)

if button:
    df = get_past_floods()

    # # adding tommorow's date
    tommorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    tommorrow = tommorrow.strftime('%m-%d')
    df.loc[tommorrow] = result

    # # adding next day date
    next = datetime.datetime.now() + datetime.timedelta(days=2)
    next = next.strftime('%m-%d')
    df.loc[next] = result

    fig = plot_creation(df)
    st.pyplot(fig)

    if float(result) >= 150 and float(result) <= 190:
        f'''
        ## ⚠️ Warning flow forecasted for tomorrow
        '''
    elif float(result) > 190:
        f'''
        ## 🛑 Danger flow forecasted for tomorrow
        '''
    else:
        f'''
        ## ✅ Normal flow forecasted for tomorrow
        '''
else:
    st.write('')

st.write('---')
