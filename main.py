from dateutil import relativedelta
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from matplotlib.ticker import FormatStrFormatter
import warnings
import requests
import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
sns.set(style='white')

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
    sekarang = datetime.now(tz=timezone(timedelta(hours=8)))  # GMT+8
    start_time = sekarang + relativedelta.relativedelta(hours=1)
    end_time = start_time + relativedelta.relativedelta(hours=47)

    date_time = pd.date_range(start=start_time, end=end_time, freq="1h")
    date_time = date_time.format(formatter=lambda x: x.strftime('%d/%m/%Y %H:00'))

    return date_time


def scraping(lokasi):
    date_time = datetime_list()
    response = requests.get(lokasi, headers=web_headers)
    soup = BeautifulSoup(response.content, "lxml")

    tag_condition = soup.find_all("span", attrs={"class": "DetailsSummary--extendedData--307Ax"})
    # tag_temperature = soup.find_all("span", attrs={"data-testid": "TemperatureValue", "class": "DetailsSummary--tempValue--jEiXE"})
    tag_probabilities = soup.find_all("span", attrs={"data-testid": "PercentageValue", "class": ""})
    tag_rainfall = soup.find_all("span", attrs={"data-testid": "AccumulationValue", "class": "DetailsTable--value--2YD0-"})

    kondisi = [isi.string for isi in tag_condition]
    # temperatur = [isi.text for isi in tag_temperature]
    probabilitas = [isi.string for isi in tag_probabilities]
    hujan = [isi.find("span", recursive=False).string for isi in tag_rainfall]

    konten = pd.DataFrame(list(zip(date_time, kondisi, probabilitas, hujan)))
    konten.columns = ["datetime", "condition", "probabilities", "rainfall"]
    konten["datetime"] = pd.to_datetime(konten["datetime"], format="%d/%m/%Y %H:%M")
    # konten["temperature"] = konten["temperature"].map(lambda x: x.rstrip('°')).astype("int64")
    konten["probabilities"] = konten["probabilities"].map(lambda x: x.rstrip('%')).astype("int64")
    konten["rainfall"] = konten["rainfall"].astype("float64")

    return konten


forecast_tentena = scraping(tentena)
forecast_salukaia = scraping(salukaia)
forecast_panjo = scraping(panjo)
forecast_mayoa = scraping(mayoa)
forecast_tindoli = scraping(tindoli)
forecast_sulewana = scraping(sulewana)
forecast_pandiri = scraping(pandiri)


day1 = datetime.now().strftime('%d %B %Y')
day2 = (datetime.now() + relativedelta.relativedelta(hours=24)).strftime('%d %B %Y')

st. set_page_config(layout="wide")
st.header("Weather Forecast Data Scraping - weather.com")
st.subheader("Rainfall & Precipitation")

tentena_rf, salukaia_rf, panjo_rf, mayoa_rf, tindoli_rf, sulewana_rf, pandiri_rf = st.tabs(["Tentena", "Salukaia", "Panjo", "Mayoa", "Tindoli", "Sulewana", "Pandiri"])

forecast_tentena_d1 = forecast_tentena.head(24)
forecast_salukaia_d1 = forecast_salukaia.head(24)
forecast_panjo_d1 = forecast_panjo.head(24)
forecast_mayoa_d1 = forecast_mayoa.head(24)
forecast_tindoli_d1 = forecast_tindoli.head(24)
forecast_sulewana_d1 = forecast_sulewana.head(24)
forecast_pandiri_d1 = forecast_pandiri.head(24)

forecast_tentena_d2 = forecast_tentena.tail(24)
forecast_salukaia_d2 = forecast_salukaia.tail(24)
forecast_panjo_d2 = forecast_panjo.tail(24)
forecast_mayoa_d2 = forecast_mayoa.tail(24)
forecast_tindoli_d2 = forecast_tindoli.tail(24)
forecast_sulewana_d2 = forecast_sulewana.tail(24)
forecast_pandiri_d2 = forecast_pandiri.tail(24)

