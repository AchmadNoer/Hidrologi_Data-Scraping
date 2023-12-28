from dateutil import relativedelta
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from matplotlib.ticker import FormatStrFormatter
import warnings
import requests
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
plt.style.use("dark_background")

st.set_page_config(page_title="Forecast - AccuWeather.com",
                   page_icon=":mostly_sunny:", layout="wide")
with st.sidebar:
    st.header("Weather Forecast :chart_with_upwards_trend:")
    st.markdown(
        """
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"] {
            width: 20% !important;
        }
    </style>
    """, unsafe_allow_html=True)

    date_list = pd.date_range(datetime.now().strftime('%d %B %Y'), periods=3).format(
        formatter=lambda x: x.strftime('%d %B %Y'))
    option = st.selectbox("Please Select Date", date_list)

    day = (pd.to_datetime(option) - datetime.now()).days + 1

web_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

tentena = "https://www.accuweather.com/id/id/saojo/679113/hourly-weather-forecast/679113?unit=c&day="
salukaia = "https://www.accuweather.com/id/id/leboni/205822/hourly-weather-forecast/205822?unit=c&day="
panjo = "https://www.accuweather.com/id/id/panjo/3479026/hourly-weather-forecast/3479026?unit=c&day="
mayoa = "https://www.accuweather.com/id/id/maya-sari/1898183/hourly-weather-forecast/1898183?unit=c&day="
tindoli = "https://www.accuweather.com/id/id/tokilo/205955/hourly-weather-forecast/205955?unit=c&day="
sulewana = "https://www.accuweather.com/id/id/sulewana/3479048/hourly-weather-forecast/3479048?unit=c&day="
pandiri = "https://www.accuweather.com/id/id/poso/205881/hourly-weather-forecast/205881?unit=c&day="


def scraping(lokasi):
    konten = pd.DataFrame(np.empty((0, 3)))
    sekarang = datetime.now(tz=timezone(timedelta(hours=8)))  # GMT+8
    day_range = 3

    for days in range(1, day_range+1):
        response = requests.get(lokasi+str(days), headers=web_headers)
        soup = BeautifulSoup(response.content, "html.parser")
        cards = soup.find_all("div", attrs={"class": "accordion-item hour"})

        for card in range(0, len(cards)):
            date = str(sekarang.strftime('%Y-%m-%d '))

            tag_hour = BeautifulSoup(str(BeautifulSoup(str(cards[card]))
                                         .find_all("h2", attrs={"class": "date"}))).find_all("div", attrs={"class": ""})
            tag_precipitation = BeautifulSoup(str(cards[card])).find_all(
                "div", attrs={"class": "precip"})
            tag_hujan = BeautifulSoup(str(cards[card])).find_all(
                "p", attrs={"class": ""})

            hour = [date+isi.text for isi in tag_hour]
            precipitation = [isi.text for isi in tag_precipitation]
            hujan = [
                isi.text for isi in tag_hujan if isi.text.startswith("Hujan")]
            if not hujan:
                hujan = ["0"]

            daily = pd.DataFrame(list(zip(hour, precipitation, hujan)))
            daily[0] = pd.to_datetime(daily[0])
            daily[1] = daily[1].map(lambda x: x.strip('\n\t').strip("%"))
            daily[2] = daily[2].map(lambda x: x.strip('Hujan').strip("mm"))

            konten = pd.concat([konten, daily], axis=0)

        sekarang = sekarang + relativedelta.relativedelta(days=1)

    konten.columns = ["datetime", "precipitation", "rainfall"]
    konten.reset_index(drop=True, inplace=True)

    konten["precipitation"] = konten["precipitation"].astype("int64")
    konten["rainfall"] = pd.to_numeric(
        konten["rainfall"], errors='coerce').astype("float64")

    item = [0, 24, 48, 72, 96, 120]
    konten = konten.iloc[item[day]:item[day+1]]

    return konten


