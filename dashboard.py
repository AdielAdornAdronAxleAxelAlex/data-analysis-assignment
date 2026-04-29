import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

weekday_map = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

def create_sumbyweekday_df(df):
    byday_df=df.drop(columns=['dteday'])
    byday_df=byday_df.groupby(['weekday']).sum()
    return byday_df

all_df = pd.read_csv("data/day.csv")

datetime_columns = ["dteday"]

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

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

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# # Menyiapkan berbagai dataframe
sum_by_weekday_df = create_sumbyweekday_df(main_df)

# plot number of daily orders (2021)
st.header('Bike Rental Dashboard :sparkles:')
st.subheader('Daily rentals')

col1, col2, col3=st.columns(3)

with col1:
    total_rentals = main_df.cnt.sum()
    st.metric("Total rentals", value=total_rentals)

with col2:
    total_casual_customers= main_df.casual.sum()
    st.metric("Total casual customers", value=total_casual_customers)

with col3:
    total_registered_customers= main_df.registered.sum()
    st.metric("Total registered customers", value=total_registered_customers)

col4, col5, col6= st.columns(3)

with col4:
    average_rentals = main_df.cnt.mean().round(2)
    st.metric("Average total rentals", value=average_rentals)

with col5:
    average_casual_customers= main_df.casual.mean().round(2)
    st.metric("Average casual customers", value=average_casual_customers)

with col6:
    average_registered_customers= main_df.registered.mean().round(2)
    st.metric("Average registered customers", value=average_registered_customers)

#daily performance
fig, ax = plt.subplots(figsize=(16, 8))
ax.set_title("Number of daily rentals", loc="center", fontsize=30)
ax.plot(
    main_df["dteday"],
    main_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16, 8))
ax.set_title("Number of daily casual rentals", loc="center", fontsize=30)
ax.plot(
    main_df["dteday"],
    main_df["casual"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16, 8))
ax.set_title("Number of daily registered rentals", loc="center", fontsize=30)
ax.plot(
    main_df["dteday"],
    main_df["registered"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# weekday performance  
sum_by_weekday_df = sum_by_weekday_df.reset_index()
sum_by_weekday_df["weekday_name"] = sum_by_weekday_df["weekday"].map(weekday_map)

max_idx=sum_by_weekday_df["cnt"].idxmax()

st.subheader("Rentals per weekday")

fig, ax = plt.subplots(figsize=(20, 10))

colors=["#D3D3D3"]*len(sum_by_weekday_df)
colors[list(sum_by_weekday_df.index).index(max_idx)]="#90CAF9"

sns.barplot(
    x="cnt", 
    y="weekday_name",
    orient='h',
    data=sum_by_weekday_df,
    palette=colors,
    ax=ax
)

ax.set_title("Number of total rentals per weekday", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(20, 10))

colors=["#D3D3D3"]*len(sum_by_weekday_df)
colors[list(sum_by_weekday_df.index).index(max_idx)]="#90CAF9"

sns.barplot(
    x="casual", 
    y="weekday_name",
    orient='h',
    data=sum_by_weekday_df,
    palette=colors,
    ax=ax
)

ax.set_title("Number of casual rentals per weekday", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(20, 10))

colors=["#D3D3D3"]*len(sum_by_weekday_df)
colors[list(sum_by_weekday_df.index).index(max_idx)]="#90CAF9"

sns.barplot(
    x="registered", 
    y="weekday_name",
    orient='h',
    data=sum_by_weekday_df,
    palette=colors,
    ax=ax
)

ax.set_title("Number of registered rentals per weekday", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)


st.caption('Copyright © Rentbike 2026')
