import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px



# Load dataset 
url = 'https://practicum-content.s3.us-west-1.amazonaws.com/datasets/vehicles_us.csv'
data = requests.get(url)
with open('vehicles_us.csv', 'wb') as file:
    file.write(data.content)

car_datasets = pd.read_csv('vehicles_us.csv')

#  Data cleaning 
car_datasets['model_year'] = pd.to_numeric(car_datasets['model_year'], errors='coerce')
car_datasets = car_datasets.drop_duplicates()
car_datasets = car_datasets.dropna(subset=['model_year', 'price'])
car_datasets['model_year'] = car_datasets['model_year'].astype(int)

car_datasets['is_4wd'] = car_datasets['is_4wd'].fillna('false')
car_datasets['is_4wd'] = car_datasets['is_4wd'].replace(1.0, 'true')
car_datasets['is_4wd'] = car_datasets['is_4wd'].map({'false': False, 'true': True})

car_datasets['cylinders'] = car_datasets['cylinders'].astype(str).fillna('unknown')
car_datasets['paint_color'] = car_datasets['paint_color'].fillna('unknown')
car_datasets['odometer'] = car_datasets['odometer'].fillna(0)

# Sort by year for easier plotting
new_car_datasets = car_datasets.sort_values(by='model_year').reset_index()
view_car_datasets = new_car_datasets[new_car_datasets['model_year'] != 1900].reset_index()

# Streamlit App 
st.header("🚗 Car Dataset Explorer")

# Show raw data checkbox
if st.checkbox("Show raw dataset"):
    st.write(view_car_datasets.head(20))

# Scatter Plot: Model Year vs Price 
st.subheader("Scatter Plot: Model Year vs Price")
fig_scatter = px.scatter(
    view_car_datasets, 
    x="model_year", 
    y="price", 
    color="cylinders",
    title="Price vs Model Year"
)
st.plotly_chart(fig_scatter)

# Histogram: Cars by Year Range
st.subheader("Histogram of Cars by Year Range")
fig = px.histogram(view_car_datasets, x="model_year", y= 'price', nbins=12, title="Histogram of Cars by Year Range")
#ax.hist(new_car_datasets["model_year"], bins=range(1900, 2021, 10), edgecolor="black")
#ax.set_xlabel("Year Range")
#ax.set_ylabel("Count of Cars")
#ax.set_title("Histogram of Cars by Year Range")
st.plotly_chart(fig)