forecast_tentena = scraping(tentena)
forecast_salukaia = scraping(salukaia)
forecast_panjo = scraping(panjo)
forecast_mayoa = scraping(mayoa)
forecast_tindoli = scraping(tindoli)
forecast_sulewana = scraping(sulewana)
forecast_pandiri = scraping(pandiri)

st.header("Weather Forecast Data Scraping :mostly_sunny: - accuweather.com")
st.subheader("Rainfall All Station 	:house:")

st.table(forecast_tentena)

col_rf_tentena, col_rf_salukaia, col_rf_panjo, col_rf_mayoa, col_rf_tindoli = st.columns(
    5)

with col_rf_tentena:
    sum_rain_tentena = forecast_tentena["rainfall"].sum()
    st.metric("Rainfall Tentena:", f"{round(sum_rain_tentena,1):n} mm/d")
with col_rf_salukaia:
    sum_rain_salukaia = forecast_salukaia["rainfall"].sum()
    st.metric("Rainfall Salukaia:", f"{round(sum_rain_salukaia,1):n} mm/d")
with col_rf_panjo:
    sum_rain_panjo = forecast_panjo["rainfall"].sum()
    st.metric("Rainfall Panjo:", f"{round(sum_rain_panjo,1):n} mm/d")
with col_rf_mayoa:
    sum_rain_mayoa = forecast_mayoa["rainfall"].sum()
    st.metric("Rainfall Mayoa:", f"{round(sum_rain_mayoa,1):n} mm/d")
with col_rf_tindoli:
    sum_rain_tindoli = forecast_tindoli["rainfall"].sum()
    st.metric("Rainfall Tindoli:", f"{round(sum_rain_tindoli,1):n} mm/d")

col_rf_sulewana, col_rf_pandiri, col_rf_kosong1, col_rf_kosong2, col_rf_kosong3 = st.columns(
    5)

with col_rf_sulewana:
    sum_rain_sulewana = forecast_sulewana["rainfall"].sum()
    st.metric("Rainfall Sulewana:", f"{round(sum_rain_sulewana,1):n} mm/d")
with col_rf_pandiri:
    sum_rain_pandiri = forecast_pandiri["rainfall"].sum()
    st.metric("Rainfall Pandiri:", f"{round(sum_rain_pandiri,1):n} mm/d")

x_data = pd.Series(["Tentena", "Salukaia", "Panjo",
                   "Mayoa", "Tindoli", "Sulewana", "Pandiri"])
y_data = pd.Series([forecast_tentena["rainfall"].sum(),
                    forecast_salukaia["rainfall"].sum(),
                    forecast_panjo["rainfall"].sum(),
                    forecast_mayoa["rainfall"].sum(),
                    forecast_tindoli["rainfall"].sum(),
                    forecast_sulewana["rainfall"].sum(),
                    forecast_pandiri["rainfall"].sum()])

fig, ax = plt.subplots(figsize=(15, 5))

ax.bar(x_data, y_data, alpha=0.9)
ax.set_ylabel("Rainfall (mm/d)")
ax.set_ylim(0, round(y_data.max())+5)
ax.bar_label(ax.containers[0], label_type="edge", fontsize=10)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax.yaxis.grid(linestyle="dashed")
ax.set_axisbelow(True)
ax.set_xlabel("Area/Station")

st.pyplot(plt)

st.subheader("Rainfall & Precipitation 	:umbrella_with_rain_drops:")

tentena_rf, salukaia_rf, panjo_rf, mayoa_rf, tindoli_rf, sulewana_rf, pandiri_rf = st.tabs(
    ["Tentena", "Salukaia", "Panjo", "Mayoa", "Tindoli", "Sulewana", "Pandiri"])

