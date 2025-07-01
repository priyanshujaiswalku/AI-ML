import pandas as pd

def calculate_sma(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    df[f'SMA_{period}'] = df['Close'].rolling(window=period).mean()
    return df

def calculate_ema(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    df[f'EMA_{period}'] = df['Close'].ewm(span=period, adjust=False).mean()
    return df

def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df[f'RSI_{period}'] = 100 - (100 / (1 + rs))
    return df

def calculate_stoch_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    df = calculate_rsi(df, period)
    rsi_col = f'RSI_{period}'
    min_rsi = df[rsi_col].rolling(window=period).min()
    max_rsi = df[rsi_col].rolling(window=period).max()
    df[f'StochRSI_{period}'] = (df[rsi_col] - min_rsi) / (max_rsi - min_rsi)
    return df
