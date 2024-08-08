import streamlit as st

# Add a name to the page, icon and enlarge the screen
st.set_page_config(
    page_title="Backend - Cyclistic Chicago",
    page_icon=":bike",
    layout="wide"
)


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


st.write("#")
line(6, "#22c519")
center_text("Complete tutorial of the practical work for the Google data analyst course provided by Coursera.", 2, "white")
line(6, "#22c519")

text_left("The first thing we need to do is download 12 consecutive months of data. The files will be downloaded as ZIPs and then unzipped. In my case I placed them in the “cyclistic/datasets/Origin” folder.", 5, "white")
st.text("")
center_picture(
    "https://github.com/Willy71/cyclistic/blob/main/pictures/Backend_001.png?raw=true", 500)
st.text("")
line(4, "#22c519")
text_left("After unzipping it we will start with the ETL (Extract, transform, and load) process.", 4, "white")
st.text("")
text_left("For this we will create a first PY file with the name “001_read_clean.py” which will be responsible for reading all the files downloaded and unzipped in the aforementioned folder, with the following code:", 5, "white")

code_01 = """
# C:/Cyclistic/001_read_clean.py

import pandas as pd
import os

list_df = []
list_name = []
# Specify the path where your CSV files are
directory = "C:/Cyclistic/datasets/Origin"
directory_final = "C:/Cyclistic/datasets"

# List all CSV files in the specified path 
for paths in os.listdir(directory):   
    if paths.endswith(".csv"):
        name_path = "/" + paths
        name_df = pd.read_csv(directory+name_path, sep=',', encoding='latin-1')
        # drop duplicates
        name_df.drop_duplicates()
        # delete columns that I am not going to use 
        name_df.drop('ride_id', axis = 1, inplace=True)
        name_df.drop('start_station_name', axis = 1, inplace=True)
        name_df.drop('start_station_id', axis = 1, inplace=True)
        name_df.drop('end_station_name', axis = 1, inplace=True)
        name_df.drop('end_station_id', axis = 1, inplace=True)
        # Overwrite each file with changes
        name_df.to_csv(directory_final+paths, index=False)
        list_df.append(name_df)
"""

st.code(code_01, language='python')
st.text("")
text_left("What this code does is the following:", 5, "white")
text_left("It reads the twelve files, removes duplicate data, removes some columns that it considers were not necessary for my analysis, and then saves them back to another folder.", 5, "white")
line(4, "#22c519")
text_left("Then we create another PY file called '002_concat.py' that will be used to join the twelve files into one file called 'data_joins.csv'", 5, "white")
st.text("")

code_02 = """
# Cyclistic/002_concat.py

import pandas as pd
import os

# Specify the path where your CSV files are
file_path = 'C:/Cyclistic/datasets'

# List all CSV files in the specified path
path_csv = [os.path.join(file_path, path) for path in os.listdir(file_path) if path.endswith('.csv')]

# List to store the DataFrames
dataframes = []

# Read and store each DataFrame in the list
for path in path_csv:
    df = pd.read_csv(path)
    dataframes.append(df)

# Join all DataFrames into one
df_join = pd.concat(dataframes, ignore_index=True)

# Save the joined DataFrame to a new CSV file
df_join.to_csv('C:/Cyclistic/datasets/data_joins.csv', index=False)

print("The databases have been successfully joined and saved in 'data_joins.csv'.")
"""

st.code(code_02, language='python')
line(4, "#22c519")
text_left("The following file called ‘003_columns_types.py’ is just to see the column type and if any modification needs to be made, for example from string to datetime how it will happen in the next code.", 5, "white")
code_03 = """
# Cyclistic/003_columns_types.py

import pandas as pd

path = "C:/Cyclistic/datasets/Origin/202401-divvy-tripdata.csv"

df = pd.read_csv(path)

print("Data types of columns in DataFrame")
print(df.dtypes)
"""
st.code(code_03, language='python')
line(4, "#22c519")
text_left("The following code is to convert the columns 'Started_at' and 'ended_at' to datetime.", 5, "white")
text_left("Also to calculate the duration of each rental in the new column called ‘time_sec’", 5, "white")
text_left("Also in the code we are going to create, through the column ‘started_at’ 4 new columns called ‘weekday’, ‘month’, ‘year’, ‘hour’", 5, "white")

