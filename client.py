import requests

BASE_URL = "http://127.0.0.1:8000"

def get_price(coin = "bitcoin", currency = "usd"):
    response = requests.get(
        f"{BASE_URL}/price",
        params={"coin" : coin, "currency" : currency})

    print("PRICE: ")
    print(response.json())

def get_history(coin = "bitcoin", days = 7, currency = "usd"):
    response = requests.get(
        f"{BASE_URL}/history",
        params={"coin" : coin, "days": days, "currency" : currency})
    print("HISTORY: ")
    print(response.json())

def create_alert(coin, target_price, condition):
    response = requests.post(
        f"{BASE_URL}/alerts",
        json={
            "coin": coin,
            "target_price": target_price,
            "condition": condition
        }
    )

    print("\nCREATE ALERT:")
    print(response.json())


def get_alerts():
    response = requests.get(f"{BASE_URL}/alerts")

    print("\nALL ALERTS:")
    print(response.json())


def check_alerts():
    response = requests.get(f"{BASE_URL}/check_alerts")

    print("\nCHECK ALERTS:")
    print(response.json())


if __name__ == "__main__":

    # PRICE TEST
    get_price("bitcoin", "usd")
    get_price("bitcoin", "eur")

    # HISTORY TEST
    get_history("bitcoin", 1, "eur")

    # CREATE ALERTS
    create_alert("bitcoin", 80000, "above")
    create_alert("bitcoin", 60000, "below")

    # GET ALERTS
    get_alerts()

    # CHECK ALERTS
    check_alerts()