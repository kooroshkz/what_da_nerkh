import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timezone, timedelta

FILE_PATH = "exchange_rate.json"
CET = timezone(timedelta(hours=1))  # Central European Time

def fetch_conversion_rate():
    url = "https://alanchand.com/currencies-price/eur"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch page")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    conversion_element = soup.select_one('td[data-v-c1354816=\"\"]:nth-of-type(2)')
    if not conversion_element:
        print("Failed to extract rate")
        return None
    conversion_rate = float(conversion_element.text.replace(',', '').replace('تومان', '').strip())
    return conversion_rate

def update_json(conversion_rate):
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    data = [data]
                elif not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append({
        "rate": conversion_rate,
        "timestamp": datetime.now(CET).isoformat() + " CET"
    })

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Updated exchange_rate.json.")

if __name__ == "__main__":
    rate = fetch_conversion_rate()
    if rate:
        update_json(rate)
