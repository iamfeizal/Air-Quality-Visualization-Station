# import library yang akan digunakan
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
from helper_func import MeanProcessing, MonthlyProcessing, WanliuProcessing
sns.set(style='dark')

# air quality dataset
air_quality_df = pd.read_csv("data/air_quality_df.csv")
air_quality_df.sort_values(by="datetime", inplace=True)
air_quality_df.reset_index(inplace=True)
air_quality_df['datetime'] = pd.to_datetime(air_quality_df['datetime'])

# wanliu station dataset
wanliu_timeseries_df = pd.read_csv("data/wanliu_timeseries_df.csv")
wanliu_timeseries_df.sort_values(by="datetime", inplace=True)
wanliu_timeseries_df.reset_index(inplace=True)
wanliu_timeseries_df['datetime'] = pd.to_datetime(wanliu_timeseries_df['datetime'])

# set min dan max datetime
min_date = air_quality_df["datetime"].min()
max_date = air_quality_df["datetime"].max()
 
# sidebar
with st.sidebar:
    st.title("Air Quality Dashboard")
    st.divider()
    st.image("asset/logo.png")
    st.divider()
    # Mengambil start_date & end_date dari input
    start_date, end_date = st.date_input(
        label='Date Range',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    st.divider()
    st.text("by Imam Agus Faisal")
    st.caption('Copyright (C) Imam Agus Faisal 2023')
air_quality_df = air_quality_df[(air_quality_df["datetime"] >= str(start_date)) & (air_quality_df["datetime"] <= str(end_date))]
wanliu_timeseries_range_df = wanliu_timeseries_df[(wanliu_timeseries_df["datetime"] >= str(start_date)) & (wanliu_timeseries_df["datetime"] <= str(end_date))]

# memproses data dengan fungsi
sorted_mean_CO_df = MeanProcessing(air_quality_df).create_sorted_CO_mean_values_df()
sorted_mean_PM10_df = MeanProcessing(air_quality_df).create_sorted_PM10_mean_values_df()
wanliu_monthly_df = MonthlyProcessing(wanliu_timeseries_df).create_monthly_mean_df()
wanliu_df = WanliuProcessing(wanliu_timeseries_range_df).create_wanliu_df()

# header dashboard
st.header('Visualization of Air Quality at The Station :leaves:')

# Bar Chart Rata-Rata Karbon Monoksida (CO) Tertinggi dan Terendah pada Stasiun
st.divider()
st.subheader("Highest and Lowest Average Carbon Monoxide (CO) at the Station")
col1, col2 = st.columns(2)
with col1:
    max_station = sorted_mean_CO_df.iat[0, 0]
    st.metric("Highest", value=max_station, help="Station with the highest CO levels")
with col2:
    min_station = sorted_mean_CO_df.iat[11, 0]
    st.metric("Lowest", value=min_station, help="Station with the lowest CO levels")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(60, 30))
colors1 = ["r", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
colors2 = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "g"]
sns.barplot(x="CO mean", y="station", data=sorted_mean_CO_df.head(6), palette=colors1, ax=ax[0])
ax[0].set_ylabel("Station", fontsize=30)
ax[0].set_xlabel("Average Carbon Monoxide (CO)", fontsize=30)
ax[0].set_title("Highest Average Carbon Monoxide (CO)", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=30)
ax[0].tick_params(axis ='x', labelsize=30)
sns.barplot(x="CO mean", y="station", data=sorted_mean_CO_df.tail(6), palette=colors2, ax=ax[1])
ax[1].set_ylabel("Station", fontsize=30)
ax[1].set_xlabel("Average Carbon Monoxide (CO)", fontsize=30)
ax[1].set_title("Lowest Average Carbon Monoxide (CO)", fontsize=50)
ax[1].tick_params(axis ='y', labelsize=30)
ax[1].tick_params(axis ='x', labelsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
st.pyplot(fig)

# Bar Chart Urutan Rata-Rata PM10 Perstasiun (Rendah ke Tinggi)
st.divider()
st.subheader("Order of Average PM10 Per Station (Low to High)")
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7, 7))
colors = ["#068DA9"]
sns.barplot(x="PM10 mean", y="station", data=sorted_mean_PM10_df, palette=colors)
ax.set_ylabel("Station", fontsize=13)
ax.set_xlabel("Average PM10", fontsize=13)
ax.set_title("Order of Average PM10 Per Station (Low to High)", fontsize=15)
ax.tick_params(axis ='y', labelsize=11)
ax.tick_params(axis ='x', labelsize=11)
st.pyplot(fig)

