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