with tentena_rf:
    x_tentena = forecast_tentena["datetime"].dt.strftime('%H')
    y1_tentena = forecast_tentena["precipitation"]
    y2_tentena = forecast_tentena["rainfall"]

    col1_tentena, col2_tentena, col3_tentena = st.columns(3)

    with col1_tentena:
        max_prec_tentena = y1_tentena.max()
        st.metric("Highest Precipitation:", f"{max_prec_tentena:n} %")
    with col2_tentena:
        sum_rain_tentena = y2_tentena.sum()
        st.metric("Rainfall per Day:", f"{round(sum_rain_tentena,1):n} mm")
    with col3_tentena:
        count_rain_tentena = y2_tentena[y2_tentena > 0].count()
        st.metric("Hours of Rain:", f"{count_rain_tentena:n} hour(s)")

    fig, ax1 = plt.subplots(figsize=(15, 5))
    ax2 = ax1.twinx()

    ax1.plot(x_tentena, y1_tentena, alpha=0.8, marker="o", color="white")
    ax1.set_ylabel("Precipitation (%)")
    ax1.legend(["Precipitation"], loc="center right",
               bbox_to_anchor=(0.5, -0.2))
    ax1.set_ylim(0, 100)
    ax1.yaxis.grid(linestyle="dashed")
    ax1.set_axisbelow(True)
    ax1.set_xlabel("Hour")

    ax2.bar(x_tentena, y2_tentena, alpha=0.8)
    ax2.set_ylabel("Rainfall (mm)")
    ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
    ax2.set_ylim(0, round(y2_tentena.max())+2)
    ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    st.pyplot(plt)

with salukaia_rf:
    x_salukaia = forecast_salukaia["datetime"].dt.strftime('%H')
    y1_salukaia = forecast_salukaia["precipitation"]
    y2_salukaia = forecast_salukaia["rainfall"]

    col1_salukaia, col2_salukaia, col3_salukaia = st.columns(3)

    with col1_salukaia:
        max_prec_salukaia = y1_salukaia.max()
        st.metric("Highest Precipitation:", f"{max_prec_salukaia:n} %")
    with col2_salukaia:
        sum_rain_salukaia = y2_salukaia.sum()
        st.metric("Rainfall per Day:", f"{round(sum_rain_salukaia,1):n} mm")
    with col3_salukaia:
        count_rain_salukaia = y2_salukaia[y2_salukaia > 0].count()
        st.metric("Hours of Rain:", f"{count_rain_salukaia:n} hour(s)")

    fig, ax1 = plt.subplots(figsize=(15, 5))
    ax2 = ax1.twinx()

    ax1.plot(x_salukaia, y1_salukaia, alpha=0.8, marker="o", color="white")
    ax1.set_ylabel("Precipitation (%)")
    ax1.legend(["Precipitation"], loc="center right",
               bbox_to_anchor=(0.5, -0.2))
    ax1.set_ylim(0, 100)
    ax1.yaxis.grid(linestyle="dashed")
    ax1.set_axisbelow(True)
    ax1.set_xlabel("Hour")

    ax2.bar(x_salukaia, y2_salukaia, alpha=0.8)
    ax2.set_ylabel("Rainfall (mm)")
    ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
    ax2.set_ylim(0, round(y2_salukaia.max())+2)
    ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    st.pyplot(plt)

