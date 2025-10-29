import streamlit as st
import pandas as pd

from utils.data_cleaning import load_and_clean_data
from utils.data_analysis import prepare_analysis_data
from utils.data_viz import plot_price_trend, plot_candlestick, plot_volatility, plot_volume_correlation

st.set_page_config(
    page_title="Bitcoin Dashboard",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def get_data():
    df = load_and_clean_data("data/btcusd_1-min_data.csv")
    df = prepare_analysis_data(df)
    return df

df = get_data()


st.title("🪙 Bitcoin Historical Data Dashboard")
st.markdown("""
Bitcoin merupakan salah satu mata uang kripto paling populer sekaligus pelopor dalam dunia aset digital.  
Sejak dirilis pada tahun 2009, nilai Bitcoin telah mengalami perjalanan yang dinamis, dari harga awal yang nyaris tak bernilai, hingga mencapai puluhan ribu dolar per koin.
""")


latest_row = df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tanggal Terakhir", latest_row["Timestamp"].strftime("%Y-%m-%d"))
col2.metric("Harga Penutupan (USD)", f"{latest_row['Close']:.2f}")
col3.metric("Volatilitas (%)", f"{latest_row['Volatility(%)']:.2f}")
col4.metric("Volume Perdagangan (BTC)", f"{latest_row['Volume']:.0f}")

st.markdown("---")

st.title("Tren Harga Bitcoin")
st.markdown("""
Bagian ini menampilkan pergerakan harga Bitcoin secara umum.  
Tujuannya adalah untuk melihat **pola tren jangka panjang** dan **momen perubahan signifikan** dalam pasar.

Perhatikan bagaimana harga Bitcoin bergerak naik-turun dalam siklus yang berulang.  
Lonjakan harga sering kali diikuti dengan periode koreksi yang cukup tajam.
""")

st.plotly_chart(plot_price_trend(df), use_container_width=True)

st.markdown("---")
st.subheader("Candlestick Chart (Detailed OHLC)")
st.markdown("""
Grafik candlestick memperlihatkan **harga pembukaan, penutupan, tertinggi, dan terendah** untuk setiap periode waktu.  
Visualisasi ini membantu kita memahami **fluktuasi harga dalam jangka pendek** serta mendeteksi pola pasar bullish (naik) atau bearish (turun).

Candlestick panjang menandakan pasar sangat aktif, sedangkan candlestick pendek menunjukkan stabilitas sementara.
""")
st.plotly_chart(plot_candlestick(df), use_container_width=True)


st.title("Analisis Volatilitas ")
st.markdown("""
Volatilitas menunjukkan tingkat **ketidakpastian atau risiko pergerakan harga**.  
Nilai volatilitas tinggi berarti harga Bitcoin berubah cepat dalam waktu singkat,  
sedangkan volatilitas rendah mengindikasikan kondisi pasar yang relatif stabil.

Biasanya, volatilitas meningkat saat terjadi pergerakan besar — baik saat harga melonjak maupun jatuh drastis.
""")

st.plotly_chart(plot_volatility(df), use_container_width=True)

st.markdown("---")
st.subheader("Statistik")

col1, col2, col3 = st.columns(3)
col1.metric("Rata-rata Volatilitas (%)", f"{df['Volatility(%)'].mean():.2f}")
col2.metric("Maks. Volatilitas (%)", f"{df['Volatility(%)'].max():.2f}")
col3.metric("Min. Volatilitas (%)", f"{df['Volatility(%)'].min():.2f}")


st.title("Korelasi Volume vs Harga / Return")
st.markdown("""
Di bagian ini, kita ingin melihat hubungan antara **aktivitas perdagangan (volume)** dan **pergerakan harga**.  
Apakah lonjakan volume biasanya diikuti dengan perubahan harga yang signifikan?

Hubungan positif menandakan bahwa ketika volume meningkat, harga cenderung ikut naik. 
Sementara hubungan lemah bisa menandakan fase akumulasi atau distribusi di pasar.
""")


mode = st.radio("Pilih Mode Korelasi:", ["Close Price", "Daily Return (%)"])
mode_key = "Return" if "Return" in mode else "Close"

fig = plot_volume_correlation(df, mode=mode_key)
st.plotly_chart(fig, use_container_width=True)
