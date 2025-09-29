import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import altair as alt
import re
import gspread
from google.oauth2.service_account import Credentials
from streamlit_gtag import st_gtag
import os, json

# Add a name to the page, icon and enlarge the screen
st.set_page_config(
    page_title="Cyclistic Chicago",
    page_icon=":bike",
    layout="wide"
)

# We reduced the empty space at the beginning of the streamlit
reduce_space ="""
            <style type="text/css">
            /* Remueve el espacio en el encabezado por defecto de las apps de Streamlit */
            div[data-testid="stAppViewBlockContainer"]{
                padding-top:30px;
            }
            </style>
            """
# We load reduce_space
st.html(reduce_space)

#==========================================================================================================================
# Code to measure audience with Google Analytics

st_gtag(
    key="gtag_send_event_page_load",
    id="G-4E6650JC15",
    event_name="app_main_page_load",
    params={
        "event_category": "page_load",
        "event_label": "main_page",
        "value": 1,
    },
)
#==========================================================================================================================

def center_picture(image, width):
    # Apply CSS style to center image with Markdown
    st.markdown(
        f'<div style="display: flex; justify-content: center;">'
        f'<img src="{image}" width="{width}">'
        f'</div>',
        unsafe_allow_html=True
    )

def line(size, color):
    st.markdown(f"<hr style= height:{size}px;border:none;color:{color};background-color:{color}; />",
                unsafe_allow_html=True)
    return

def center_text(text, size, color):
    st.markdown(f"<h{size} style='text-align: center; color: {color}'>{text}</h{size}>",
                unsafe_allow_html=True)


def text_left(text, size, color):
    st.markdown(f"<h{size} style='text-align: left; color: {color}'>{text}</h{size}>",
                unsafe_allow_html=True)


def center_text_link(link_text, link_url, size, color):
    texto_html = f"<h{size} style='text-align: center; color: {color}'><a href='{link_url}' target='_blank'>{link_text}</a></h{size}>"
    st.markdown(texto_html, unsafe_allow_html=True)


# Título de la aplicación
center_picture('https://github.com/Willy71/background/blob/main/picture/Coursera.png?raw=true', 700)
#center_text("Cyclistic Bike-Share Chicago", 1, 'white')
center_text("Bicycle Rental Analysis", 2, 'white')
center_text("Case study done in Python for Coursera - by Guillermo Cerato", 3, 'white')

line(4, "#2a30e3")
with st.container():
    col120, col121, col122, col123, col124 = st.columns(5)
    with col121:
        center_picture("https://github.com/Willy71/cyclistic/blob/main/pictures/Coursera.png?raw=true", 90)
    with col123:
        center_picture("https://github.com/Willy71/cyclistic/blob/main/pictures/Google.jpg?raw=true", 150)
line(4, "#2a30e3")
center_text("Cyclistic, a bike-sharing company in Chicago, needs to figure out how to convince casual cyclists to purchase an annual service package. The company's future growth depends on this as annual packages are much more profitable than daily or hourly passes.", 4, 'white')
line(4, "#2a30e3")

center_text(
    'The analysis was based on annual data, between June 2023 and May 2024.', 4, 'white')
center_text(
    'The data is public and can be downloaded from the following link:', 4, 'white')
center_text_link('Download the data here',
                 'https://divvy-tripdata.s3.amazonaws.com/index.html', 4, 'white')
line(4, "#2a30e3")
center_text("Questions", 2, 'white')
center_text(
    "1 - Why would this past year's casual cyclists pay for an annual membership?", 4, 'white')
center_text(
    "2 - What is the difference between the use of bicycles by casual users and annual users?", 4, 'white')
center_text(
    "3 - What metrics can I use to convince a cyclist to purchase an annual membership?", 4, 'white')
center_text(
    "4 - What advantage would a casual customer have as a member customer?", 4, 'white')
line(8, "#2a30e3")

# =================================================================================================================================================
# Conection to Google Sheets
# Path to credentials file
SERVICE_ACCOUNT_INFO = json.loads(os.environ["GSHEETS_CREDENTIALS"])

# Necessary Scopes
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

# Load credentials and authorize
credentials = Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES)
gc = gspread.authorize(credentials)

# Spreadsheet key (the part of the URL after "/d/" and before "/edit")
# Replace with your document key
SPREADSHEET_KEY = '1xM9dD_v9JjcY9oi5RJ3PuIV9hU0S6ijc48NvLeIlGgQ'
# Loading the data
SHEET_001 = "01_freq_type_of_client"
SHEET_002 = "02_average_duration"
SHEET_003 = "03_day_hour_distribution"
SHEET_004 = "04_monthly_distribution"
SHEET_005 = "05_day_week_distribution"
#SHEET_006 = "06_common_routes"
SHEET_007 = "07_bicycle_of_preference"
SHEET_008 = "08_time_travel"