code_04 = """
# Cyclistic/004_times.py

import pandas as pd
import datetime as dt

path = "C:/Cyclistic/data_joins.csv"

df = pd.read_csv(path)

# convert the started_at and ended_at columns to datetime format
df["started_at"] = pd.to_datetime(df["started_at"])
df["ended_at"] = pd.to_datetime(df["ended_at"])

# Create a new column with the length of the tour named time_sec, 
# containing the end of the route seconds its beginning (ended_at - started_at)
df["time_sec"] = (df["ended_at"] - df["started_at"]) / dt.timedelta(seconds=1)   

# Add 4 new columns - month - year - weekday _ hour
def my_func(x):
    return x.strftime('%A')

df["weekday"] = df["started_at"].apply(my_func)
df['month'] = df[ "started_at"].dt.month
df['year'] = df[ "started_at"].dt.year
df['hour'] = df['started_at'].dt.hour
df = df.astype({'hour':'int8'})

df.to_csv('C:/Cyclistic/datasets/finalized_data.csv', index=False)
"""
st.code(code_04, language='python')
line(4, "#22c519")
text_left("Finally, we are going to create 8 secondary files to upload to Google Sheets and create the graphics and our storytelling.", 5, "white")
code_05 = """
# Cyclistic/005_analisis.py

import pandas as pd

# Upload the large file
data = pd.read_csv('datasets/finalized_data.csv')


# Basic Descriptive Analysis

# Frequency of Use by Type of Client
freq_tipo_cliente = data.groupby('member_casual').size().reset_index(name='count')
freq_tipo_cliente['percentage'] = (freq_tipo_cliente['count'] / freq_tipo_cliente['count'].sum()) * 100
freq_tipo_cliente.to_csv('datasets/01_freq_type_of_client.csv', index=False)

# Average Trip Duration
duracion_promedio = data.groupby('member_casual')['time_sec'].mean().reset_index(name='average_duration_sec')
duracion_promedio.to_csv('datasets/02_average_duration.csv', index=False)

# Distribution of Trips by Day of the Week and Time of Day
distribucion_dia_hora = data.groupby(['weekday', 'hour', 'member_casual']).size().reset_index(name='count')
distribucion_dia_hora.to_csv('datasets/03_day_hour_distribution.csv', index=False)

# Time Segment Analysis

# Seasonality
distribucion_mensual = data.groupby(['month', 'member_casual']).size().reset_index(name='count')
distribucion_mensual.to_csv('datasets/04_monthly_distribution.csv', index=False)

# Weekday
distribucion_dia_semana = data.groupby(['weekday', 'member_casual']).size().reset_index(name='count')
distribucion_dia_semana.to_csv('datasets/05_day_week_distribution.csv', index=False)

# Geospatial Analysis

# Common Route Analysis
# Function to round and format to 2 decimal places
def round_to_2(value):
    return format(round(value, 2), '.2f')

# Apply the function to the latitude and longitude columns
data['start_lat_dec'] = data['start_lat'].apply(round_to_2)
data['start_lng_dec'] = data['start_lng'].apply(round_to_2)
data['end_lat_dec'] = data['end_lat'].apply(round_to_2)
data['end_lng_dec'] = data['end_lng'].apply(round_to_2)

# Group by rounded coordinates
rutas_comunes = data.groupby(['start_lat_dec', 'start_lng_dec', 'end_lat_dec', 'end_lng_dec', 'weekday', 'rideable_type', 'member_casual']).size().reset_index(name='count')
rutas_comunes.to_csv('datasets/06_common_routes.csv', index=False)


# Usage Analysis by Type of Bike

# Preference for Type of Bike
preferencia_bicicleta = data.groupby(['rideable_type', 'member_casual']).size().reset_index(name='count')
preferencia_bicicleta.to_csv('datasets/07_bicycle_of_preference.csv', index=False)


# Customer Satisfaction

# Journey Time Analysis
tiempo_recorrido = data.groupby('member_casual')['time_sec'].agg(['mean', 'median']).reset_index()
tiempo_recorrido.to_csv('datasets/08_time_travel.csv', index=False)
"""
st.code(code_05, language='python')
line(4, "#22c519")
text_left("At the end the files and databases would look like this:", 5, "white")
st.text("")
center_picture("https://github.com/Willy71/cyclistic/blob/main/pictures/Backend_002.png?raw=true", 500)

line(4, "#22c519")

center_text("The following is the link to the Github repository of this project.", 2, "white")

center_text_link("Github","https://github.com/Willy71/cyclistic/tree/main", 3, "blue")