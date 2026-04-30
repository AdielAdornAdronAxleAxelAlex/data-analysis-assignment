import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

all_df = pd.read_csv("processed.csv")

datetime_columns = ["date"]

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["date"].min()
max_date = all_df["date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRPYH4zPxn-h3o-eJmfDTLtZDGM8bCiOKnspg&s")
    #SUMBER  LOGO PERUSAHAAN:https://elements.envato.com/rent-bike-logo-62Q9FHS?srsltid=AfmBOoqdOr9W4ClZC9s2kw-buABj-1vRS87bvyEd_YNgShz5vQCk73on
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["date"] >= str(start_date)) & 
                (all_df["date"] <= str(end_date))]

st.header('Bike Rental Dashboard :sparkles:')
st.subheader('weather factor correlation')

weather_factor = st.selectbox(
    'Factor?',
    ('binned_temperature','binned_humidity','binned_wind_speed','binned_air_temperature','season','weather'))

binned_order=['very low','low','average','high','very high']
season_order=['spring','summer','fall','winter']
weather_order=['clear','light rain/snow','misty','heavy rain']

if weather_factor in ['binned_temperature','binned_humidity',
                      'binned_wind_speed','binned_air_temperature']:
    main_df[weather_factor]=pd.Categorical(
        main_df[weather_factor],
        categories=binned_order,
        ordered=True
    )

elif weather_factor=='season':
    main_df[weather_factor]=pd.Categorical(
        main_df[weather_factor],
        categories=season_order,
        ordered=True
    )

elif weather_factor=='weather':
    main_df[weather_factor]=pd.Categorical(
        main_df[weather_factor],
        categories=weather_order,
        ordered=True
    )

weather_df=main_df.groupby(weather_factor, sort=False)['total'].mean().reset_index().sort_values(weather_factor)
col1,col2=st.columns(2)

with col1:
    total_rentals = main_df.total.sum()
    st.metric("Total rentals", value=total_rentals)

with col2:
    average_rentals = main_df.total.mean().round(2)
    st.metric("Average rentals", value=average_rentals)

#weather factor correlation
fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(weather_df[weather_factor], weather_df['total'], color="#90CAF9")
ax.axhline(average_rentals, color='red', linestyle='--', label='rata-rata')
ax.set_title(f'Dampak {weather_factor} pada total', fontsize=20)
ax.set_xlabel(weather_factor,fontsize=20)
ax.set_ylabel(f'rata-rata total',fontsize=20)
ax.tick_params(axis='x', rotation=45,labelsize=20)
ax.tick_params(axis='y',labelsize=20)
ax.legend()
st.pyplot(fig)

#work/holiday correlation
day_factor = st.selectbox(
    'Working_day or holiday?',
    ('working_day','holiday'))

customer_type = st.selectbox(
    'Registered or casual?',
    ('registered','casual'))

day_df=main_df.groupby(day_factor)[customer_type].mean().reset_index()

col1,col2=st.columns(2)

with col1:
    total_specific_rentals = main_df[customer_type].sum()
    st.metric(label=f'Total {customer_type} rentals', value=total_specific_rentals)

with col2:
    average_specific_rentals = main_df[customer_type].mean().round(2)
    st.metric(label=f'Average {customer_type} rentals', value=average_specific_rentals)


fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(day_df[day_factor], day_df[customer_type], color="#90CAF9")
ax.axhline(average_specific_rentals, color='red', linestyle='--', label='rata-rata')
ax.set_title(f'Dampak {day_factor} pada {customer_type}', fontsize=28)
ax.set_xlabel(day_factor,fontsize=20)
ax.set_ylabel(f'rata-rata total',fontsize=20)
ax.tick_params(axis='x', rotation=45,labelsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.legend(fontsize=20)
st.pyplot(fig)


st.caption('Copyright © Rentbike 2026')