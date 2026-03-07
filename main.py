from fastapi import FastAPI, Query
import requests
from datetime import datetime, timedelta

app = FastAPI()

# API endpoints

# /price -> current cryptocurrency price
@app.get("/price")
def get_price(coin: str = Query("bitcoin", description="Coin ID in CoinGecko")):
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids" : coin,
        "vs_currencies" : "usd"
    }

    response = requests.get(url, params=params)
    data = response.json()


    #   data = {
    #       "bitcoin" : {
    #           "usd" : ...
    #       }
    #   }

    price = data.get(coin, {}).get("usd")

    return{
        "coin" : coin,
        "price_usd" : price
    }


# /history
@app.get("/history")
def get_history(
    coin : str = Query("bitcoin", description="Coin ID"),
    days : int = Query(7, description="number of days back")
):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"

    params = {
        "vs_currency" : "usd",
        "days" : days
    }

    response = requests.get(url, params=params)
    data = response.json()

    prices = data.get("prices", [])


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
        "days" : days,
        "prices" : result
    }
    


