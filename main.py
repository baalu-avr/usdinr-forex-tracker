from src.fetcher import fetch_usdinr, get_summary
from src.visualizer import plot_usdinr, plot_yearly_depreciation

def main():
    print("=" * 50)
    print("   USD/INR Forex Tracker")
    print("=" * 50)

    df = fetch_usdinr(period="10y")
    get_summary(df)

    print("\n📊 Generating charts...")
    plot_usdinr(df)
    plot_yearly_depreciation(df)
    print("\n✅ Done! Charts saved to output/charts/")

if __name__ == "__main__":
    main()