import requests
from bs4 import BeautifulSoup
import json
import os
import subprocess
from datetime import datetime, timezone, timedelta

FILE_PATH = "exchange_rate.json"
CET = timezone(timedelta(hours=1))  # Central European Time (CET)

def fetch_conversion_rate():
    url = "https://alanchand.com/currencies-price/eur"
    headers = {"User-Agent": "Mozilla/5.0"}  # Prevents blocking by some servers
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to fetch the page")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    conversion_element = soup.select_one('td[data-v-c1354816=""]:nth-of-type(2)')
    
    if not conversion_element:
        print("Failed to extract conversion rate")
        return None
    
    conversion_rate = float(conversion_element.text.replace(',', '').replace('تومان', '').strip())
    return conversion_rate

def update_json(conversion_rate):
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)

                # If data is a dictionary (old format), convert it to a list
                if isinstance(data, dict):
                    data = [data]
                elif not isinstance(data, list):
                    data = []
                    
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append new exchange rate entry
    data.append({
        "rate": conversion_rate,
        "timestamp": datetime.now(CET).isoformat() + " CET"
    })

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Updated exchange_rate.json with new exchange rate.")

def commit_and_push():
    try:
        subprocess.run(["git", "config", "user.name", "github-actions"], check=True)
        subprocess.run(["git", "config", "user.email", "github-actions@github.com"], check=True)
        subprocess.run(["git", "add", FILE_PATH], check=True)
        subprocess.run(["git", "commit", "-m", "Updated exchange rate"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except subprocess.CalledProcessError as e:
        print("Git commit/push failed:", e)

if __name__ == "__main__":
    rate = fetch_conversion_rate()
    if rate:
        update_json(rate)
        commit_and_push()
