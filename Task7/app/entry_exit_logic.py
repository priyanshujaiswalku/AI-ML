import os
import pandas as pd
from flask import Flask, render_template, request
from datetime import datetime, timedelta
from pydantic import BaseModel, validator, ValidationError
from typing import Literal
import re
import sys
from Task6a.app.market_insight import market_insight_bp
from Task8.app.apple import apple_bp
from flask import Blueprint
from .indicators import calculate_sma, calculate_ema, calculate_rsi, calculate_stoch_rsi
from .recommendation import generate_recommendation


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..Task6a/app')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..Task8/app')))

app1 = Flask(__name__)
app1.register_blueprint(market_insight_bp)
app1.register_blueprint(apple_bp)


class EntryExitForm(BaseModel):
    entry_date: str
    exit_date: str
    entry_time: str
    exit_time: str
    time_frame: str
    symbol: str
    position_type: Literal['long', 'short']

    @validator('entry_date', 'exit_date')
    def validate_date_format(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v

    @validator('entry_time', 'exit_time')
    def validate_time_format(cls, v):
        if not re.match(r'^\d{2}:\d{2}$', v):
            raise ValueError('Time must be in HH:MM format')
        return v

    @validator('time_frame')
    def validate_time_frame(cls, v):
        if not re.match(r'^\d+[mhd]$', v):
            raise ValueError('Time frame must be like 5m, 1h')
        return v

    @validator('symbol')
    def symbol_lower(cls, v):
        return v.lower()


@app1.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'GET':
        return render_template("dashboard.html")
    
    if request.method == 'POST':
        symbol = request.form['symbol']
        date = request.form['date']
        selected_indicators = request.form.getlist('indicators')

        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Data'))
        file_path = os.path.join(base_path, f"{symbol}_{date}.csv")

        if not os.path.exists(file_path):
            return "Data not found for dashboard."

        df = pd.read_csv(file_path)
        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

        if 'SMA' in selected_indicators:
            df = calculate_sma(df, period=14)
        if 'EMA' in selected_indicators:
            df = calculate_ema(df, period=14)
        if 'RSI' in selected_indicators:
            df = calculate_rsi(df, period=14)
        if 'StochRSI' in selected_indicators:
            df = calculate_stoch_rsi(df, period=14)

        recommendation = generate_recommendation(df, selected_indicators, period=14)

        chart_data = {
            "labels": df['Datetime'].dt.strftime('%H:%M').tolist(),
            "close": df['Close'].tolist(),
            "sma": df['SMA_14'].tolist() if 'SMA' in selected_indicators else [],
            "ema": df['EMA_14'].tolist() if 'EMA' in selected_indicators else [],
            "rsi": df['RSI_14'].tolist() if 'RSI' in selected_indicators else [],
            "stochrsi": df['StochRSI_14'].tolist() if 'StochRSI' in selected_indicators else []
        }


        return render_template("dashboard.html", recommendation=recommendation, indicators=selected_indicators, chart_data=chart_data)


@app1.route('/entry_exit', methods=['GET', 'POST'])
def entry_exit():
    if request.method == 'GET':
        return render_template('entry_exit.html')

    if request.method == 'POST':
        log_messages = [] 
        try:
            form_data = EntryExitForm(
                entry_date=request.form['entry_date'],
                exit_date=request.form['exit_date'],
                entry_time=request.form['entry_time'],
                exit_time=request.form['exit_time'],
                time_frame='1m',
                symbol=request.form['symbol'],
                position_type=request.form['position_type']
            )
        except ValidationError as ve:
            error_dict = {error['loc'][0]: error['msg'] for error in ve.errors()}
            return render_template('Resultout.html',errors=error_dict, message="Form validation failed. Please check inputs.", message_type='error', results=[],log_messages=[] )

        entry_date = form_data.entry_date
        exit_date = form_data.exit_date
        entry_time = form_data.entry_time
        exit_time = form_data.exit_time
        time_frame = form_data.time_frame
        symbol = form_data.symbol
        position_type = form_data.position_type
     
        results = []
        current_date = pd.to_datetime(entry_date)
        final_date = pd.to_datetime(exit_date)

        while current_date <= final_date:
            date_str = current_date.strftime("%Y-%m-%d")
           
            try:
                base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Data'))
                file_path = os.path.join(base_path, f"{symbol}_{date_str}.csv")


                if not os.path.exists(file_path):
                    print(f" File not found: {file_path}")
                    log_messages.append(f"File not found: {file_path}")
                    current_date += timedelta(days=1)
                    continue


                print(f" File found: {file_path}")
                df = pd.read_csv(file_path)
                log_messages.append(f" Loaded {len(df)} rows from {file_path}")
                print(f"Loaded DataFrame with {len(df)} rows")


                if 'Datetime' not in df.columns:
                    if 'Date' in df.columns and 'Time' in df.columns:
                        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
                    else:
                        print("Missing Date or Time columns")
                        current_date += timedelta(days=1)
                        continue

                entry_price = None
                exit_price = None

                for i in range(len(df)):
                    current_time = pd.to_datetime(df.loc[i, 'Time'], format='%H:%M:%S').strftime('%H:%M')
                    if current_time == entry_time:
                        entry_price = df.loc[i, 'Close']
                    elif current_time == exit_time:
                        exit_price = df.loc[i, 'Close']

                log_messages.append(f" Entry price: {entry_price}, Exit price: {exit_price}")
                print(f" Entry Price: {entry_price}, Exit Price: {exit_price}")        

                if entry_price is None or exit_price is None:
                    log_messages.append(f" Entry or Exit time not found for {date_str}")
                    print(" Missing entry or exit price")
                    current_date += timedelta(days=1)
                    continue
                df['Time_HHMM'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.strftime('%H:%M')

                entry_row = df[df['Time_HHMM'] == entry_time]
                exit_row = df[df['Time_HHMM'] == exit_time]

                if not entry_row.empty and not exit_row.empty:
                 entry_price = entry_row.iloc[0]['Close']
                 exit_price = exit_row.iloc[0]['Close']
                pnl = (entry_price - exit_price) if position_type == 'short' else (exit_price - entry_price)
                print(f" PnL for {date_str}: {pnl:.2f}")

                results.append({
                   'entry_data': date_str,
                   'exit_data': date_str,
                   'entry_time': entry_time,
                   'exit_time': exit_time,
                   'Time Frame': time_frame,
                   'Symbol': symbol.upper(),
                   'Position Type': position_type.capitalize(),
                   'Date': date_str,
                   'Entry_Price': entry_price,
                   'Exit_Price': exit_price,
                   'PnL': round(float(pnl), 2)
                })
                log_messages.append(f" PnL for {date_str}: {pnl:.2f}")
            except Exception as e:
                log_messages.append(f" Error processing {date_str}: {str(e)}")
                print(f"Error processing {date_str}: {e}")

            current_date += timedelta(days=1)

        pnl_chart = {
            "labels": [row['Date'] for row in results],
            "pnl": [row['PnL'] for row in results]
        }
       
    return render_template('Resultout.html', results=results, log_messages=log_messages, pnl_chart=pnl_chart)
    


