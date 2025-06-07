A Streamlit-based web application that retrieves, analyzes, and displays categorized financial ratios and historical price data for NASDAQ-listed stocks. It compares each ratio against industry benchmarks, helping users evaluate a stock’s market position at a glance.

---

## 🚀 Features

- 🔍 Search NASDAQ stock by ticker symbol(limited to 5 stocks for now- more to be added soon!)
- 📊 Display key financial ratios across categories:
  - **Profitability**
  - **Liquidity**
  - **Valuation**
  - **Leverage (Solvency)**
  - **Returns & Yield**
- 🟢 Ratio interpretations with benchmarks (e.g., P/E Ratio < 25)
- 📉 Historical price chart with:
  - **VWAP** (Volume Weighted Average Price)
  - **% Change** (daily returns)
- 🧠 Clean, readable UI with real-time data
- ☁️ Deployed with **Render**

---
🛠 Tools & Technologies
Python

Streamlit (Frontend UI)

FastAPI (Backend API service)

Financial Modeling Prep API (Financial data source)

Render (Cloud deployment)


---
🚧 Usage Instructions
Clone the repository:

```
git clone https://github.com/Sricharan-Kb/stock.git
cd stock
```
---
Create and activate a virtual environment (recommended):

```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
---
Install dependencies:

```
pip install -r requirements.txt
```
---
Create a .env file and add your Financial Modeling Prep API key:
```
FMP_API_KEY=your_api_key_here
```
---
Run backend FastAPI server:
```
uvicorn backend:app --host 0.0.0.0 --port 8000
```

---
Run Streamlit frontend:
```
streamlit run "whatever you name your frontend".py
```
Open http://localhost:8501 in your browser.
