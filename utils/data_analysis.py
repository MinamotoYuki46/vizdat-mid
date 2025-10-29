import pandas as pd

def calculate_volatility(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Volatility(%)"] = ((df["High"] - df["Low"]) / df["Open"]) * 100
    return df


def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Daily_Return(%)"] = df["Close"].pct_change() * 100
    return df


def calculate_moving_averages(df: pd.DataFrame, windows=(7, 30)) -> pd.DataFrame:
    df = df.copy()
    for w in windows:
        df[f"MA_{w}"] = df["Close"].rolling(window=w).mean()
    return df


def prepare_analysis_data(df: pd.DataFrame) -> pd.DataFrame:
    df = calculate_volatility(df)
    df = calculate_returns(df)
    df = calculate_moving_averages(df)
    return df


if __name__ == "__main__":
    from data_cleaning import load_and_clean_data

    df = load_and_clean_data("data/btcusd_1-min_data.csv")
    analyzed = prepare_analysis_data(df)
    print(analyzed.head())
    print(analyzed.describe())
