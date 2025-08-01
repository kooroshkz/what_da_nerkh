from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
from datetime import datetime, timezone
import time
import os
import re

DIVIDE_100 = ["JPY", "KRW", "SYP", "AMD", "IQD"]

def persian_to_english_digits(text):
    """Convert Persian/Farsi digits to English digits"""
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    
    for persian, english in zip(persian_digits, english_digits):
        text = text.replace(persian, english)
    
    return text

def extract_currency_code_from_url(onclick_attr):
    """Extract currency code from onclick URL"""
    if not onclick_attr:
        return None
    
    # Extract URL from onclick="window.location='...'"
    match = re.search(r"window\.location='([^']+)'", onclick_attr)
    if not match:
        return None
    
    url = match.group(1)
    # Extract currency code from URL like https://alanchand.com/currencies-price/usd
    parts = url.split('/')
    if len(parts) > 0:
        currency_code = parts[-1].upper()
        # Handle special cases like 'usd-hav', 'eur-ist', etc.
        if '-' in currency_code:
            # For now, skip these special variants to avoid duplicates
            return None
        return currency_code
    
    return None

def get_currency_prices_selenium():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    url = "https://alanchand.com/currencies-price"
    driver.get(url)
    time.sleep(5)  # Increased wait time for the new structure

    now_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    result = {}
    # Look for table rows in the currency tables
    rows = driver.find_elements(By.CSS_SELECTOR, "table.CurrencyTbl tbody tr")

    for row in rows:
        try:
            # Extract currency code from onclick attribute
            onclick_attr = row.get_attribute("onclick")
            currency_code = extract_currency_code_from_url(onclick_attr)
            
            if not currency_code:
                continue

            # Extract buy price
            buy_price = None
            try:
                buy_cell = row.find_element(By.CSS_SELECTOR, "td.buyPrice")
                buy_text = buy_cell.text.strip()
                # Convert Persian digits to English and remove commas
                buy_text = persian_to_english_digits(buy_text).replace(",", "")
                buy_price = float(buy_text)
            except Exception:
                buy_price = None

            # Extract sell price
            sell_price = None
            try:
                sell_cell = row.find_element(By.CSS_SELECTOR, "td.sellPrice")
                sell_text = sell_cell.text.strip()
                # Remove any extra elements like <span> tags by splitting
                sell_text = sell_text.split()[0] if sell_text else ""
                # Convert Persian digits to English and remove commas
                sell_text = persian_to_english_digits(sell_text).replace(",", "")
                sell_price = float(sell_text)
            except Exception:
                sell_price = None

            # Skip if both prices are None
            if buy_price is None and sell_price is None:
                continue

            # Apply division for specific currencies
            if currency_code in DIVIDE_100:
                if buy_price is not None:
                    buy_price = buy_price / 100
                if sell_price is not None:
                    sell_price = sell_price / 100

            result[currency_code] = {
                "buy": buy_price,
                "sell": sell_price,
                "timestamp": now_utc
            }

        except Exception as e:
            # Skip problematic rows
            continue

    driver.quit()
    return {
        "updated_at": now_utc,
        "currencies": result
    }

if __name__ == "__main__":
    data = get_currency_prices_selenium()
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "price_data")

    with open(os.path.join(data_dir, "alanchand_live.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    all_data = []
    historical_file = os.path.join(data_dir, "alanchand_historical.json")
    if os.path.exists(historical_file):
        with open(historical_file, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except Exception:
                all_data = []
    all_data.append(data)
    with open(historical_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
