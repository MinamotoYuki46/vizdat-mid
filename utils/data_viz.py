import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_price_trend(df: pd.DataFrame) -> go.Figure:

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Timestamp"], y=df["Close"],
        mode="lines", name="Close Price",
        line=dict(color="#1f77b4", width=2)
    ))

    for col in [c for c in df.columns if c.startswith("MA_")]:
        fig.add_trace(go.Scatter(
            x=df["Timestamp"], y=df[col],
            mode="lines", name=col,
            line=dict(width=1.5, dash="dot")
        ))

    fig.update_layout(
        title="Harga Bitcoin dan Rata-Rata Pergerakan (Moving Average)",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white",
        hovermode="x unified",
        legend_title="Legend"
    )
    return fig



def plot_volatility(df: pd.DataFrame):

    fig = px.area(
        df, x="Timestamp", y="Volatility(%)",
        title="Volatility Harian(%)",
        labels={"Volatility(%)": "Volatility (%)"},
        template="plotly_white"
    )

    fig.update_traces(line=dict(color="#ff7f0e"))
    return fig


def plot_volume_correlation(df: pd.DataFrame, mode="Close"):
    if mode == "Return":
        y_col = "Daily_Return(%)"
        title = "Volume vs Daily Return (%)"
    else:
        y_col = "Close"
        title = "Volume vs Closing Price"

    fig = px.scatter(
        df, x="Volume", y=y_col,
        color="Volatility(%)",
        title=title,
        labels={
            "Volume_(BTC)": "Trading Volume (BTC)",
            y_col: y_col
        },
        template="plotly_white",
        opacity=0.7
    )

    fig.update_traces(marker=dict(size=6))
    return fig


def plot_candlestick(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(data=[go.Candlestick(
        x=df["Timestamp"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Candlestick"
    )])

    fig.update_layout(
        title="Bitcoin Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white"
    )

    return fig
