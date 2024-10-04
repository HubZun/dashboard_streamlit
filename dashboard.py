import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
day_df = pd.read_csv("../data/day.csv")
hour_df = pd.read_csv("../data/hour.csv")

# Set page title
st.title("Dashboard Analisis Data Penyewaan Sepeda")

# Sidebar for user input
st.sidebar.header("Pengaturan Filter")
view_option = st.sidebar.selectbox("Pilih Data yang Ingin Ditampilkan", ("Data Harian", "Data Per Jam"))
season_option = st.sidebar.multiselect("Pilih Musim", day_df["season"].unique(), default=day_df["season"].unique())
workingday_option = st.sidebar.radio("Hanya Hari Kerja?", (True, False))

# Filter dataset berdasarkan input
if view_option == "Data Harian":
    filtered_df = day_df[day_df["season"].isin(season_option)]
    if workingday_option:
        filtered_df = filtered_df[filtered_df["workingday"] == 1]
else:
    filtered_df = hour_df[hour_df["season"].isin(season_option)]
    if workingday_option:
        filtered_df = filtered_df[filtered_df["workingday"] == 1]

# Add date range filter
if view_option == "Data Harian":
    start_date = st.sidebar.date_input("Mulai Tanggal", pd.to_datetime(day_df["dteday"]).min())
    end_date = st.sidebar.date_input("Akhir Tanggal", pd.to_datetime(day_df["dteday"]).max())
    filtered_df = filtered_df[(pd.to_datetime(filtered_df["dteday"]) >= pd.to_datetime(start_date)) & 
                              (pd.to_datetime(filtered_df["dteday"]) <= pd.to_datetime(end_date))]
    
# Add histogram of rentals
st.subheader(f"Distribusi Penyewaan {view_option}")
fig, ax = plt.subplots()
ax.hist(filtered_df["cnt"], bins=20, color='skyblue')
ax.set_xlabel("Jumlah Penyewaan")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)




# Display data
st.header(f"Data {view_option}")
st.write(filtered_df.head())

# Display statistics
st.subheader("Statistik Deskriptif")
st.write(filtered_df.describe())

# Display plot
st.subheader(f"Grafik Penyewaan {view_option}")
if view_option == "Data Harian":
    fig, ax = plt.subplots()
    ax.plot(filtered_df["dteday"], filtered_df["cnt"], label="Total Penyewaan")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.legend()
    st.pyplot(fig)
else:
    fig, ax = plt.subplots()
    ax.plot(filtered_df["hr"], filtered_df["cnt"], label="Total Penyewaan", alpha=0.7)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.legend()
    st.pyplot(fig)

# Footer
st.write("Dashboard ini menggunakan dataset penyewaan sepeda.")