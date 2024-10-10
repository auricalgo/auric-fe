import datetime
import random
import os
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from nandan import final_run

# Show app title and description.
st.set_page_config(page_title="Auric Algo", page_icon="🎫",layout="wide")
st.title("🎫 Customised Strategy")
st.write(
    """
    """
)

if "df" not in st.session_state:
    np.random.seed(42)
    if os.path.exists('live.csv'):
        df = pd.read_csv('live.csv')
        # df = df.drop(['Unnamed: 0'],axis=1)
        st.session_state.df = df
    else:
        st.session_state.df = pd.DataFrame()

if 'run_button' in st.session_state and st.session_state.run_button == True:
    st.session_state.running = True
else:
    st.session_state.running = False

submitted = False
st.header("Today's Run")
if st.session_state.df.shape[0]:
    st.session_state.df['date_of_run'] = pd.to_datetime(st.session_state.df['date_of_run'], infer_datetime_format=True, errors='coerce')
    st.session_state.df['date_of_run'] = pd.to_datetime(st.session_state.df['date_of_run'], format='%d/%m/%y').dt.date

    df12 = pd.read_csv('timesheet.csv')
    df12 = df12.drop(['Unnamed: 0'],axis=1,errors='ignore')

    df12['date_of_run'] = pd.to_datetime(df12['date_of_run'], format='%d/%m/%y', errors='coerce')
    df12['time_of_run'] = pd.to_timedelta(df12['time_of_run'])
    df12['exact_time'] = df12['date_of_run'] + df12['time_of_run']

    today = datetime.datetime.now()
    yesterday = today - pd.Timedelta(days=1)
    yesterday_330_pm = yesterday.replace(hour=15, minute=30, second=0, microsecond=0)
    today_915_am = today.replace(hour=9, minute=15, second=0, microsecond=0)
    today_330_pm = today.replace(hour=15, minute=30, second=0, microsecond=0)


    max_date = df12['date_of_run'].dt.date.max()
    max_time = df12[df12['date_of_run'] == max_date]['time_of_run'].max()
    max_datetime = df12['exact_time'].max()

    if yesterday_330_pm <= today <= today_330_pm and max_datetime < today_330_pm:
        st.write("Run Completed for Today - ",max_date)
        st.session_state.running = True
        filtered_df = st.session_state.df[st.session_state.df['date_of_run'] == max_date]
        st.dataframe(filtered_df)
    elif today > today_330_pm and max_datetime > today_330_pm:
        st.write("Run Completed for Today - ",max_date)
        st.session_state.running = True
        filtered_df = st.session_state.df[st.session_state.df['date_of_run'] == max_date]
        st.dataframe(filtered_df)
    else:
        submitted  = st.button('Run',disabled=st.session_state.running, key='run_button')
else:
        submitted  = st.button('Run',disabled=st.session_state.running, key='run_button')

if submitted:
    df = final_run()
    st.dataframe(df)
    df1 = pd.read_csv('live.csv')
    st.session_state.df = df1

st.header("History")
st.dataframe(st.session_state.df,use_container_width=True)