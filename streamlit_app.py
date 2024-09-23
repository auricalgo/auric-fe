import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from nandan import final_run

# Show app title and description.
st.set_page_config(page_title="Auric Algo", page_icon="🎫")
st.title("🎫 Customised Strategy")
st.write(
    """
    """
)

if "df" not in st.session_state:
    np.random.seed(42)
    df = pd.read_csv('live.csv')
    df = df.drop(['Unnamed: 0'],axis=1)
    st.session_state.df = df

if 'run_button' in st.session_state and st.session_state.run_button == True:
    st.session_state.running = True
else:
    st.session_state.running = False


st.header("Today's Run")
if st.session_state.df.shape[0]:
    st.session_state.df['date_of_run'] = pd.to_datetime(st.session_state.df['date_of_run'], format='%d/%m/%y')
    latest_date_of_run = st.session_state.df['date_of_run'].max()
    today = datetime.datetime.now()
    if latest_date_of_run == today.date():
        st.write("Run Completed for Today - ",datetime.datetime.today().strftime('%Y-%m-%d'))
        submitted = False
        st.session_state.running = True
        filtered_df = st.session_state.df[st.session_state.df['date_of_run'] == latest_date_of_run]
        st.dataframe(filtered_df)
    else:
        submitted  = st.button('Run',disabled=st.session_state.running, key='run_button')

if submitted:
    df = final_run()
    st.dataframe(df)
    df1 = pd.read_csv('live.csv')
    df1 = df1.drop(['Unnamed: 0'],axis=1)
    st.session_state.df = df1

st.header("History")
st.dataframe(st.session_state.df,use_container_width=True)