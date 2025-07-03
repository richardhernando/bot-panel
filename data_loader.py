from binance.client import Client
import pandas as pd

API_KEY = 'TU_API_KEY'
API_SECRET = 'TU_API_SECRET'

client = Client(API_KEY, API_SECRET)

def get_candles(symbol='BTCUSDT', interval='1m', limit=100):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
    ])

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = df[col].astype(float)

    return df[['open', 'high', 'low', 'close', 'volume']]