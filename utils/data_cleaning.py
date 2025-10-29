import pandas as pd

def load_and_clean_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    expected_cols = ["Timestamp", "Open", "High", "Low", "Close", "Volume"]
    df.columns = [col.strip() for col in df.columns]

    missing_cols = [col for col in expected_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing expected columns: {missing_cols}")

    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s", utc=True)
    df = df.sort_values("Timestamp").reset_index(drop=True)

    df = df.drop_duplicates(subset="Timestamp")

    df = (
        df.set_index("Timestamp")
        .resample("1D")
        .agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })
        .dropna()
        .reset_index()
    )

    return df


if __name__ == "__main__":
    cleaned = load_and_clean_data("data/btcusd_1-min_data.csv")
    print(cleaned.head())
    print(cleaned.info())