try:
    ws_01 = gc.open_by_key(SPREADSHEET_KEY).worksheet(SHEET_001)
    df1 = pd.DataFrame(ws_01.get_all_records())
    ws_02 = gc.open_by_key(SPREADSHEET_KEY).worksheet(SHEET_002)
    df2 = pd.DataFrame(ws_02.get_all_records())
    ws_03 = gc.open_by_key(SPREADSHEET_KEY).worksheet(SHEET_003)
    df3 = pd.DataFrame(ws_03.get_all_records())
    ws_04 = gc.open_by_key(SPREADSHEET_KEY).worksheet(SHEET_004)
    df4 = pd.DataFrame(ws_04.get_all_records())
    ws_05 = gc.open_by_key(SPREADSHEET_KEY).worksheet(SHEET_005)
    df5 = pd.DataFrame(ws_05.get_all_records())
    # ws_06 = gc.open_by_key(SPREADSHEET_KEY).worksheet(SHEET_006)
    # df6 = pd.DataFrame(ws_06.get_all_records())
    ws_07 = gc.open_by_key(SPREADSHEET_KEY).worksheet(SHEET_007)
    df7 = pd.DataFrame(ws_07.get_all_records())
    ws_08 = gc.open_by_key(SPREADSHEET_KEY).worksheet(SHEET_008)
    df8 = pd.DataFrame(ws_08.get_all_records())
except gspread.exceptions.SpreadsheetNotFound:
    st.error(
        f"The spreadsheet with the key was not found '{SPREADSHEET_KEY}'. Please make sure the key is correct and that you have shared the sheet with the service customer email.")
# =================================================================================================================================================


center_text("From the data analysis it is observed:", 2, 'white')
line(8, "#2a30e3")

center_text(
    "Member customers request more bicycles than casual customers", 2, 'white')
center_text("Type of customer (Percentages)", 3, 'white')
# Pie Chart with Labels altair
# Create a column for the combined labels
df1['labels'] = df1.apply(lambda row: f"{row['percentage']:.1f}%", axis=1)

color_scale = alt.Scale(
    domain=['member', 'casual'],
    range=['#E66A00', 'blue']
)

with st.container():
    col01, col02, col03, col04 = st.columns([1, 5, 1, 0.5])
    with col02:
        base = alt.Chart(df1).encode(
            alt.Theta(field="percentage", type="quantitative").stack(True),
            alt.Color(field="member_casual", type="nominal", scale=color_scale).legend(
                labelColor='white', title="Users type", titleColor='white').legend(None)  # legend(labelColor='white', title="Users type", titleColor='white')
        )

        pie = base.mark_arc(outerRadius=150)

        text = base.mark_text(
            radius=200,
            size=30
        ).encode(
            text=alt.Text(field="labels")
        )
        st.altair_chart(pie + text, use_container_width=True)
    with col03:
        st.header("")
        center_picture(
            "https://github.com/Willy71/cyclistic/blob/main/pictures/User%20type.png?raw=true", 150)

line(8, "#2a30e3")
center_text(
    "Casual customers use the bicycle more but for much longer on average than members.", 2, 'white')
# Frequency by type of client
center_text('Average usage time by type of customer', 3, 'white')
df2['minutes'] = df2["average_duration_sec"]/60
c = (
    alt.Chart(df2).mark_bar().encode(
        x=alt.X("member_casual", title=None),
        y=alt.Y("minutes", title=None),
        color=alt.condition(
            # If the year is 1810 this test returns True,
            alt.datum.member_casual == "member",
            alt.value('#E66A00'),     # which sets the bar orange.
            # And if it's not true it sets the bar steelblue.
            alt.value('blue')
        ))
).properties(width=100, height=500)

with st.container():
    col10, col11, col12, col14 = st.columns([1, 5, 1, 0.5])
    with col11:
        st.altair_chart(c, use_container_width=True)
    with col12:
        st.header("")
        center_picture(
            "https://github.com/Willy71/cyclistic/blob/main/pictures/User%20type.png?raw=true", 150)

line(8, "#2a30e3")


center_text(
    "The relationship between renting classic or electric bicycles is almost the same.", 2, 'white')
g = (
    alt.Chart(df7).mark_bar().encode(
        x=alt.X('count', title=None).stack("zero"),
        y=alt.Y('rideable_type', title=None),
        color=alt.condition(
            # If the year is 1810 this test returns True,
            alt.datum.member_casual == "member",
            alt.value('#E66A00'),     # which sets the bar orange.
            # And if it's not true it sets the bar steelblue.
            alt.value('blue'),
        )
    )
).properties(height=300)