with tentena_rf:
    with st.expander(day1, expanded=True):
        x_tentena = forecast_tentena_d1["datetime"].dt.strftime('%H')
        y1_tentena = forecast_tentena_d1["probabilities"]
        y2_tentena = forecast_tentena_d1["rainfall"]

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

        ax1.plot(x_tentena, y1_tentena, alpha=0.8, marker="o", color="black")
        ax1.set_ylabel("Precipitation (%)")
        ax1.legend(["Precipitation"], loc="center right",
                bbox_to_anchor=(0.5, -0.2))
        ax1.set_ylim(0, 100)
        ax1.yaxis.grid(linestyle="dashed")
        ax1.set_xlabel("Hour")

        ax2.bar(x_tentena, y2_tentena, alpha=0.8)
        ax2.set_ylabel("Rainfall (mm)")
        ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
        ax2.set_ylim(0, round(y2_tentena.max())+1)
        ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        st.pyplot(plt)

    with st.expander(day2, expanded=True):
        x_tentena = forecast_tentena_d2["datetime"].dt.strftime('%H')
        y1_tentena = forecast_tentena_d2["probabilities"]
        y2_tentena = forecast_tentena_d2["rainfall"]

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

        ax1.plot(x_tentena, y1_tentena, alpha=0.8, marker="o", color="black")
        ax1.set_ylabel("Precipitation (%)")
        ax1.legend(["Precipitation"], loc="center right",
                bbox_to_anchor=(0.5, -0.2))
        ax1.set_ylim(0, 100)
        ax1.yaxis.grid(linestyle="dashed")
        ax1.set_xlabel("Hour")

        ax2.bar(x_tentena, y2_tentena, alpha=0.8)
        ax2.set_ylabel("Rainfall (mm)")
        ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
        ax2.set_ylim(0, round(y2_tentena.max())+1)
        ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        st.pyplot(plt)


with salukaia_rf:
    with st.expander(day1, expanded=True):
        x_salukaia = forecast_salukaia_d1["datetime"].dt.strftime('%H')
        y1_salukaia = forecast_salukaia_d1["probabilities"]
        y2_salukaia = forecast_salukaia_d1["rainfall"]

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

        ax1.plot(x_salukaia, y1_salukaia, alpha=0.8, marker="o", color="black")
        ax1.set_ylabel("Precipitation (%)")
        ax1.legend(["Precipitation"], loc="center right",
                bbox_to_anchor=(0.5, -0.2))
        ax1.set_ylim(0, 100)
        ax1.yaxis.grid(linestyle="dashed")
        ax1.set_xlabel("Hour")

        ax2.bar(x_salukaia, y2_salukaia, alpha=0.8)
        ax2.set_ylabel("Rainfall (mm)")
        ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
        ax2.set_ylim(0, round(y2_salukaia.max())+1)
        ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        st.pyplot(plt)

    with st.expander(day2, expanded=True):
        x_salukaia = forecast_salukaia_d2["datetime"].dt.strftime('%H')
        y1_salukaia = forecast_salukaia_d2["probabilities"]
        y2_salukaia = forecast_salukaia_d2["rainfall"]

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

        ax1.plot(x_salukaia, y1_salukaia, alpha=0.8, marker="o", color="black")
        ax1.set_ylabel("Precipitation (%)")
        ax1.legend(["Precipitation"], loc="center right",
                bbox_to_anchor=(0.5, -0.2))
        ax1.set_ylim(0, 100)
        ax1.yaxis.grid(linestyle="dashed")
        ax1.set_xlabel("Hour")

        ax2.bar(x_salukaia, y2_salukaia, alpha=0.8)
        ax2.set_ylabel("Rainfall (mm)")
        ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
        ax2.set_ylim(0, round(y2_salukaia.max())+1)
        ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        st.pyplot(plt)


with panjo_rf:
    with st.expander(day1, expanded=True):
        x_panjo = forecast_panjo_d1["datetime"].dt.strftime('%H')
        y1_panjo = forecast_panjo_d1["probabilities"]
        y2_panjo = forecast_panjo_d1["rainfall"]

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

        ax1.plot(x_panjo, y1_panjo, alpha=0.8, marker="o", color="black")
        ax1.set_ylabel("Precipitation (%)")
        ax1.legend(["Precipitation"], loc="center right",
                bbox_to_anchor=(0.5, -0.2))
        ax1.set_ylim(0, 100)
        ax1.yaxis.grid(linestyle="dashed")
        ax1.set_xlabel("Hour")

        ax2.bar(x_panjo, y2_panjo, alpha=0.8)
        ax2.set_ylabel("Rainfall (mm)")
        ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
        ax2.set_ylim(0, round(y2_panjo.max())+1)
        ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        st.pyplot(plt)

    with st.expander(day2, expanded=True):
        x_panjo = forecast_panjo_d2["datetime"].dt.strftime('%H')
        y1_panjo = forecast_panjo_d2["probabilities"]
        y2_panjo = forecast_panjo_d2["rainfall"]

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

        ax1.plot(x_panjo, y1_panjo, alpha=0.8, marker="o", color="black")
        ax1.set_ylabel("Precipitation (%)")
        ax1.legend(["Precipitation"], loc="center right",
                bbox_to_anchor=(0.5, -0.2))
        ax1.set_ylim(0, 100)
        ax1.yaxis.grid(linestyle="dashed")
        ax1.set_xlabel("Hour")

        ax2.bar(x_panjo, y2_panjo, alpha=0.8)
        ax2.set_ylabel("Rainfall (mm)")
        ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
        ax2.set_ylim(0, round(y2_panjo.max())+1)
        ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        st.pyplot(plt)


