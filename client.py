import requests

BASE_URL = "http://127.0.0.1:8000"

def get_price(coin = "bitcoin"):
    response = requests.get(f"{BASE_URL}/price", params={"coin" : coin})
    print("PRICE: ")
    print(response.json())

def get_history(coin = "bitcoin", days = 7):
    response = requests.get(f"{BASE_URL}/history", params={"coin" : coin, "days": days})
    print("HISTORY: ")
    print(response.json())

if __name__ == "__main__":
    get_price("bitcoin")
    get_history("bitcoin", 1)