import streamlit as st
import pandas as pd
import requests

st.cache_data(ttl=1800)
def get_current_weather_data(api_key, city_name):

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        st.warning(f"Error while getting information about {city_name}, error code: {response.status_code}")
    else:
        return data

def main():

    API_KEY = st.secrets["openweathermap"]["api_key"]

    st.set_page_config(page_title="Weather Report", layout="wide")
    st.title("Weather Map & Data Visualization App")
    st.divider()

    city_name = st.text_input("Enter a city:", "Budapest")

    weather_data = get_current_weather_data(API_KEY, city_name)

    if weather_data:

        st.header(f"Current weather in {city_name}")

        col_1, col_2, col_3 = st.columns(3)

        with col_1:
            st.metric(label="Temperature (°C)", value=f"{weather_data['main']['temp']} °C")
        with col_2:
            st.metric(label="Humidity (%)", value=f"{weather_data['main']['humidity']} %")
        with col_3:
            st.metric(label="Wind Speed (m/s)", value=f"{weather_data['wind']['speed']} m/s")

        st.header("Weather Map")
        st.map(pd.DataFrame({"lon": [weather_data['coord']['lon']], "lat": [weather_data['coord']['lat']]}))


if __name__ == "__main__":
    main()