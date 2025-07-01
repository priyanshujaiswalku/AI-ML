import yfinance as yf
from datetime import datetime, timedelta

# path = 'c:\Users\Priyanshu kumar\OneDrive\Desktop\Arkalogi\Task7\app\Data\sbin_2025-06-12.csv'
date = '2025-06-18'
symbol = 'sbin'

def fetch_required_data(date:str, path:str, stock:str):

    if '.NS' not in stock:
        stock = stock.upper()+'.NS'
    else:
        stock = stock.upper()
        
    
    datetime_obj = datetime.strptime(date, "%Y-%m-%d").date()
    end_date = datetime_obj+timedelta(days=1)
    end_date_str = end_date.strftime("%Y-%m-%d")
    print("date", date, type(date))
    print("end_date_str", end_date_str, type(end_date_str))

    data = yf.download(stock, start=date,end=end_date_str, interval="1d")
    if data.empty:
        print(f"No data for {stock}")
        err_msg = 'no data found'
        return err_msg
    
    print(data)
    data.to_csv(path)

err_msg = fetch_required_data(date, '', symbol)
if err_msg:
    print("issue is with the data downloading")
else:
    print("data downloading is successfull")
