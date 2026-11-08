import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    page_icon="🚲",
    layout="wide"
)

sns.set_theme(style='darkgrid')

# 2. Fungsi Memuat dan Membersihkan Data
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    
    # Ubah tipe data tanggal
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Rename kolom agar lebih deskriptif
    df.rename(columns={
        'dteday': 'date', 
        'yr': 'year', 
        'mnth': 'month',
        'weathersit': 'weather_condition', 
        'hum': 'humidity', 
        'cnt': 'total_count'
    }, inplace=True)
    
    # Mapping nilai kategorikal
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    df['season'] = df['season'].map(season_mapping)
    
    weather_mapping = {
        1: 'Clear/Partly Cloudy', 
        2: 'Misty/Cloudy', 
        3: 'Light Snow/Rain', 
        4: 'Severe Weather'
    }
    df['weather_condition'] = df['weather_condition'].map(weather_mapping)
    
    return df

# Panggil fungsi load_data
day_df = load_data()

# 3. Sidebar Filter
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2972/2972185.png", width=120)
st.sidebar.header("Filter Data 🚲")

min_date = day_df['date'].min()
max_date = day_df['date'].max()

# Filter Rentang Tanggal
date_range = st.sidebar.date_input(
    label='Pilih Rentang Tanggal',
    min_value=min_date, 
    max_value=max_date,
    value=[min_date, max_date]
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0]

# Filter Musim
selected_season = st.sidebar.multiselect(
    label='Pilih Musim',
    options=day_df['season'].unique(),
    default=day_df['season'].unique()
)

# 4. Filter Dataset Berdasarkan Input Sidebar
filtered_df = day_df[
    (day_df['date'] >= pd.to_datetime(start_date)) & 
    (day_df['date'] <= pd.to_datetime(end_date)) &
    (day_df['season'].isin(selected_season))
]

# 5. Header & KPI Cards
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Dashboard interaktif untuk menganalisis penyewaan sepeda berdasarkan iklim, musim, dan tipe pengguna (2011–2012).")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{filtered_df['total_count'].sum():,}")
with col2:
    st.metric("Total Pengguna Kasual", value=f"{filtered_df['casual'].sum():,}")
with col3:
    st.metric("Total Pengguna Terdaftar", value=f"{filtered_df['registered'].sum():,}")

st.markdown("---")

# 6. Visualisasi 1: Pengaruh Musim dan Kondisi Cuaca
st.subheader("1. Pengaruh Musim dan Kondisi Cuaca terhadap Penyewaan Sepeda (2011–2012)")
fig1, ax1 = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

# Subplot 1: Musim
sns.barplot(
    x='season', 
    y='total_count', 
    data=filtered_df, 
    ax=ax1[0], 
    palette='viridis', 
    errorbar=None
)
ax1[0].set_title('Rata-rata Penyewaan per Musim', fontsize=14)
ax1[0].set_xlabel('Musim', fontsize=12)
ax1[0].set_ylabel('Rata-rata Penyewaan Harian', fontsize=12)
for container in ax1[0].containers:
    ax1[0].bar_label(container, fmt='%.0f', padding=3)

# Subplot 2: Kondisi Cuaca
sns.barplot(
    x='weather_condition', 
    y='total_count', 
    data=filtered_df, 
    ax=ax1[1], 
    palette='Set2', 
    errorbar=None
)
ax1[1].set_title('Rata-rata Penyewaan per Kondisi Cuaca', fontsize=14)
ax1[1].set_xlabel('Kondisi Cuaca', fontsize=12)
ax1[1].set_ylabel('Rata-rata Penyewaan Harian', fontsize=12)
for container in ax1[1].containers:
    ax1[1].bar_label(container, fmt='%.0f', padding=3)

plt.tight_layout()
st.pyplot(fig1)

# 7. Visualisasi 2: Perilaku Pengguna Kasual vs Terdaftar
st.subheader("2. Perbandingan Pola Penyewaan Pengguna Kasual vs Terdaftar pada Hari Kerja & Libur")

melted_df = pd.melt(
    filtered_df, 
    id_vars=['workingday'], 
    value_vars=['casual', 'registered'],
    var_name='user_type', 
    value_name='count'
)
melted_df['workingday'] = melted_df['workingday'].map({0: 'Akhir Pekan / Libur', 1: 'Hari Kerja'})
melted_df['user_type'] = melted_df['user_type'].map({'casual': 'Kasual (Casual)', 'registered': 'Terdaftar (Registered)'})

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='workingday', 
    y='count', 
    hue='user_type', 
    data=melted_df, 
    palette='Blues_d', 
    errorbar=None, 
    ax=ax2
)
ax2.set_title('Rata-rata Penyewaan Harian Berdasarkan Tipe Hari dan Kategori Pengguna', fontsize=14)
ax2.set_xlabel('Tipe Hari', fontsize=12)
ax2.set_ylabel('Rata-rata Penyewaan', fontsize=12)
ax2.legend(title='Tipe Pengguna')

for container in ax2.containers:
    ax2.bar_label(container, fmt='%.0f', padding=3)

plt.tight_layout()
st.pyplot(fig2)

st.caption("Copyright © 2026 - Bike Sharing Analysis Project")