# Line Chart Rata-Rata Bulanan PM 2.5 pada Stasiun Wanliu (12 Bulan Terakhir)
st.divider()
st.subheader("Average Monthly PM 2.5 at Wanliu Station (Last 12 Months)")
last_1_year = wanliu_monthly_df.tail(12)
sorted_last_1_year = last_1_year.sort_values(by="PM2.5")
col1, col2 = st.columns(2)
with col1:
    max_PM2 = round(sorted_last_1_year['PM2.5'].tail(1), 3)
    mon_max_PM2 = sorted_last_1_year.iat[11, 0]
    st.metric("Highest", value=max_PM2, help="Highest level of PM 2.5 at Wanliu Station (last 12 months)")
    st.metric("At", value=mon_max_PM2, help="The month when PM 2.5 levels are highest")
with col2:
    min_PM2 = round(sorted_last_1_year['PM2.5'].head(1), 3)
    mon_max_PM2 = sorted_last_1_year.iat[0, 0]
    st.metric("Lowest", value=min_PM2, help="Lowest level of PM 2.5 at Wanliu Station (last 12 months)")
    st.metric("At", value=mon_max_PM2, help="The month when PM 2.5 levels are lowest")
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    last_1_year["datetime"],
    last_1_year["PM2.5"],
    marker='o', 
    linewidth=2,
    color="r"
)
ax.set_title('Average Monthly PM 2.5 at Wanliu Station (Last 12 Months)')
ax.set_xlabel('Date')
ax.set_ylabel('PM 2.5 level')
ax.tick_params(axis ='y', labelsize=11)
ax.tick_params(axis ='x', labelsize=11, rotation=45)
ax.grid(True, linestyle='--', linewidth=0.5, which='both', color='gray')
st.pyplot(fig)
with st.expander("See Explanation"):
        st.write('Based on the results of Data Visualization using a Line Chart, it can be concluded that the data for the last 12 months tends to fluctuate. A significant increase in PM 2.5 levels occurred in the period October 2016 - January 2017 and peaked in January 2017. However, PM 2.5 levels again decreased sharply in March 2017.')

# Bar Chart Detail Air Quality pada Stasiun Wanliu
st.divider()
st.subheader("Details of Air Quality at Wanliu Station")
tab1, tab2, tab3 = st.tabs(["PM 2.5", "PM 10", "CO"])
with tab1:
    sorted_wanliu_PM2_df = wanliu_df.sort_values(by="PM2.5")
    sorted_wanliu_PM2_df.index = sorted_wanliu_PM2_df.index.strftime('%d %B %Y')
    sorted_wanliu_PM2_df = sorted_wanliu_PM2_df.reset_index()
    length = len(sorted_wanliu_PM2_df) - 1
    max_PM2 = round(sorted_wanliu_PM2_df.iat[length, 1], 3)
    delta_max = round(sorted_wanliu_PM2_df.iat[length, 1]-sorted_wanliu_PM2_df.iat[(length-1), 1], 3)
    min_PM2 = round(sorted_wanliu_PM2_df.iat[0, 1], 3)
    delta_min = round(sorted_wanliu_PM2_df.iat[0, 1]-sorted_wanliu_PM2_df.iat[1, 1], 3)
    col1, col2 = st.columns(2)
    with col1:
        mon_max_PM2 = sorted_wanliu_PM2_df.iat[length, 0]
        st.metric("Highest PM 2.5 levels", value=f"{max_PM2} µg/m³", delta=delta_max, delta_color="inverse", help="Highest levels of PM 2.5 at Wanliu Station")
        st.metric("At", value=mon_max_PM2, help="The month when PM 2.5 levels are highest")
    with col2:
        mon_min_PM2 = sorted_wanliu_PM2_df.iat[0, 0]
        st.metric("Lowest PM 2.5 levels", value=f"{min_PM2} µg/m³", delta=delta_min, delta_color="inverse", help="Lowest levels of PM 2.5 at Wanliu Station")
        st.metric("At", value=mon_min_PM2, help="The month when PM 2.5 levels are lowest")
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        wanliu_df.index,
        wanliu_df["PM2.5"],
        marker='o', 
        linewidth=2,
        color="r"
    )
    ax.set_title('Daily Average PM 2.5 at Wanliu Station')
    ax.set_xlabel('Date')
    ax.set_ylabel('PM 2.5 level')
    ax.tick_params(axis ='y', labelsize=11)
    ax.tick_params(axis ='x', labelsize=11, rotation=45)
    ax.grid(True, linestyle='--', linewidth=0.5, which='both', color='gray')
    st.pyplot(fig)
