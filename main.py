from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import requests
from datetime import datetime, timedelta



app = FastAPI()

# === ALERT  MODEL ===
class Alert(BaseModel):
    coin: str
    target_price: float
    condition: str    # above or below


# storage
alerts = []
next_id = 1




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





# /alerts
@app.post("/alerts")
def create_alert(alert: Alert):
    global next_id

    if alert.condition not in ["above", "below"]:
        raise HTTPException(status_code=400, detail="Condition must be 'above' or 'below'")

    new_alert = {
        "id" : next_id,
        "coin" : alert.coin,
        "target_price" : alert.target_price,
        "condition" : alert.condition
    }

    alerts.append(new_alert)
    next_id += 1

    return new_alert

@app.get("/alerts")
def get_alerts():
    return alerts


def check_alerts_logic():
    triggered = []

    for alert in alerts:
        coin = alert["coin"]
        target = alert["target_price"]
        condition = alert["condition"]

        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": coin,
            "vs_currencies": "usd"
        }

        response = requests.get(url, params=params)
        data = response.json()

        price = data.get(coin, {}).get("usd")

        if price is None:
            continue

        if condition == "above" and price > target:
            triggered.append({
                "coin": coin,
                "price": price,
                "target": target
            })

        if condition == "below" and price < target:
            triggered.append({
                "coin": coin,
                "price": price,
                "target": target
            })

    return triggered


@app.get("/check_alerts")
def check_alerts():
    return {
        "triggered_alerts": check_alerts_logic()
    }








