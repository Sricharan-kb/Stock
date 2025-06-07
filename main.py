from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "Put Your API key here"
BASE_URL = "https://financialmodelingprep.com/api/v3"

@app.get("/tickers")
def get_tickers():

    # To keep it simple, return a fixed list of tickers here
    return ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

@app.get("/ratios/{symbol}")
def get_ratios(symbol: str):
    url = f"{BASE_URL}/ratios-ttm/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    return response.json()

@app.get("/prices/{symbol}")
def get_prices(symbol: str):
    url = f"{BASE_URL}/historical-price-full/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "historical" in data:
        return data["historical"]
    return []
