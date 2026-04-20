import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ======================
# CONFIG
# ======================
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
# MENU SIDEBAR
# ======================
menu = st.sidebar.radio(
    "Menu",
    ["Home", "Nilai Tukar Rupiah", "Harga Minyak Mentah", "Forecast", "Evaluasi"]
)

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
    'Price': 'Harga'
})

kurs['Terakhir'] = kurs['Terakhir'].astype(str).str.replace(',', '').astype(float)
minyak['Harga'] = minyak['Harga'].astype(str).str.replace(',', '').astype(float)

kurs = kurs.sort_values("Tanggal").set_index("Tanggal")
minyak = minyak.sort_values("Tanggal").set_index("Tanggal")
forecast = forecast.sort_values("Tanggal").set_index("Tanggal")

# ======================
# MENU HOME
# ======================
if menu == "Home":

    st.title("Dashboard Peramalan Nilai Tukar Rupiah Oktober - Desember 2025")

    st.write("""
    Dashboard ini menampilkan analisis dan peramalan nilai tukar Rupiah terhadap USD 
    menggunakan model ARIMAX dengan variabel eksternal harga minyak mentah dunia.
    """)

# ======================
# NILAI TUKAR
# ======================
elif menu == "Nilai Tukar Rupiah":

    st.subheader("Grafik Nilai Tukar Rupiah")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=kurs.index,
        y=kurs['Terakhir'],
        mode='lines',
        name='Nilai Tukar',
        line=dict(width=2)
    ))

    fig.update_layout(
        title="Pergerakan Nilai Tukar Rupiah",
        xaxis_title="Tanggal",
        yaxis_title="Nilai Tukar (Rp/USD)",
        template="plotly_white",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# HARGA MINYAK
# ======================
elif menu == "Harga Minyak Mentah":

    st.subheader("Grafik Harga Minyak Mentah")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=minyak.index,
        y=minyak['Harga'],
        mode='lines',
        name='Harga Minyak',
        line=dict(width=2)
    ))

    fig.update_layout(
        title="Pergerakan Harga Minyak Mentah Dunia",
        xaxis_title="Tanggal",
        yaxis_title="Harga",
        template="plotly_white",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# FORECAST
# ======================
elif menu == "Forecast":

    st.subheader("Perbandingan Actual vs Forecast")

    fig = go.Figure()

    # Actual
    fig.add_trace(go.Scatter(
        x=forecast.index,
        y=forecast['Actual'],
        mode='lines+markers',
        name='Actual',
        line=dict(width=2)
    ))

    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast.index,
        y=forecast['Forecast_ARIMAX'],
        mode='lines',
        name='Forecast',
        line=dict(dash='dash', width=2)
    ))

    fig.update_layout(
        title="Perbandingan Nilai Aktual dan Forecast",
        xaxis_title="Tanggal",
        yaxis_title="Nilai Tukar",
        template="plotly_white",
        hovermode="x unified",
        xaxis=dict(rangeslider=dict(visible=True))  # slider bawah
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Tabel Nilai Actual")
    st.dataframe(forecast[['Actual']], use_container_width=True)

    st.subheader("Tabel Hasil Forecast")
    st.dataframe(
        forecast[['Forecast_ARIMAX']].style.format("{:.0f}"),
        use_container_width=True
    )

# ======================
# EVALUASI
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

    st.markdown("---")

    st.write("""
    **Penjelasan:**

    - RMSE menunjukkan besar rata-rata error dalam satuan asli (rupiah).
    - MAPE menunjukkan besar error dalam persen.
    Semakin kecil nilainya, semakin baik model.
    """)
