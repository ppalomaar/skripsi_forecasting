import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Dashboard Forecast Nilai Tukar Oktober - Desember 2025",
    layout="wide"
)

# ======================
# STYLE SIDEBAR
# ======================
st.markdown("""
<style>
section[data-testid="stSidebar"] * {
    font-size: 18px !important;
}
.sidebar-title {
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    '<p class="sidebar-title">Nilai Tukar USD ke Rupiah</p>',
    unsafe_allow_html=True
)

# ======================
# MENU SIDEBAR BUTTON
# ======================
if "menu" not in st.session_state:
    st.session_state.menu = "Home"

if st.sidebar.button("Home"):
    st.session_state.menu = "Home"

if st.sidebar.button("Nilai Tukar Rupiah"):
    st.session_state.menu = "Nilai Tukar Rupiah"

if st.sidebar.button("Harga Minyak Mentah"):
    st.session_state.menu = "Harga Minyak Mentah"

if st.sidebar.button("Forecast"):
    st.session_state.menu = "Forecast"

if st.sidebar.button("Evaluasi"):
    st.session_state.menu = "Evaluasi"

menu = st.session_state.menu

# ======================
# LOAD DATA
# ======================
kurs = pd.read_csv("kurs.csv")
minyak = pd.read_csv("minyak.csv")
forecast = pd.read_csv("hasil_forecast_arimax_finall.csv")

# ======================
# PREPROCESSING
# ======================
kurs['Tanggal'] = pd.to_datetime(kurs['Tanggal'])
minyak['Date'] = pd.to_datetime(minyak['Date'])
forecast['Tanggal'] = pd.to_datetime(forecast['Tanggal'])

minyak = minyak.rename(columns={
    'Date': 'Tanggal',
    'Price': 'Harga',
    'Open': 'Buka',
    'High': 'Tertinggi',
    'Low': 'Terendah',
    'Vol.': 'Volume',
    'Change %': 'Perubahan (%)'
})

kurs['Terakhir'] = kurs['Terakhir'].astype(str).str.replace(',', '').astype(float)
minyak['Harga'] = minyak['Harga'].astype(str).str.replace(',', '').astype(float)

kurs = kurs.sort_values("Tanggal")
minyak = minyak.sort_values("Tanggal")
forecast = forecast.sort_values("Tanggal")

kurs = kurs.set_index("Tanggal")
minyak = minyak.set_index("Tanggal")
forecast = forecast.set_index("Tanggal")

# ======================
# MENU HOME (LANDING PAGE)
# ======================
if menu == "Home":

    st.title("Dashboard Peramalan Nilai Tukar Rupiah Oktober - Desember 2025")

    st.markdown("""
### 📌 Gambaran Umum
Platform ini menyediakan layanan analisis dan proyeksi nilai tukar Rupiah terhadap Dollar Amerika Serikat sebagai bagian dari dukungan pengambilan keputusan berbasis data. 
Pergerakan nilai tukar memiliki dampak langsung terhadap aktivitas perdagangan, investasi, serta stabilitas ekonomi, sehingga diperlukan alat analisis yang mampu memberikan estimasi yang akurat dan terukur.

### 🎯 Tujuan Layanan
Dashboard ini dirancang untuk memberikan insight prediktif terkait pergerakan nilai tukar Rupiah pada Bulan September hingga Desember 2025 
guna mendukung pelaku usaha dan pemangku kebijakan dalam melakukan perencanaan, mitigasi risiko, serta penyusunan strategi ekonomi.

### ⚙️ Pendekatan Analitis
Peramalan dilakukan menggunakan model **ARIMAX (AutoRegressive Integrated Moving Average with Exogenous Variable)** yang mengintegrasikan data historis nilai tukar dengan variabel eksternal berupa harga minyak mentah dunia, 
sebagai salah satu indikator global yang mempengaruhi dinamika ekonomi.

### 📊 Cakupan Data
Analisis didasarkan pada:
- Data historis nilai tukar Rupiah terhadap USD  
- Data harga minyak mentah dunia sebagai variabel eksternal  

### 📈 Fitur Layanan
- Visualisasi pergerakan nilai tukar Rupiah terhadap USD selama periode Januari hingga Desember 2025  
- Visualisasi tren harga minyak mentah dunia pada periode yang sama sebagai indikator eksternal  
- Proyeksi nilai tukar Rupiah dalam horizon mingguan (7 hari)  
- Perbandingan antara nilai aktual dan hasil proyeksi untuk memantau kinerja model  

### 💡 Nilai Tambah
Informasi yang dihasilkan dapat dimanfaatkan sebagai dasar pertimbangan dalam pengambilan keputusan strategis, baik dalam konteks bisnis maupun kebijakan publik. Pendekatan berbasis data ini diharapkan mampu memberikan gambaran yang lebih objektif terhadap potensi pergerakan nilai tukar di masa depan.
""")

# ======================
# MENU NILAI TUKAR
# ======================
elif menu == "Nilai Tukar Rupiah":

    st.subheader("Grafik Nilai Tukar Rupiah")

    fig, ax = plt.subplots(figsize=(14,6))
    ax.plot(kurs.index, kurs['Terakhir'], linewidth=2, label="Nilai Tukar Rupiah")

    ax.set_title("Pergerakan Nilai Tukar Rupiah")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Nilai Tukar (Rp/USD)")

    ax.grid(True, linestyle="--", alpha=0.3)
    plt.xticks(rotation=45)

    ax.legend()
    st.pyplot(fig)

# ======================
# MENU MINYAK
# ======================
elif menu == "Harga Minyak Mentah":

    st.subheader("Grafik Harga Minyak Mentah")

    fig, ax = plt.subplots(figsize=(14,6))
    ax.plot(minyak.index, minyak['Harga'], linewidth=2, label="Harga Minyak Mentah")

    ax.set_title("Pergerakan Harga Minyak Mentah Dunia")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Harga")

    ax.grid(True, linestyle="--", alpha=0.3)
    plt.xticks(rotation=45)

    ax.legend()
    st.pyplot(fig)

# ======================
# MENU FORECAST
# ======================
elif menu == "Forecast":

    st.subheader("Grafik Forecast Per Minggu")

    fig, ax = plt.subplots(figsize=(14,6))
    ax.plot(forecast.index, forecast['Forecast_ARIMAX'], linewidth=2, marker='o', label="Forecast")

    ax.set_title("Forecast Nilai Tukar Per Minggu")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Nilai Tukar")

    ax.grid(True, linestyle="--", alpha=0.3)
    plt.xticks(rotation=45)

    ax.legend()
    st.pyplot(fig)

    st.subheader("Grafik Keseluruhan Actual vs Forecast")

    fig2, ax2 = plt.subplots(figsize=(14,6))
    ax2.plot(forecast.index, forecast['Actual'], linewidth=2, label="Actual")
    ax2.plot(forecast.index, forecast['Forecast_ARIMAX'], linewidth=2, linestyle='--', label="Forecast")

    ax2.set_title("Perbandingan Actual vs Forecast")
    ax2.set_xlabel("Tanggal")
    ax2.set_ylabel("Nilai Tukar")

    ax2.grid(True, linestyle="--", alpha=0.3)
    plt.xticks(rotation=45)

    ax2.legend()
    st.pyplot(fig2)

    st.subheader("Tabel Nilai Real (Actual)")
    st.dataframe(forecast[['Actual']], use_container_width=True)

    st.subheader("Tabel Hasil Forecast")
    st.dataframe(forecast[['Forecast_ARIMAX']].style.format("{:.0f}"), use_container_width=True)

# ======================
# MENU EVALUASI
# ======================
elif menu == "Evaluasi":

    st.subheader("Evaluasi Model")

    rmse = ((forecast['Actual'] - forecast['Forecast_ARIMAX'])**2).mean()**0.5
    mape = (abs((forecast['Actual'] - forecast['Forecast_ARIMAX']) / forecast['Actual']).mean()) * 100

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="RMSE", value=f"{rmse:.2f}")

    with col2:
        st.metric(label="MAPE", value=f"{mape:.2f}%")