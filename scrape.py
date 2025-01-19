import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.tgju.org/profile/price_eur"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_euro_price():
    print("Fetching Euro price from:", URL)
    
    response = requests.get(URL, headers=HEADERS)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        price_tag = soup.find("span", {"data-col": "info.last_trade.PDrCotVal"})
        
        if price_tag:
            price = price_tag.text.replace(",", "").strip()
            print("Scraped price:", price)
            return int(price) // 10  # Remove last digit
        else:
            print("❌ Error: Could not find price tag.")
    else:
        print(f"❌ HTTP Error: {response.status_code}")

    return None

# Fetch price
price = fetch_euro_price()

# Debugging: Print output for GitHub Actions
print("Fetched Price:", price)

if price:
    print("✅ Saving price to price.json")
    with open("price.json", "w") as file:
        json.dump({"price": price}, file, indent=4)
else:
    print("❌ Failed to fetch price")

# Check if the file was written correctly
with open("price.json", "r") as file:
    print("🔍 price.json content:", file.read())
