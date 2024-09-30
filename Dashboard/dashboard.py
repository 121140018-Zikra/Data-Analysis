import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

day_df = pd.read_csv('Data/day.csv')
hour_df = pd.read_csv('Data/hour.csv')

season_map = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}

season_options = list(season_map.values()) + ['Semua Musim']
day_df['season'] = day_df['season'].map(season_map)

weather_mapping = {1: 'Cerah', 2: 'Berawan', 3: 'Hujan Ringan', 4: 'Badai'}
day_df['weathersit'] = day_df['weathersit'].replace(weather_mapping)

st.title('Bike-Sharing Data Analysis Dashboard')

if st.checkbox('Show Raw Data'):
    st.subheader('day.csv')
    st.write(day_df)
    st.subheader('hour.csv')
    st.write(hour_df)

selected_season = st.sidebar.selectbox("Pilih Musim", options=season_options)

if selected_season == 'Semua Musim':
    filtered_day_df = day_df
else:
    filtered_day_df = day_df[day_df['season'] == selected_season]

st.subheader('Jumlah Rental Berdasarkan Musim')
fig, ax = plt.subplots()
sns.boxplot(data=filtered_day_df, x='season', y='cnt', ax=ax)
ax.set_title('Boxplot Rental Sepeda Berdasarkan Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Total Rental')
st.pyplot(fig)

st.subheader('Jumlah Rental Berdasarkan Cuaca')
fig, ax = plt.subplots()
sns.boxplot(data=filtered_day_df, x='weathersit', y='cnt', ax=ax)
ax.set_title('Boxplot Rental Sepeda Berdasarkan Cuaca')
ax.set_xlabel('Cuaca')
ax.set_ylabel('Total Rental')
st.pyplot(fig)

st.subheader('Heatmap Korelasi yang Memengaruhi Jumlah Rental')
fig, ax = plt.subplots()
corr_matrix = filtered_day_df[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

st.subheader('Rental Sepeda Berdasarkan Jam')
fig, ax = plt.subplots()
sns.lineplot(data=hour_df, x='hr', y='cnt', ax=ax)
ax.set_title('Lineplot Jumlah Rental Sepeda Berdasarkan Jam')
ax.set_xlabel('Jam')
ax.set_ylabel('Total Rental')
st.pyplot(fig)

st.markdown(""" 
## Conclusion:
1. Musim, cuaca, dan temperatur memiliki pengaruh kuat terhadap jumlah pengguna rental sepeda. Pada musim gugur dan cuaca cerah memiliki jumlah pengguna yang lebih banyak. Sebaliknya pada musim dingin dan cuaca ekstrim jumlah pengguna turun drastis.
2. Berdasarkan waktu penggunaan, terdapat lonjakan signifikan pada jam-jam sibuk, yakni pagi hari sekitar pukul 08:00 dan sore hari antara pukul 17:00 hingga 18:00. Hal ini mengindikasikan bahwa bike-sharing banyak digunakan sebagai sarana transportasi saat berangkat dan pulang kerja.
""")
