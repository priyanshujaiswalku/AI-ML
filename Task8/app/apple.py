from flask import Flask, jsonify, render_template, send_file
import pandas as pd
import yfinance as yf
from datetime import datetime
from flask import Blueprint, render_template, request
import os

apple_bp = Blueprint('apple', __name__)

INDEX_SYMBOLS = { 'NIFTY 50': '^NSEI', 'SENSEX': '^BSESN','BSE MidCap': 'BSE-MIDCAP.BO'}

@apple_bp.route('/index')
def index():
    return render_template('index.html')

@apple_bp.route('/api/indices', methods=['GET', 'POST'])
def get_indices_data():  
    data = []
    for name, symbol in INDEX_SYMBOLS.items():
        base_path =os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period='1d', interval='1m')
        if hist.empty:
            continue
        last_price = hist['Close'][-1]
        prev_close = ticker.history(period='2d')['Close'][0]
        change_pct = ((last_price - prev_close) / prev_close) * 100
        data.append({
            'name': name,
            'symbol': symbol,
            'price': round(last_price, 2),
            'change_pct': round(change_pct, 2),
            'data': hist['Close'].round(2).tolist(),
            'time': hist.index.strftime('%H:%M').tolist()
        })
    return jsonify(data)




