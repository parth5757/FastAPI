# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

# Allowing all origins (React frontend will connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stock/{ticker}")
async def get_stock_data(ticker: str):
    # Get stock data from Yahoo Finance
    stock = yf.Ticker(f"{ticker}.NS")
    history = stock.history(period="max")

    current_price = history['Close'][-1]
    all_time_high = history['Close'].max()
    difference = all_time_high - current_price

    # Return the result as JSON
    return {
        "ticker": ticker,
        "all_time_high": round(all_time_high, 2),
        "current_price": round(current_price, 2),
        "difference": round(difference, 2),
    }


# class Return_Hello():
#     def give_name(name):
#         return "Hello" +" " + name