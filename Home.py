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

st.set_page_config(page_title="Hidrologi PLTA Poso",
                   page_icon=":mostly_sunny:", layout="wide")

with st.sidebar:
    st.markdown(
        """
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"] {
            width: 20% !important;
        }
    </style>
    """, unsafe_allow_html=True)

st.write("# Welcome to Hidrologi PLTA Poso! 👋")

st.markdown(
    """
        **👈 Select a page from the dropdown on the left** to see more options
        of what this site offers!

        ### Contents

        - Weather forecast data scraping from [AccuWeather](https://www.accuweather.com/id)
        - Weather forecast data scraping from [Weather](https://weather.com/id-ID)
        - More to come later... Soon 😉

        ### Credits

        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        - Made with [streamlit.io](https://streamlit.io)
        - Check out the Developer at [GitHub](https://github.com/AchmadNoer)
    """
)
