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

    # Set seed for reproducibility.
    np.random.seed(42)
    df = pd.read_csv('live.csv')
    df = df.drop(['Unnamed: 0'],axis=1)
    print(df)
    st.session_state.df = df


# Show a section to add a new ticket.
st.header("Today's Run")
if st.session_state.df.shape[0]:
    st.session_state.df['date_of_run'] = pd.to_datetime(st.session_state.df['date_of_run'], format='%d/%m/%y')
    latest_date_of_run = st.session_state.df['date_of_run'].max()
    today = datetime.datetime.now()
    if latest_date_of_run == today.date():
        st.write("Run Completed for Today - ",datetime.datetime.today().strftime('%Y-%m-%d'))
        submitted = False
    else:
        submitted  = st.button('Run')

if submitted:
    df = final_run()
    st.dataframe(df)

# today = datetime.datetime.now().strftime("%m-%d-%Y")
# df_new = pd.DataFrame(
#     [
#         {
#             "Status": "Open",
#             "Date Submitted": today,
#         }
#     ]
# )

# Show a little success message.
st.write("Here are the details:")
# st.dataframe(df_new, use_container_width=True, hide_index=True)
# st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

# Show section to view and edit existing tickets in a table.
st.header("History")
st.dataframe(st.session_state.df,use_container_width=True)

# st.info(
#     "You can edit the tickets by double clicking on a cell. Note how the plots below "
#     "update automatically! You can also sort the table by clicking on the column headers.",
#     icon="✍️",
# )

# Show the tickets dataframe with `st.data_editor`. This lets the user edit the table
# cells. The edited data is returned as a new dataframe.
# edited_df = st.data_editor(
#     st.session_state.df,
#     use_container_width=True,
#     hide_index=True,
#     column_config={
#         "Status": st.column_config.SelectboxColumn(
#             "Status",
#             help="Ticket status",
#             options=["Open", "In Progress", "Closed"],
#             required=True,
#         ),
#         "Priority": st.column_config.SelectboxColumn(
#             "Priority",
#             help="Priority",
#             options=["High", "Medium", "Low"],
#             required=True,
#         ),
#     },
#     # Disable editing the ID and Date Submitted columns.
#     disabled=["ID", "Date Submitted"],
# )

# # Show some metrics and charts about the ticket.
# st.header("Statistics")

# # Show metrics side by side using `st.columns` and `st.metric`.
# col1, col2, col3 = st.columns(3)
# num_open_tickets = len(st.session_state.df[st.session_state.df.Status == "Open"])
# col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
# col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
# col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# # Show two Altair charts using `st.altair_chart`.
# st.write("")
# st.write("##### Ticket status per month")
# status_plot = (
#     alt.Chart(edited_df)
#     .mark_bar()
#     .encode(
#         x="month(Date Submitted):O",
#         y="count():Q",
#         xOffset="Status:N",
#         color="Status:N",
#     )
#     .configure_legend(
#         orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
#     )
# )
# st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

# st.write("##### Current ticket priorities")
# priority_plot = (
#     alt.Chart(edited_df)
#     .mark_arc()
#     .encode(theta="count():Q", color="Priority:N")
#     .properties(height=300)
#     .configure_legend(
#         orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
#     )
# )
# st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")