with mayoa_rf:
    with st.expander(day1, expanded=True):
        x_mayoa = forecast_mayoa_d1["datetime"].dt.strftime('%H')
        y1_mayoa = forecast_mayoa_d1["probabilities"]
        y2_mayoa = forecast_mayoa_d1["rainfall"]

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

        ax1.plot(x_mayoa, y1_mayoa, alpha=0.8, marker="o", color="black")
        ax1.set_ylabel("Precipitation (%)")
        ax1.legend(["Precipitation"], loc="center right",
                bbox_to_anchor=(0.5, -0.2))
        ax1.set_ylim(0, 100)
        ax1.yaxis.grid(linestyle="dashed")
        ax1.set_xlabel("Hour")

        ax2.bar(x_mayoa, y2_mayoa, alpha=0.8)
        ax2.set_ylabel("Rainfall (mm)")
        ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
        ax2.set_ylim(0, round(y2_mayoa.max())+1)
        ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        st.pyplot(plt)

    with st.expander(day2, expanded=True):
        x_mayoa = forecast_mayoa_d2["datetime"].dt.strftime('%H')
        y1_mayoa = forecast_mayoa_d2["probabilities"]
        y2_mayoa = forecast_mayoa_d2["rainfall"]

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

        ax1.plot(x_mayoa, y1_mayoa, alpha=0.8, marker="o", color="black")
        ax1.set_ylabel("Precipitation (%)")
        ax1.legend(["Precipitation"], loc="center right",
                bbox_to_anchor=(0.5, -0.2))
        ax1.set_ylim(0, 100)
        ax1.yaxis.grid(linestyle="dashed")
        ax1.set_xlabel("Hour")

        ax2.bar(x_mayoa, y2_mayoa, alpha=0.8)
        ax2.set_ylabel("Rainfall (mm)")
        ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
        ax2.set_ylim(0, round(y2_mayoa.max())+1)
        ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        st.pyplot(plt)


with tindoli_rf:
    with st.expander(day1, expanded=True):
        x_tindoli = forecast_tindoli_d1["datetime"].dt.strftime('%H')
        y1_tindoli = forecast_tindoli_d1["probabilities"]
        y2_tindoli = forecast_tindoli_d1["rainfall"]

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

        ax1.plot(x_tindoli, y1_tindoli, alpha=0.8, marker="o", color="black")
        ax1.set_ylabel("Precipitation (%)")
        ax1.legend(["Precipitation"], loc="center right",
                bbox_to_anchor=(0.5, -0.2))
        ax1.set_ylim(0, 100)
        ax1.yaxis.grid(linestyle="dashed")
        ax1.set_xlabel("Hour")

        ax2.bar(x_tindoli, y2_tindoli, alpha=0.8)
        ax2.set_ylabel("Rainfall (mm)")
        ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
        ax2.set_ylim(0, round(y2_tindoli.max())+1)
        ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        st.pyplot(plt)

    with st.expander(day2, expanded=True):
        x_tindoli = forecast_tindoli_d2["datetime"].dt.strftime('%H')
        y1_tindoli = forecast_tindoli_d2["probabilities"]
        y2_tindoli = forecast_tindoli_d2["rainfall"]

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

        ax1.plot(x_tindoli, y1_tindoli, alpha=0.8, marker="o", color="black")
        ax1.set_ylabel("Precipitation (%)")
        ax1.legend(["Precipitation"], loc="center right",
                bbox_to_anchor=(0.5, -0.2))
        ax1.set_ylim(0, 100)
        ax1.yaxis.grid(linestyle="dashed")
        ax1.set_xlabel("Hour")

        ax2.bar(x_tindoli, y2_tindoli, alpha=0.8)
        ax2.set_ylabel("Rainfall (mm)")
        ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
        ax2.set_ylim(0, round(y2_tindoli.max())+1)
        ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        st.pyplot(plt)


