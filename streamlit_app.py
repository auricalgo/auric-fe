import datetime
import random
import os
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import requests

from nandan import final_run

# Show app title and description.
st.set_page_config(page_title="Auric Algo", page_icon="🎫",layout="wide")
st.title("🎫 Customised Strategy")
st.write(
    """
    """
)

st.header("Today's Run")
data = requests.get("'http://ec2-15-207-116-252.ap-south-1.compute.amazonaws.com/api/get_today_data'").json()
st.dataframe(data,use_container_width=True)


st.header("History")
data1 = requests.get("'http://ec2-15-207-116-252.ap-south-1.compute.amazonaws.com/api/get_data'").json()
st.dataframe(data1,use_container_width=True)