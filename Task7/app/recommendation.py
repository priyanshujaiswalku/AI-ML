def generate_recommendation(df, indicators, period=14):
    last = df.iloc[-1]

    close = last['Close']
    
    signal = "Hold"
    confidence = 50
    rsi = stoch = ema = sma = None

    if 'RSI' in indicators:
        rsi = last.get(f'RSI_{period}')
        if rsi is not None:
            if rsi < 30:
                signal = "Buy"
                confidence += 25
            elif rsi > 70:
                signal = "Sell"
                confidence += 25

    if 'StochRSI' in indicators:
        stoch = last.get(f'StochRSI_{period}')
        if stoch is not None:
            if stoch < 0.2:
                signal = "Buy"
                confidence += 15
            elif stoch > 0.8:
                signal = "Sell"
                confidence += 15

    if 'EMA' in indicators:
        ema = last.get(f'EMA_{period}')
        if ema is not None:
            if close > ema:
                confidence += 5
            else:
                confidence -= 5

    if 'SMA' in indicators:
        sma = last.get(f'SMA_{period}')
        if sma is not None:
            if close > sma:
                confidence += 5
            else:
                confidence -= 5

    recommendation = {
        "Signal": signal,
        "Confidence": min(confidence, 100),
        "RSI": round(rsi, 2) if rsi is not None else "-",
        "StochRSI": round(stoch, 2) if stoch is not None else "-",
        "EMA": round(ema, 2) if ema is not None else "-",
        "SMA": round(sma, 2) if sma is not None else "-",
        "Price": round(close, 2),
        "Symbol": df.iloc[-1]['Symbol'].upper() if 'Symbol' in df.columns else "-",
        "Date": df.iloc[-1]['Date'] if 'Date' in df.columns else "-"
    }

    return recommendation
