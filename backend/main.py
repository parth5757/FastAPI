# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd

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
    difference_percentage = 100 - (current_price * 100 / all_time_high)

    # Return the result as JSON
    return {
        "ticker": ticker,
        "all_time_high": round(all_time_high),
        "current_price": round(current_price),
        "difference": round(difference),
        "difference_percentage": round(difference_percentage)
    }

# @app.get("/stock_symbol/")
# async def get_stock_symbol():
#     # Load the CSV file containing NSE stock symbols
#     nse = pd.read_csv('nse_files/nifty50.csv')
    
#     # Strip any extra whitespace from column names
#     nse.columns = nse.columns.str.strip()
    
#     # Extract the 'SYMBOL' column and convert it to a list
#     nse_symbol_list = nse['SYMBOL'].tolist()
    
#     # Print the list of symbols for debugging
#     print(nse_symbol_list)
    
#     # Return the list of symbols as a JSON response
#     # return {"symbols": nse_symbol_list}

#     for symbol in nse_symbol_list:
#         return{
#             "symbol": symbol
#         }

@app.get("/stock_symbol/")
async def get_stock_symbol():
    # Load the CSV file containing NSE stock symbols
    nse = pd.read_csv('nse_files/nifty50.csv')
    
    # Strip any extra whitespace from column names
    nse.columns = nse.columns.str.strip()
    
    # Extract the 'SYMBOL' column and convert it to a list
    nse_symbol_list = nse['SYMBOL'].tolist()
    
    # Initialize a list to hold stock data
    stock_data_list = []

    # Fetch data for each symbol
    for symbol in nse_symbol_list:
        stock = yf.Ticker(f"{symbol}.NS")
        history = stock.history(period="max")

        if not history.empty:  # Check if history has data
            current_price = history['Close'][-1]
            all_time_high = history['Close'].max()
            difference = all_time_high - current_price
            difference_percentage = 100 - (current_price * 100 / all_time_high)
            
            stock_data_list.append({
                "ticker": symbol,
                "all_time_high": round(all_time_high),
                "current_price": round(current_price),
                "difference": round(difference),
                "difference_percentage": round(difference_percentage)
            })

    # Return the list of stock data
    return {"stocks": stock_data_list}
