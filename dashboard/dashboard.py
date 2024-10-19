import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

# Load the data
def load_data():
    main_df = pd.read_csv('./main_data.csv')
    monthly_avg_gdf = gpd.read_file('./main_data.shp')
    return main_df, monthly_avg_gdf
main_df, monthly_avg_gdf = load_data()

# Sidebar for user inputs
st.sidebar.title('Air Quality Dashboard')
districts = monthly_avg_gdf['district'].unique()
selected_districts = st.sidebar.multiselect('Select Districts', options=districts, default=districts)
date_range = st.sidebar.date_input("Select Date Range", [pd.to_datetime('2014-01-01'), pd.to_datetime('2016-12-01')])

# Correlation Heatmap
st.title("Correlation Heatmap Between Parameters")
corr_matrix = main_df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, linewidths=0.5, vmin=-1, vmax=1, ax=ax)
st.pyplot(fig)

# Line plots for Pollution Index, Temperature, etc.
st.title("Time-Series Plots")
features = {'PI': 'Pollution Index', 'TEMP': 'Temperature', 'PRES': 'Pressure', 'WSPM': 'Wind Speed', 'RAIN': 'Precipitation'}
selected_feature = st.selectbox("Select Feature to Plot", list(features.keys()), format_func=lambda x: features[x])
monthly_avg_filtered = monthly_avg_gdf[monthly_avg_gdf['district'].isin(selected_districts)]
monthly_avg_filtered = monthly_avg_filtered[(monthly_avg_filtered['datetime'] >= pd.to_datetime(date_range[0])) & (monthly_avg_filtered['datetime'] <= pd.to_datetime(date_range[1]))]
fig = px.line(monthly_avg_filtered, x='datetime', y=selected_feature, color='district', title=f"Time-Series of {features[selected_feature]}")
st.plotly_chart(fig)

# Geographical Heatmap with customization options
st.title("Geographical Heatmap")
month = st.selectbox("Select Month", pd.to_datetime(monthly_avg_gdf['datetime'].unique()).strftime('%Y-%m'))
vmin, vmax = st.slider('Set Color Scale Range for Pollution Index', 0, 50, (2, 10), step=1)
monthly_avg_selected = monthly_avg_gdf[pd.to_datetime(monthly_avg_gdf['datetime']).dt.strftime('%Y-%m') == month]
fig, ax = plt.subplots(figsize=(10, 8))
monthly_avg_selected.plot(column='PI', cmap='magma_r', linewidth=0.8, edgecolor='0.8', ax=ax, legend=True, vmin=vmin, vmax=vmax)
ax.set_title(f"Pollution Index in {month}")
ax.axis('off')
st.pyplot(fig)

# Footer
st.write("Data visualization for Beijing Air Quality Monitoring Stations.")