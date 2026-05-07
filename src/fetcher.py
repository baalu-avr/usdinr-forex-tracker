import yfinance as yf
import pandas as pd


def fetch_usdinr(period="10y", interval="1d"):
    """
    Fetches USD/INR historical exchange rate data from Yahoo Finance.
    
    period: how far back to fetch — "1y", "5y", "10y", "max"
    interval: data frequency — "1d", "1wk", "1mo"
    
    Returns a clean DataFrame with Date and Close (exchange rate) columns.
    """

    print(f"Fetching USD/INR data ({period})...")
    
    # Yahoo Finance ticker for USD/INR
    ticker = yf.Ticker("INR=X")
    df = ticker.history(period=period, interval=interval)

    # Reset index to make Date a column
    df = df.reset_index()

    # Keep only what we need
    df = df[["Date", "Close"]].copy()
    df.columns = ["date", "usdinr"]

    # Clean up date format
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)

    # Drop missing values
    df = df.dropna().reset_index(drop=True)

    print(f"✅ Fetched {len(df)} records")
    print(f"📅 Date range: {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"💱 Current USD/INR: ₹{df['usdinr'].iloc[-1]:.2f}")

    return df


def get_summary(df):
    """
    Prints a quick summary of USD/INR trends.
    """
    current = df["usdinr"].iloc[-1]
    one_year_ago = df[df["date"] >= df["date"].max() - pd.DateOffset(years=1)]["usdinr"].iloc[0]
    five_years_ago = df[df["date"] >= df["date"].max() - pd.DateOffset(years=5)]["usdinr"].iloc[0]

    print("\n📊 USD/INR Summary:")
    print(f"   Current Rate     : ₹{current:.2f}")
    print(f"   1 Year Ago       : ₹{one_year_ago:.2f}  ({((current - one_year_ago) / one_year_ago * 100):+.1f}%)")
    print(f"   5 Years Ago      : ₹{five_years_ago:.2f}  ({((current - five_years_ago) / five_years_ago * 100):+.1f}%)")
    print(f"   All-time High    : ₹{df['usdinr'].max():.2f}")
    print(f"   All-time Low     : ₹{df['usdinr'].min():.2f}")


if __name__ == "__main__":
    df = fetch_usdinr(period="10y")
    get_summary(df)