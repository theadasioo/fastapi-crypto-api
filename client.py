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

if __name__ == "__main__":
    print("USD TEST")
    get_price("bitcoin", "usd")

    print("\nEUR TEST")
    get_price("bitcoin", "eur")

    print("\nPLN TEST")
    get_price("bitcoin", "pln")

    print("\nHISTORY EUR")
    get_history("bitcoin", 1, "eur")