text = alt.Chart(df7).mark_text(dx=-40, dy=2, color='white', size=20).encode(
    x=alt.X('member_casual', title=None).stack('center'),
    y=alt.Y('rideable_type', title=None),
    detail='member_casual',
    text=alt.Text('count', format='.1f')
)

with st.container():
    col20, col21, col22, col23 = st.columns([1, 5, 1, 0.5])
    with col21:
        st.altair_chart(g + text, use_container_width=True)
    with col22:
        st.header("")
        center_picture(
            "https://github.com/Willy71/cyclistic/blob/main/pictures/User%20type.png?raw=true", 150)

line(8, "#2a30e3")

center_text("Friday, Saturday and Sunday are the days with the highest attendance of casual customers, ideal days to run a promotion.", 2, 'white')
h = alt.Chart(df5).mark_bar().encode(
    x=alt.X('weekday', sort=['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']),
    y=alt.Y('count').stack("zero"),
    color=alt.condition(
        # If the year is 1810 this test returns True,
        alt.datum.member_casual == "member",
        alt.value('#E66A00'),     # which sets the bar orange.
        # And if it's not true it sets the bar steelblue.
        alt.value('blue'),
    ),
).properties(width=50, height=450)

text = alt.Chart(df5).mark_text(dx=5, dy=10, color='white', size=15).encode(
    x=alt.X('weekday', sort=['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']).stack('center'),
    y=alt.Y('count'),
    detail='member_casual',
    text=alt.Text('count', format='.1f')
)

with st.container():
    col30, col31, col32, col33 = st.columns([1, 5, 1, 0.5])
    with col31:
        st.altair_chart(h+text, use_container_width=True)
    with col32:
        st.header("")
        center_picture(
            "https://github.com/Willy71/cyclistic/blob/main/pictures/User%20type.png?raw=true", 150)

line(8, "#2a30e3")


center_text("The percentage increase between the winter and summer months is 281.51%. Winter (December, January and February) 592.110 users, Summer (June, July and August) 2.258.961 users", 2, 'white')
month_map = {
    1: 'January 2024', 2: 'February 2024', 3: 'March 2024', 4: 'April 2024',
    5: 'May 2024', 6: 'June 2023', 7: 'July 2023', 8: 'August 2023',
    9: 'September 2023', 10: 'October 2023', 11: 'November 2023', 12: 'December 2023'
}
df4['month_name'] = df4['month'].map(month_map)

i = alt.Chart(df4).mark_bar().encode(
    x=alt.X('month_name', sort=['June 2023', 'July 2023', 'August 2023', 'September 2023', 'October 2023',
            'November 2023', 'December 2023', 'January 2024', 'February 2024', 'March 2024', 'April 2024', 'May 2024']),
    y=alt.Y('count').stack("zero"),
    color=alt.condition(
        # If the year is 1810 this test returns True,
        alt.datum.member_casual == "member",
        alt.value('#E66A00'),     # which sets the bar orange.
        # And if it's not true it sets the bar steelblue.
        alt.value('blue'),
    )
).properties(width=50, height=450)

with st.container():
    col40, col41, col42, col43 = st.columns([1, 5, 1, 0.5])
    with col41:
        st.altair_chart(i, use_container_width=True)
    with col42:
        st.header("")
        center_picture(
            "https://github.com/Willy71/cyclistic/blob/main/pictures/User%20type.png?raw=true", 150)


line(8, "#2a30e3")

center_text("The busiest time slot is between 4 and 6 p.m.", 2, 'white')

# Group the data by time and member type, adding up the counts
grouped_data = df3.groupby(['hour', 'member_casual']).sum().reset_index()

# Remove the 'weekday' column as it is not needed
grouped_data = grouped_data.drop(columns=['weekday'], errors='ignore')


center_text('Number of clients per hour', 3, 'white')
i = alt.Chart(grouped_data).mark_bar().encode(
    x=alt.X('hour'),
    y=alt.Y('count').stack("zero"),
    color=alt.condition(
        # If the year is 1810 this test returns True,
        alt.datum.member_casual == "member",
        alt.value('#E66A00'),     # which sets the bar orange.
        # And if it's not true it sets the bar steelblue.
        alt.value('blue'),
    )
).properties(width=80, height=450)

with st.container():
    col50, col51, col52, col53 = st.columns([1, 5, 1, 0.5])
    with col51:
        st.altair_chart(i, use_container_width=True)
    with col52:
        st.header("")
        center_picture(
            "https://github.com/Willy71/cyclistic/blob/main/pictures/User%20type.png?raw=true", 150)


line(8, "#2a30e3")