with panjo_rf:
    x_panjo = forecast_panjo["datetime"].dt.strftime('%H')
    y1_panjo = forecast_panjo["precipitation"]
    y2_panjo = forecast_panjo["rainfall"]

    col1_panjo, col2_panjo, col3_panjo = st.columns(3)

    with col1_panjo:
        max_prec_panjo = y1_panjo.max()
        st.metric("Highest Precipitation:", f"{max_prec_panjo:n} %")
    with col2_panjo:
        sum_rain_panjo = y2_panjo.sum()
        st.metric("Rainfall per Day:", f"{round(sum_rain_panjo,1):n} mm")
    with col3_panjo:
        count_rain_panjo = y2_panjo[y2_panjo > 0].count()
        st.metric("Hours of Rain:", f"{count_rain_panjo:n} hour(s)")

    fig, ax1 = plt.subplots(figsize=(15, 5))
    ax2 = ax1.twinx()

    ax1.plot(x_panjo, y1_panjo, alpha=0.8, marker="o", color="white")
    ax1.set_ylabel("Precipitation (%)")
    ax1.legend(["Precipitation"], loc="center right",
               bbox_to_anchor=(0.5, -0.2))
    ax1.set_ylim(0, 100)
    ax1.yaxis.grid(linestyle="dashed")
    ax1.set_axisbelow(True)
    ax1.set_xlabel("Hour")

    ax2.bar(x_panjo, y2_panjo, alpha=0.8)
    ax2.set_ylabel("Rainfall (mm)")
    ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
    ax2.set_ylim(0, round(y2_panjo.max())+2)
    ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    st.pyplot(plt)

with mayoa_rf:
    x_mayoa = forecast_mayoa["datetime"].dt.strftime('%H')
    y1_mayoa = forecast_mayoa["precipitation"]
    y2_mayoa = forecast_mayoa["rainfall"]

    col1_mayoa, col2_mayoa, col3_mayoa = st.columns(3)

    with col1_mayoa:
        max_prec_mayoa = y1_mayoa.max()
        st.metric("Highest Precipitation:", f"{max_prec_mayoa:n} %")
    with col2_mayoa:
        sum_rain_mayoa = y2_mayoa.sum()
        st.metric("Rainfall per Day:", f"{round(sum_rain_mayoa,1):n} mm")
    with col3_mayoa:
        count_rain_mayoa = y2_mayoa[y2_mayoa > 0].count()
        st.metric("Hours of Rain:", f"{count_rain_mayoa:n} hour(s)")

    fig, ax1 = plt.subplots(figsize=(15, 5))
    ax2 = ax1.twinx()

    ax1.plot(x_mayoa, y1_mayoa, alpha=0.8, marker="o", color="white")
    ax1.set_ylabel("Precipitation (%)")
    ax1.legend(["Precipitation"], loc="center right",
               bbox_to_anchor=(0.5, -0.2))
    ax1.set_ylim(0, 100)
    ax1.yaxis.grid(linestyle="dashed")
    ax1.set_axisbelow(True)
    ax1.set_xlabel("Hour")

    ax2.bar(x_mayoa, y2_mayoa, alpha=0.8)
    ax2.set_ylabel("Rainfall (mm)")
    ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
    ax2.set_ylim(0, round(y2_mayoa.max())+2)
    ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    st.pyplot(plt)

with tindoli_rf:
    x_tindoli = forecast_tindoli["datetime"].dt.strftime('%H')
    y1_tindoli = forecast_tindoli["precipitation"]
    y2_tindoli = forecast_tindoli["rainfall"]

    col1_tindoli, col2_tindoli, col3_tindoli = st.columns(3)

    with col1_tindoli:
        max_prec_tindoli = y1_tindoli.max()
        st.metric("Highest Precipitation:", f"{max_prec_tindoli:n} %")
    with col2_tindoli:
        sum_rain_tindoli = y2_tindoli.sum()
        st.metric("Rainfall per Day:", f"{round(sum_rain_tindoli,1):n} mm")
    with col3_tindoli:
        count_rain_tindoli = y2_tindoli[y2_tindoli > 0].count()
        st.metric("Hours of Rain:", f"{count_rain_tindoli:n} hour(s)")

    fig, ax1 = plt.subplots(figsize=(15, 5))
    ax2 = ax1.twinx()

    ax1.plot(x_tindoli, y1_tindoli, alpha=0.8, marker="o", color="white")
    ax1.set_ylabel("Precipitation (%)")
    ax1.legend(["Precipitation"], loc="center right",
               bbox_to_anchor=(0.5, -0.2))
    ax1.set_ylim(0, 100)
    ax1.yaxis.grid(linestyle="dashed")
    ax1.set_axisbelow(True)
    ax1.set_xlabel("Hour")

    ax2.bar(x_tindoli, y2_tindoli, alpha=0.8)
    ax2.set_ylabel("Rainfall (mm)")
    ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
    ax2.set_ylim(0, round(y2_tindoli.max())+2)
    ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    st.pyplot(plt)

