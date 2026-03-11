from fastapi import FastAPI, Query, HTTPException
import requests
from datetime import datetime, timedelta

app = FastAPI()

# API endpoints

# /price -> current cryptocurrency price
@app.get("/price")
def get_price(
        coin: str = Query("bitcoin", description="Coin ID in CoinGecko"),
        currency: str = Query("usd", description="Target currency (usd, eur, pln...)")):
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids" : coin,
        "vs_currencies" : currency
    }

    response = requests.get(url, params=params)
    data = response.json()


    #   data = {
    #       "bitcoin" : {
    #           "usd" : ...
    #       }
    #   }

    price = data.get(coin)
    if price is None:
        raise HTTPException(status_code=404, detail="Coin not found")

    return{
        "coin" : coin,
        "price_usd" : price
    }


# /history
@app.get("/history")
def get_history(
    coin : str = Query("bitcoin", description="Coin ID"),
    days : int = Query(7, description="number of days back", ge=1, le=365),
    currency: str = Query("usd", description="Target currency")
):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"

    params = {
        "vs_currency" : currency,
        "days" : days
    }

    response = requests.get(url, params=params)
    data = response.json()

    prices = data.get("prices", [])
    if prices is None:
        raise HTTPException(status_code=404, detail="Coin not found")


    result = []
    last_added_time = None
    interval = timedelta(hours = 2)

    for timestamp, price in prices:
        date = datetime.fromtimestamp(timestamp / 1000)  # convert milliseconds timestamp to seconds and then to datetime
        if last_added_time is None or date - last_added_time >= interval:
            result.append({
                "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "price": round(price, 2)
            })

            last_added_time = date


    return{
        "coin" : coin,
        "currency": currency,
        "days" : days,
        "prices" : result
    }
    