with st.container():
    col60, col61, col62 = st.columns([2, 3, 3])
    with col61:
        center_text("Casual", 3, 'white')
        center_text("$1 + $0.18/min", 5, 'white')
    with col62:
        center_text("Member", 3, "white")
        center_text("$143.90/year", 5, "white")

st.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """,
            unsafe_allow_html=True)

with st.container():
    col70, col71, col72 = st.columns(3)
    with col70:
        text_left("Classic bike prices", 5, "white")
        st.subheader("")
        text_left("Ebike prices", 5, "white")
    with col71:
        text_left("$1 unlock + $0.18/min", 5, "white")
        st.subheader("")
        text_left("$1 unlock + $0.44/min", 5, "white")
    with col72:
        text_left("45 min free, then $0.18/min", 5, "white")
        st.subheader("")
        text_left("Free unlocks + $0.18/min", 5, "white")

line(8, "#2a30e3")

center_text('Final Conclusions.', 1, 'white')
line(8, "#2a30e3")
text_left(
    "1- Why would last year's casual riders purchase an annual membership?", 2, "white")
st.text('')
text_left("Long-term savings:", 3, "orange")
text_left("If a casual rider rents an electric bike for 28 minutes each use, averaging 2 times per week, they would spend approximately $1,324.16 annually. The annual membership of $143.90 is a much more economical option in the long run, especially considering members have free electric bike unlocks.", 4, "white")
st.text('')
text_left("Flexibility and convenience:", 3, "orange")
text_left("Members enjoy 45 free minutes per day on classic bikes and free unlocks on electric ones, allowing for short trips without time concerns. This is particularly appealing for those using bikes for short commutes or city exploration.", 4, "white")
st.text('')
text_left("Priority access:", 3, "orange")
text_left("Members can have priority access to bikes, especially during peak hours or special events, avoiding long waits.", 4, "white")
st.text('')
st.text('')
line(8, "#2a30e3")
text_left("2 - What is the difference in bike usage between casual and annual users?", 2, 'white')
st.text('')
text_left("The metrics clearly show some differences:", 3, "white")
st.text('')
text_left("Trip duration: ", 3, "orange")
text_left("Casual users take longer trips (average 28 minutes) compared to members (average 13 minutes). This suggests members use bikes for shorter, more frequent trips.", 4, "white")
st.text('')
text_left("Peak usage days: ", 3, "orange")
text_left("Weekends are peak days for casual users, while members use bikes throughout the week.", 4, "white")
st.text('')
text_left("Seasonality: ", 3, "orange")
text_left("Bike usage increases significantly in summer, indicating many casual users use the service seasonally.", 4, "white")
st.text('')
st.text('')
line(8, "#2a30e3")
text_left("3- What metrics can I use to convince a rider to purchase an annual membership?", 2, 'white')
st.text('')
text_left("Cost comparison: ", 3, "orange")
text_left("Considering the average casual customer uses 28 minutes per rental, if they rented twice a week, they would spend approximately $1,324.16 annually, while the annual membership is only $143.90.", 4, "white")
st.text('')
text_left("Flexibility: ", 3, "orange")
text_left("Members enjoy 45 free minutes daily, versus the 28-minute average for casual users.", 4, "white")
st.text('')
st.text('')
line(8, "#2a30e3")
text_left("4 - What advantage would a casual customer have as a member?", 2, 'white')
st.text('')
text_left(
    "The primary advantages for a casual customer becoming a member are:", 3, "white")
st.text('')
text_left("Cost savings:", 3, "orange")
text_left("As mentioned, membership is more economical in the long run.", 4, "white")
st.text('')
text_left("Greater flexibility:", 3, "orange")
text_left(
    "Members have more freedom to use the bike without time restrictions.", 3, "white")
st.text('')
text_left("Convenience:", 3, "orange")
text_left("Membership simplifies the rental process and avoids making payments each time.", 4, "white")
st.text('')
text_left("Priority access:", 3, "orange")
text_left("Members can enjoy priority access to bikes.", 4, "white")
st.text('')
st.text('')
line(8, "#2a30e3")
text_left("Key improvements:", 2, 'white')
st.text('')
text_left("Clarity and conciseness:", 4, "orange")
text_left("The language is more direct and focused on the key points.", 4, "white")
st.text('')
text_left("Data-driven:", 4, "orange")
text_left("The analysis is grounded in specific data points, making the conclusions more convincing.", 4, "white")
st.text('')
text_left("Customer-centric:", 4, "orange")
text_left("The benefits are presented from the customer's perspective, highlighting how membership can improve their experience.", 4, "white")
st.text('')
text_left("Call to action:", 4, "orange")
text_left("The text implicitly encourages casual riders to consider membership.", 4, "white")
line(8, "#2a30e3")

