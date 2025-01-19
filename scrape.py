import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.tgju.org/profile/price_eur"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_euro_price():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        price_tag = soup.find("span", {"data-col": "info.last_trade.PDrCotVal"})
        if price_tag:
            price = price_tag.text.replace(",", "")
            return int(price) // 10  # Drop last digit
    return None

price = fetch_euro_price()
if price:
    with open("price.json", "w") as file:
        json.dump({"price": price}, file)
