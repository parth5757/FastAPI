# backend/tests/test_main.py

from fastapi.testclient import TestClient
import sys
sys.path.append("d:/FastAPI/NSE_Stock/backend")
from main import app

# Create a TestClient using the FastAPI app
client = TestClient(app)

def test_get_stock_data_valid_ticker():
    # Example with a valid NSE stock ticker
    response = client.get("/stock/TCS")
    assert response.status_code == 200
    data = response.json()
    assert "ticker" in data
    assert "all_time_high" in data
    assert "current_price" in data
    assert "difference" in data
    assert data["ticker"] == "TCS"

def test_get_stock_data_invalid_ticker():
    # Example with an invalid ticker
    response = client.get("/stock/INVALIDTICKER")
    assert response.status_code == 200  # FastAPI should handle this, no 404
    data = response.json()
    assert data["all_time_high"] == 0  # If the ticker doesn't exist, you can customize the response for such cases
