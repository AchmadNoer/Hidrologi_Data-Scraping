from dateutil import relativedelta
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from matplotlib.ticker import FormatStrFormatter
import warnings
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
plt.style.use("dark_background")

st.set_page_config(page_title="Forecast - Weather.com",
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

    date_list = pd.date_range(datetime.now().strftime('%d %B %Y'), periods=2).format(
        formatter=lambda x: x.strftime('%d %B %Y'))
    option = st.selectbox("Please Select Date", date_list)

    day = (pd.to_datetime(option) - datetime.now()).days + 1

web_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}

tentena = "https://weather.com/id-ID/weather/hourbyhour/l/7b9340fda49387b63ac66d4cbd3486fa306c173b88fcfdc87709428eb8f6133945a5fe34d43e820fd42b50181226e5fe?unit=m"
salukaia = "https://weather.com/id-ID/weather/hourbyhour/l/15f4ff4b88a7d5bc5edacda4b6a3a248160efda10f5ff3649103d441e11aa78c898d1ca063e531f97aa1d4254a2f70a9?unit=m"
panjo = "https://weather.com/id-ID/weather/hourbyhour/l/627c444b60529213032e9466655ba376b0e8b676c07e79f0c506c42fa3686160b1b65cea1e41a9e289911f7aceccfe25?unit=m"
mayoa = "https://weather.com/id-ID/weather/hourbyhour/l/872b3188e907e3fdc999a88e365e6ac2c8d4726cb8597c26fdba4e0c13dacce3a1146825d7634cca605079216df1c229?unit=m"
tindoli = "https://weather.com/id-ID/weather/hourbyhour/l/20515b497b1367e2407770c38e0d57c1858faf744cafc13e10637efbd2a1695d925b5d72c48c13cf4cbec4b55ca7ea84?unit=m"
sulewana = "https://weather.com/id-ID/weather/hourbyhour/l/089d52851167204cab70c25c4dfe195c4eab8d1e61ed4757f890cbcdeeb7b218d77f59a29b3fad1b8849c44305badc06?unit=m"
pandiri = "https://weather.com/id-ID/weather/hourbyhour/l/28025aa10e0b0b615ffa036b5ee5a30238b9f10ec577293c163a60558b5d72ff77dbcc78af90874daf728c4e7d2212fa?unit=m"


def datetime_list():
    start_time = datetime.now(tz=timezone(
        timedelta(hours=8))) + relativedelta.relativedelta(hours=1)
    end_time = start_time + relativedelta.relativedelta(hours=47)

    date_time = pd.date_range(start=start_time, end=end_time, freq="1h")
    date_time = date_time.format(
        formatter=lambda x: x.strftime('%d/%m/%Y %H:00'))

    return date_time


def scraping(lokasi):
    date_time = datetime_list()
    response = requests.get(lokasi, headers=web_headers)
    soup = BeautifulSoup(response.content, "html.parser")

    tag_probabilities = soup.find_all(
        "span", attrs={"data-testid": "PercentageValue", "class": ""})
    tag_rainfall = soup.find_all("span", attrs={
                                 "data-testid": "AccumulationValue", "class": "DetailsTable--value--2YD0-"})
    probabilitas = [isi.string for isi in tag_probabilities]
    hujan = [isi.find("span", recursive=False).string for isi in tag_rainfall]

    konten = pd.DataFrame(list(zip(date_time, probabilitas, hujan)))
    konten.columns = ["datetime", "probabilities", "rainfall"]
    konten["datetime"] = pd.to_datetime(
        konten["datetime"], format="%d/%m/%Y %H:%M")
    konten["probabilities"] = konten["probabilities"].map(
        lambda x: x.rstrip('%')).astype("int64")
    konten["rainfall"] = konten["rainfall"].astype("float64")
    # konten["rainfall"] = konten["rainfall"].apply(lambda x: x if x > 1 else 0)

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

st.header("Weather Forecast Data Scraping :mostly_sunny: - weather.com")
st.subheader("Rainfall All Station 	:house:")

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
    y1_tentena = forecast_tentena["probabilities"]
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
    y1_salukaia = forecast_salukaia["probabilities"]
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
    y1_panjo = forecast_panjo["probabilities"]
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
    y1_mayoa = forecast_mayoa["probabilities"]
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
    y1_tindoli = forecast_tindoli["probabilities"]
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
    y1_sulewana = forecast_sulewana["probabilities"]
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
    y1_pandiri = forecast_pandiri["probabilities"]
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
