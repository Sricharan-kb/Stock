import streamlit as st
import pandas as pd
import requests

API_URL = "https://stock-api-5tzk.onrender.com"  

#Stock name and Ticker Mapping
stock_options = {
    "Apple Inc. (AAPL)": "AAPL",
    "Microsoft Corp. (MSFT)": "MSFT",
    "Alphabet Inc. (GOOGL)": "GOOGL",
    "Tesla Inc. (TSLA)": "TSLA",
    "Amazon.com Inc. (AMZN)": "AMZN"
}

#Important Ratios and Benchmarks
financial_ratios = {
    "Profitability": {
        "grossProfitMarginTTM": ("Gross Profit Margin", "Higher is better"),
        "netProfitMarginTTM": ("Net Profit Margin", "Higher is better"),
        "operatingProfitMarginTTM": ("Operating Profit Margin", "Higher is better")
    },
    "Liquidity": {
        "currentRatioTTM": ("Current Ratio", "Ideal > 1.5"),
        "quickRatioTTM": ("Quick Ratio", "Ideal > 1.0"),
        "cashRatioTTM": ("Cash Ratio", "Higher is better")
    },
    "Valuation": {
        "peRatioTTM": ("P/E Ratio", "Ideal < 25"),
        "priceToBookRatioTTM": ("P/B Ratio", "Lower is better"),
        "priceToSalesRatioTTM": ("P/S Ratio", "Lower is better (<2 ideal)")
    },
    "Returns": {
        "returnOnEquityTTM": ("Return on Equity", "Higher is better"),
        "returnOnAssetsTTM": ("Return on Assets", "Higher is better")
    },
    "Leverage": {
        "debtEquityRatioTTM": ("Debt to Equity", "Ideal < 1.0"),
        "debtRatioTTM": ("Debt Ratio", "Lower is better")
    }
}

def format_val(val):
    if val is None:
        return "N/A"
    try:
        if abs(val) < 1:
            return f"{val * 100:.2f}%"
        return f"{val:.2f}"
    except:
        return str(val)


def main():
    st.set_page_config(page_title="📊 Stock Insights", layout="wide")
    st.title("📊 Stock Insights")

    st.sidebar.header("Select a Stock")
    selected_label = st.sidebar.selectbox("Choose a company", list(stock_options.keys()))
    symbol = stock_options[selected_label]
    company_name = selected_label.split(" (")[0]

    col1, col2 = st.columns(2)

    # --- Financial Ratios Section ---
    with col1:
        if st.button("Get Financial Ratios"):
            try:
                res = requests.get(f"{API_URL}/ratios/{symbol}")
                res.raise_for_status()
                data = res.json()

                if not data or not isinstance(data, list):
                    st.warning("No ratio data available.")
                    return

                ratios = data[0]
                st.subheader(f"📈 Financial Ratios for {company_name} ({symbol})")
                for category, metrics in financial_ratios.items():
                    st.markdown(f"### {category}")
                    for key, (label, benchmark) in metrics.items():
                        val = format_val(ratios.get(key))
                        st.markdown(f"**{label}:** {val} _(Benchmark: {benchmark})_")
            except Exception as e:
                st.error(f"Error fetching ratios: {e}")

    # --- Historical Prices Section ---
    with col2:
        if st.button("Get Historical Prices"):
            try:
                res = requests.get(f"{API_URL}/prices/{symbol}")
                res.raise_for_status()
                prices = res.json()

                if isinstance(prices, list) and prices:
                    df = pd.DataFrame(prices)
                    df["date"] = pd.to_datetime(df["date"])
                    df = df.sort_values("date")

                    df["% Change"] = df["close"].pct_change() * 100
                    df["VWAP"] = (df["close"] * df["volume"]).cumsum() / df["volume"].cumsum()

                    st.subheader(f"📅 Historical Prices for {company_name} ({symbol})")
                    st.dataframe(
                        df[["date", "open", "high", "low", "close", "volume", "% Change", "VWAP"]]
                        .sort_values("date", ascending=False).head(20),
                        use_container_width=True
                    )

                    st.line_chart(df.set_index("date")[["close", "VWAP"]])

                    st.markdown("""
###  Explanation

####  VWAP (Volume Weighted Average Price)
VWAP gives the average price of a stock over the day, weighted by volume.  
It reflects the **true average price** at which most trading took place.

- **If Price > VWAP** → Stock is trading above average → Could signal **bullish momentum**
- **If Price < VWAP** → Stock is trading below average → Could signal **bearish pressure**
- **Used by:** Institutional investors to assess if they bought/sold at a good price.

It’s commonly used as a **reference line** for:
- Timing entries and exits
- Avoiding trades far from fair value
- Measuring trade execution quality

####  % Change (Daily Return)
% Change shows how much the stock price moved from the **previous day's close**.

- A **positive % change** means the stock **gained value**
- A **negative % change** means the stock **lost value**
- Large changes may signal:
- Earnings reports
- Market news
- Economic events
- Sector-wide movement

""")

                else:
                    st.warning("No historical price data found.")
            except Exception as e:
                st.error(f"Error fetching historical prices: {e}")

if __name__ == "__main__":
    main()
