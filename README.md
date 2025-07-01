💼 Arkalogi Internship – Priyanshu Kumar
Welcome! This repository documents my journey and contributions during my backend internship at Arkalogi. Below is a concise summary of all tasks assigned, my approach, and the technologies used.

📌 Task 01: NIFTY50 Option Symbol Filtering (CSV)
Objective:
Extract and process options and futures data from the Zerodha instrument CSV.

Steps:

Read the full instruments CSV using pandas.

For each NIFTY50 symbol:

Filter rows where trading_symbol starts with the symbol and ends with CE, PE, or FUT.

Extract expiry (like 25JUL) by slicing (without regex).

Sort each group by expiry and save as separate CSV.

Tech Used: Python, Pandas
Constraints: No regex, no AI tools, logic must be handcrafted.

📌 Task 02: Trade PnL & Drawdown Analysis (JSON)
Objective:
Analyze trade performance and drawdowns from a given JSON file.

Steps:

Load the JSON and flatten trades using pandas.

Calculate PnL for each trade using long/short logic.

Implement Drawdown:

Track cumulative PnL and max observed value.

Drawdown = peak - current value.

Compute metrics:

Average PnL

Top 5 profitable trades

Max drawdown

Win/loss summary

Tech Used: Python, Pandas, JSON
Output: result.csv

📌 Task 03: ML-Based PnL Percentage Prediction (CSV)
Objective:
Predict PnL % using features like support/resistance distances and entry time.

Steps:

Prepare dataset with pnl_percentage = (pnl / entry_price) * 100

Features used: support distance %, resistance distance %, time of entry

Applied ML models:

RandomForestRegressor

XGBRegressor

Evaluated model with RMSE and R² score

Tech Used: Scikit-learn, XGBoost, Pandas, Matplotlib

📌 Task 04: CSV to Python Dictionary Converter
Objective:
Convert any CSV to a structured Python dictionary for easy access.

Steps:

Read the CSV row-by-row

Construct nested dictionaries using keys like symbol → date → trade

Tech Used: Python, Pandas

📌 Task 05: Market Insight (SMA Based API)
Objective:
Build a Flask API that returns SMA-based stock performance insight.

Steps:

Download 30 days of daily OHLC data for NIFTY50 stocks using yfinance.

Calculate SMA for each stock using user-input length.

Compare current close price with SMA.

Return:

json
Copy
Edit
{ "above_sma": [...], "below_sma": [...] }
Tech Used: Flask, Pandas, YFinance, HTML

📌 Task 06: Service Selection Web App (Flask)
Objective:
Build a multipage web app with dynamic routing and form inputs.

Features:

Homepage: Service selection (Market Insight, Entry/Exit Simulator, etc.)

Individual form pages for each service

Dynamic routing using Flask Blueprints

Result pages showing calculations and charts

Tech Used: Flask, HTML, CSS, JS

📌 Task 07: Entry/Exit Trade Simulation (Backend + Frontend)
Objective:
Simulate trades over a date range using user inputs.

Steps:

Accept user inputs: symbol, entry/exit date-time, timeframe, position_type

Use existing CSV data or download 1-minute data

Resample to selected timeframe (like 5min)

Simulate entry at candle close on entry_time, and exit on exit_time

Return PnL and store result in CSV

Display results in a frontend table

Tech Used: Flask, Pandas, YFinance, Chart.js

📌 Task 08: Recommendation Dashboard
Objective:
Create an interactive dashboard with multi-indicator strategy insights.

Features:

Calculate indicators:

SMA ✅

EMA

RSI

Stochastic RSI

Generate signal/recommendation from combined indicators

Visual charts using Chart.js

Display confidence via gauge

Show PnL trend chart

Tech Used: Flask, Chart.js, Pandas, Custom Indicators

📌 Task 09: API Validation & Security (Pydantic)
Objective:
Validate API inputs/outputs using Pydantic.

Steps:

Create BaseModel classes for request validation

Enforce formats for date, time, symbols, etc.

Sanitize and validate responses

Tech Used: Flask, Pydantic

📌 Task 10: UI Polishing & Frontend Layout
Objective:
Make the UI cleaner and more user-friendly.

Features:

Add top navigation links (Market Data, Company Data, Entry/Exit, Dashboard)

Improve styling using clean layouts, colors, and fonts

Align charts and tables properly

Tech Used: HTML, CSS, JavaScript, Chart.js

📚 Skills Applied
Flask Framework (Routing, Blueprints, Templates)

API Design & Validation

Data Analysis & Time Series Resampling

Machine Learning (Regression Models)

Frontend Integration (HTML, JS, Chart.js)

GitHub & Deployment Best Practices

🔗 GitHub: github.com/priyanshujaiswalku




Tools



ChatGPT can make mistakes. Check