with sulewana_rf:
    x_sulewana = forecast_sulewana["datetime"].dt.strftime('%H')
    y1_sulewana = forecast_sulewana["precipitation"]
    y2_sulewana = forecast_sulewana["rainfall"]

    col1_sulewana, col2_sulewana, col3_sulewana = st.columns(3)

    with col1_sulewana:
        max_prec_sulewana = y1_sulewana.max()
        st.metric("Highest Precipitation:", f"{max_prec_sulewana:n} %")
    with col2_sulewana:
        sum_rain_sulewana = y2_sulewana.sum()
        st.metric("Rainfall per Day:", f"{round(sum_rain_sulewana,1):n} mm")
    with col3_sulewana:
        count_rain_sulewana = y2_sulewana[y2_sulewana > 0].count()
        st.metric("Hours of Rain:", f"{count_rain_sulewana:n} hour(s)")

    fig, ax1 = plt.subplots(figsize=(15, 5))
    ax2 = ax1.twinx()

    ax1.plot(x_sulewana, y1_sulewana, alpha=0.8, marker="o", color="white")
    ax1.set_ylabel("Precipitation (%)")
    ax1.legend(["Precipitation"], loc="center right",
               bbox_to_anchor=(0.5, -0.2))
    ax1.set_ylim(0, 100)
    ax1.yaxis.grid(linestyle="dashed")
    ax1.set_axisbelow(True)
    ax1.set_xlabel("Hour")

    ax2.bar(x_sulewana, y2_sulewana, alpha=0.8)
    ax2.set_ylabel("Rainfall (mm)")
    ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
    ax2.set_ylim(0, round(y2_sulewana.max())+2)
    ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    st.pyplot(plt)

with pandiri_rf:
    x_pandiri = forecast_pandiri["datetime"].dt.strftime('%H')
    y1_pandiri = forecast_pandiri["precipitation"]
    y2_pandiri = forecast_pandiri["rainfall"]

    col1_pandiri, col2_pandiri, col3_pandiri = st.columns(3)

    with col1_pandiri:
        max_prec_pandiri = y1_pandiri.max()
        st.metric("Highest Precipitation:", f"{max_prec_pandiri:n} %")
    with col2_pandiri:
        sum_rain_pandiri = y2_pandiri.sum()
        st.metric("Rainfall per Day:", f"{round(sum_rain_pandiri,1):n} mm")
    with col3_pandiri:
        count_rain_pandiri = y2_pandiri[y2_pandiri > 0].count()
        st.metric("Hours of Rain:", f"{count_rain_pandiri:n} hour(s)")

    fig, ax1 = plt.subplots(figsize=(15, 5))
    ax2 = ax1.twinx()

    ax1.plot(x_pandiri, y1_pandiri, alpha=0.8, marker="o", color="white")
    ax1.set_ylabel("Precipitation (%)")
    ax1.legend(["Precipitation"], loc="center right",
               bbox_to_anchor=(0.5, -0.2))
    ax1.set_ylim(0, 100)
    ax1.yaxis.grid(linestyle="dashed")
    ax1.set_axisbelow(True)
    ax1.set_xlabel("Hour")

    ax2.bar(x_pandiri, y2_pandiri, alpha=0.8)
    ax2.set_ylabel("Rainfall (mm)")
    ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
    ax2.set_ylim(0, round(y2_pandiri.max())+2)
    ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    st.pyplot(plt)