with sulewana_rf:
    with st.expander(day1, expanded=True):
        x_sulewana = forecast_sulewana_d1["datetime"].dt.strftime('%H')
        y1_sulewana = forecast_sulewana_d1["probabilities"]
        y2_sulewana = forecast_sulewana_d1["rainfall"]

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

        ax1.plot(x_sulewana, y1_sulewana, alpha=0.8, marker="o", color="black")
        ax1.set_ylabel("Precipitation (%)")
        ax1.legend(["Precipitation"], loc="center right",
                bbox_to_anchor=(0.5, -0.2))
        ax1.set_ylim(0, 100)
        ax1.yaxis.grid(linestyle="dashed")
        ax1.set_xlabel("Hour")

        ax2.bar(x_sulewana, y2_sulewana, alpha=0.8)
        ax2.set_ylabel("Rainfall (mm)")
        ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
        ax2.set_ylim(0, round(y2_sulewana.max())+1)
        ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        st.pyplot(plt)

    with st.expander(day2, expanded=True):
        x_sulewana = forecast_sulewana_d2["datetime"].dt.strftime('%H')
        y1_sulewana = forecast_sulewana_d2["probabilities"]
        y2_sulewana = forecast_sulewana_d2["rainfall"]

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

        ax1.plot(x_sulewana, y1_sulewana, alpha=0.8, marker="o", color="black")
        ax1.set_ylabel("Precipitation (%)")
        ax1.legend(["Precipitation"], loc="center right",
                bbox_to_anchor=(0.5, -0.2))
        ax1.set_ylim(0, 100)
        ax1.yaxis.grid(linestyle="dashed")
        ax1.set_xlabel("Hour")

        ax2.bar(x_sulewana, y2_sulewana, alpha=0.8)
        ax2.set_ylabel("Rainfall (mm)")
        ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
        ax2.set_ylim(0, round(y2_sulewana.max())+1)
        ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        st.pyplot(plt)


with pandiri_rf:
    with st.expander(day1, expanded=True):
        x_pandiri = forecast_pandiri_d1["datetime"].dt.strftime('%H')
        y1_pandiri = forecast_pandiri_d1["probabilities"]
        y2_pandiri = forecast_pandiri_d1["rainfall"]

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

        ax1.plot(x_pandiri, y1_pandiri, alpha=0.8, marker="o", color="black")
        ax1.set_ylabel("Precipitation (%)")
        ax1.legend(["Precipitation"], loc="center right",
                bbox_to_anchor=(0.5, -0.2))
        ax1.set_ylim(0, 100)
        ax1.yaxis.grid(linestyle="dashed")
        ax1.set_xlabel("Hour")

        ax2.bar(x_pandiri, y2_pandiri, alpha=0.8)
        ax2.set_ylabel("Rainfall (mm)")
        ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
        ax2.set_ylim(0, round(y2_pandiri.max())+1)
        ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        st.pyplot(plt)

    with st.expander(day2, expanded=True):
        x_pandiri = forecast_pandiri_d2["datetime"].dt.strftime('%H')
        y1_pandiri = forecast_pandiri_d2["probabilities"]
        y2_pandiri = forecast_pandiri_d2["rainfall"]

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

        ax1.plot(x_pandiri, y1_pandiri, alpha=0.8, marker="o", color="black")
        ax1.set_ylabel("Precipitation (%)")
        ax1.legend(["Precipitation"], loc="center right",
                bbox_to_anchor=(0.5, -0.2))
        ax1.set_ylim(0, 100)
        ax1.yaxis.grid(linestyle="dashed")
        ax1.set_xlabel("Hour")

        ax2.bar(x_pandiri, y2_pandiri, alpha=0.8)
        ax2.set_ylabel("Rainfall (mm)")
        ax2.legend(["Rainfall"], loc="center left", bbox_to_anchor=(0.5, -0.2))
        ax2.set_ylim(0, round(y2_pandiri.max())+1)
        ax2.bar_label(ax2.containers[0], label_type="edge", fontsize=10)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        st.pyplot(plt)
