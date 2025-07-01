import os
from flask import Blueprint, render_template, request
import pandas as pd

market_insight_bp = Blueprint('market_insight', __name__)

STOCKS = ['SBIN.NS', 'TATAMOTORS.NS', 'RELIANCE.NS', 'INFY.NS', 'HDFCBANK.NS',
          'ITC.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'LT.NS', 'TCS.NS']

@market_insight_bp.route('/')
def home():
    return render_template('home.html')

@market_insight_bp.route('/select_service')
def select_service():
    return render_template('service_select.html')

@market_insight_bp.route('/market_insight', methods=['POST'])
def market_insight():
    sma_length = int(request.form['sma_length'])
    result = get_market_insight(sma_length)
    return render_template('result.html', result=result)

def get_market_insight(sma_length):
    above_sma = []
    below_sma = []

    for stock in STOCKS:
        base_path =os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
        folder_path = os.path.join(base_path, f"{stock}.csv")
        data = pd.read_csv(folder_path)
        data['Close'] = pd.to_numeric(data['Close'], errors='coerce')
        sma = data['Close'].rolling(window=sma_length).mean()
        latest_close = data['Close'].iloc[-1]
        latest_sma = sma.iloc[-1]

        if latest_close > latest_sma:
            above_sma.append(stock.split('.')[0])
        else:
            below_sma.append(stock.split('.')[0])

    return {"above_sma": above_sma, "below_sma": below_sma}
