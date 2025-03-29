def get_price(binance, symbol="BTC/BRL"):
    try:
        order_book = binance.fetch_order_book(symbol)
        bid = order_book['bids'][0][0] if order_book['bids'] else None
        ask = order_book['asks'][0][0] if order_book['asks'] else None
        mid = (bid + ask) / 2 if bid and ask else None

        return {
            "bid": bid,
            "ask": ask,
            "mid": mid
        }
    except Exception as e:
        print(f"[ERRO - Order Book] {e}")
        return {"bid": None, "ask": None, "mid": None}

def get_candles(binance, symbol="BTC/BRL", timeframe='1m', limit=10):
    try:
        candles = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        return candles
    except Exception as e:
        print(f"[ERRO - Candles] {e}")
        return []