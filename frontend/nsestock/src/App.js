// frontend/src/App.js

import React, { useState } from "react";

function App() {
  const [ticker, setTicker] = useState("");
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchStockData = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/stock/${ticker}`);
      const data = await response.json();
      setStockData(data);
    } catch (error) {
      console.error("Error fetching stock data:", error);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>NSE Stock Price Checker</h1>
      <input
        type="text"
        placeholder="Enter NSE Ticker (e.g. TCS)"
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
      />
      <button onClick={fetchStockData} disabled={loading}>
        {loading ? "Fetching..." : "Get Stock Data"}
      </button>

      {stockData && (
        <div>
          <h2>{stockData.ticker.toUpperCase()}</h2>
          <p>All-Time High: ₹{stockData.all_time_high}</p>
          <p>Current Price: ₹{stockData.current_price}</p>
          <p>Difference: ₹{stockData.difference}</p>
        </div>
      )}
    </div>
  );
}

export default App;
