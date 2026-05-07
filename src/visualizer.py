import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os


def plot_usdinr(df, save=True):
    """
    Plots USD/INR exchange rate history with key economic events annotated.
    """

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(df["date"], df["usdinr"],
            color="#2196F3", linewidth=1.5, label="USD/INR Rate")

    ax.fill_between(df["date"], df["usdinr"],
                    df["usdinr"].min(), alpha=0.1, color="#2196F3")

    # Annotate key economic events
    events = [
        ("2020-03-23", "COVID Crash\n₹76+", -3),
        ("2022-10-01", "All-time\nHigh ~₹83", -4),
        ("2024-11-01", "Post-Trump\nSurge", -4),
    ]

    for date, label, offset in events:
        event_date = pd.Timestamp(date)
        if df["date"].min() <= event_date <= df["date"].max():
            rate = df[df["date"] >= event_date]["usdinr"].iloc[0]
            ax.annotate(label,
                        xy=(event_date, rate),
                        xytext=(0, 30 + offset * 5),
                        textcoords="offset points",
                        fontsize=8, color="#E63946",
                        arrowprops=dict(arrowstyle="->", color="#E63946", lw=1),
                        ha="center")

    # Latest rate annotation
    latest = df.iloc[-1]
    ax.annotate(f'Today: ₹{latest["usdinr"]:.2f}',
                xy=(latest["date"], latest["usdinr"]),
                xytext=(-80, 15), textcoords="offset points",
                fontsize=10, fontweight="bold", color="#2196F3",
                arrowprops=dict(arrowstyle="->", color="#2196F3", lw=1.5))

    ax.set_title("USD/INR Exchange Rate — Rupee Depreciation (2016–2026)",
                 fontsize=16, fontweight="bold", pad=20)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("₹ per 1 USD", fontsize=12)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    plt.xticks(rotation=45)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(fontsize=11)

    fig.text(0.99, 0.01, "Source: Yahoo Finance (INR=X)",
             ha="right", fontsize=9, color="gray")

    plt.tight_layout()

    if save:
        os.makedirs("output/charts", exist_ok=True)
        filepath = "output/charts/usdinr_history.png"
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        print(f"Chart saved to {filepath}")

    plt.show()


def plot_yearly_depreciation(df, save=True):
    """
    Bar chart showing how much the rupee depreciated each year.
    """

    df = df.copy()
    df["year"] = df["date"].dt.year
    yearly = df.groupby("year")["usdinr"].mean().reset_index()
    yearly["change"] = yearly["usdinr"].pct_change() * 100
    yearly = yearly.dropna()

    colors = ["#E63946" if x > 0 else "#4CAF50" for x in yearly["change"]]

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(yearly["year"], yearly["change"], color=colors, edgecolor="white", linewidth=0.5)

    ax.axhline(y=0, color="white", linewidth=0.8, alpha=0.5)

    for bar, val in zip(bars, yearly["change"]):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + (0.1 if val > 0 else -0.3),
                f"{val:+.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_title("Rupee Depreciation vs USD — Year by Year (%)",
                 fontsize=16, fontweight="bold", pad=20)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Change in USD/INR (%)", fontsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    fig.text(0.99, 0.01, "Source: Yahoo Finance (INR=X)",
             ha="right", fontsize=9, color="gray")

    plt.tight_layout()

    if save:
        os.makedirs("output/charts", exist_ok=True)
        filepath = "output/charts/yearly_depreciation.png"
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        print(f"Chart saved to {filepath}")

    plt.show()


if __name__ == "__main__":
    from fetcher import fetch_usdinr

    df = fetch_usdinr(period="10y")
    print("\nGenerating charts...")
    plot_usdinr(df)
    plot_yearly_depreciation(df)
    print("Done! Check output/charts/ folder.")