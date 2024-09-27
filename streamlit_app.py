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
    st.session_state.df['date_of_run'] = pd.to_datetime(st.session_state.df['date_of_run'], format='%d/%m/%y').dt.date
    # print(st.session_state.df['date_of_run'])
    df12 = pd.read_csv('timesheet.csv')
    df12 = df12.drop(['Unnamed: 0'],axis=1)
    df12['date_of_run'] = pd.to_datetime(df12['date_of_run'], format='%Y-%m-%d').dt.date
    df12['time_of_run'] = pd.to_datetime(df12['time_of_run'], format='%H:%M:%S').dt.time

    max_date = df12['date_of_run'].max()
    max_time = df12[df12['date_of_run'] == max_date]['time_of_run'].max()

    time_threshold_pm = pd.to_datetime('15:30:00', format='%H:%M:%S').time()
    time_threshold_am = pd.to_datetime('09:15:00', format='%H:%M:%S').time()

    today = datetime.datetime.now()
    yesterday = today - pd.Timedelta(days=1)
    today = pd.to_datetime(today).date()
    yesterday = pd.to_datetime(yesterday).date()
    if (max_date == yesterday and max_time >= time_threshold_pm) or (max_date == pd.to_datetime('today') and max_time <= time_threshold_am) :
        st.write("Run Completed for Today - ",max_date)
        st.session_state.running = True
        filtered_df = st.session_state.df[st.session_state.df['date_of_run'] == max_date]
        st.dataframe(filtered_df)
    elif (max_date == pd.to_datetime('today') and max_time <= time_threshold_pm) :
        st.write("Run Completed for Today - ",max_date)
        st.session_state.running = True
        filtered_df = st.session_state.df[st.session_state.df['date_of_run'] == max_date]
        st.dataframe(filtered_df)
    elif (max_date == pd.to_datetime('today') and max_time >= time_threshold_pm) :
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