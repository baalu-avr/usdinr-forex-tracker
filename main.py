from src.fetcher import fetch_usdinr, get_summary
from src.visualizer import plot_usdinr, plot_yearly_depreciation
import sys

def main():
    print("=" * 50)
    print("   USD/INR Forex Tracker")
    print("=" * 50)

    try:
        df = fetch_usdinr(period="10y")
        get_summary(df)
        print("\n📊 Generating charts...")
        plot_usdinr(df, save=True)
        plot_yearly_depreciation(df, save=True)
        print("\n✅ Done! Charts saved to output/charts/")
    except Exception as e:
        print(f"⚠️ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()