with tab2:
    sorted_wanliu_PM10_df = wanliu_df.sort_values(by="PM10")
    sorted_wanliu_PM10_df.index = sorted_wanliu_PM10_df.index.strftime('%d %B %Y')
    sorted_wanliu_PM10_df = sorted_wanliu_PM10_df.reset_index()
    length = len(sorted_wanliu_PM10_df) - 1
    print(sorted_wanliu_PM10_df.info())
    max_PM10 = round(sorted_wanliu_PM10_df.iat[length, 2], 3)
    delta_max = round(sorted_wanliu_PM10_df.iat[length, 2]-sorted_wanliu_PM10_df.iat[(length-1), 2], 3)
    min_PM10 = round(sorted_wanliu_PM10_df.iat[0, 2], 3)
    delta_min = round(sorted_wanliu_PM10_df.iat[0, 2]-sorted_wanliu_PM10_df.iat[1, 2], 3)
    col1, col2 = st.columns(2)
    with col1:
        mon_max_PM10 = sorted_wanliu_PM10_df.iat[length, 0]
        st.metric("Highest PM 10 levels", value=f"{max_PM10} µg/m³", delta=delta_max, delta_color="inverse", help="Highest levels of PM 10 at Wanliu Station")
        st.metric("At", value=mon_max_PM10, help="The month when PM 10 levels are highest")
    with col2:
        mon_min_PM10 = sorted_wanliu_PM10_df.iat[0, 0]
        st.metric("Lowest PM 10 levels", value=f"{min_PM10} µg/m³", delta=delta_min, delta_color="inverse", help="Lowest levels of PM 10 at Wanliu Station")
        st.metric("At", value=mon_min_PM10, help="The month when PM 10 levels are lowest")
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        wanliu_df.index,
        wanliu_df["PM10"],
        marker='o', 
        linewidth=2,
        color="r"
    )
    ax.set_title('Daily Average PM 10 at Wanliu Station')
    ax.set_xlabel('Date')
    ax.set_ylabel('PM 10 level')
    ax.tick_params(axis ='y', labelsize=11)
    ax.tick_params(axis ='x', labelsize=11, rotation=45)
    ax.grid(True, linestyle='--', linewidth=0.5, which='both', color='gray')
    st.pyplot(fig)
with tab3:
    sorted_wanliu_CO_df = wanliu_df.sort_values(by="CO")
    sorted_wanliu_CO_df.index = sorted_wanliu_CO_df.index.strftime('%d %B %Y')
    sorted_wanliu_CO_df = sorted_wanliu_CO_df.reset_index()
    length = len(sorted_wanliu_CO_df) - 1
    print(sorted_wanliu_CO_df.info())
    max_CO = round(sorted_wanliu_CO_df.iat[length, 3], 3)
    delta_max = round(sorted_wanliu_CO_df.iat[length, 3]-sorted_wanliu_CO_df.iat[(length-1), 3], 3)
    min_CO = round(sorted_wanliu_CO_df.iat[0, 3], 3)
    delta_min = round(sorted_wanliu_CO_df.iat[0, 3]-sorted_wanliu_CO_df.iat[1, 3], 3)
    col1, col2 = st.columns(2)
    with col1:
        mon_max_CO = sorted_wanliu_CO_df.iat[length, 0]
        st.metric("Highest CO Levels", value=f"{max_CO} ppm", delta=delta_max, delta_color="inverse", help="Highest CO levels at Wanliu Station")
        st.metric("At", value=mon_max_CO, help="The month when CO levels are highest")
    with col2:
        mon_min_CO = sorted_wanliu_CO_df.iat[0, 0]
        st.metric("Lowest CO Levels", value=f"{min_CO} ppm", delta=delta_min, delta_color="inverse", help="Lowest CO levels at Wanliu Station")
        st.metric("At", value=mon_min_CO, help="The month when CO levels are lowest")
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        wanliu_df.index,
        wanliu_df["CO"],
        marker='o', 
        linewidth=2,
        color="r"
    )
    ax.set_title('Average Daily CO at Wanliu Station')
    ax.set_xlabel('Date')
    ax.set_ylabel('CO Level')
    ax.tick_params(axis ='y', labelsize=11)
    ax.tick_params(axis ='x', labelsize=11, rotation=45)
    ax.grid(True, linestyle='--', linewidth=0.5, which='both', color='gray')
    st.pyplot(fig)