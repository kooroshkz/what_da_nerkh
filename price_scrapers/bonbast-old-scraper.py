from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
from datetime import datetime, timezone
import time
import os

def clean_price(text):
    return int(text.replace(",", "").replace(" ", ""))

def get_currencies_bonbast():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.bon-bast.com/")
    time.sleep(2)

    now_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    result = {}

    tables = driver.find_elements(By.CSS_SELECTOR, "table.table-condensed")

    for table in tables:
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]

        for row in rows:
            tds = row.find_elements(By.TAG_NAME, "td")
            if len(tds) < 4:
                continue

            try:
                code = tds[0].find_element(By.TAG_NAME, "img").get_attribute("alt").upper().strip()
            except Exception:
                continue

            name = tds[1].text.strip()

            try:
                sell = clean_price(tds[2].text)
            except Exception:
                sell = None

            try:
                buy = clean_price(tds[3].text)
            except Exception:
                buy = None

            if "Armenian Dram" in name or code == "AMD":
                if sell: sell = sell / 10
                if buy: buy = buy / 10
            if "Japanese Yen" in name or code == "JPY":
                if sell: sell = sell / 10
                if buy: buy = buy / 10
            if "Iraqi Dinar" in name or code == "IQD":
                if sell: sell = sell / 100
                if buy: buy = buy / 100

            result[code] = {
                "code": code,
                "name": name,
                "buy": buy,
                "sell": sell,
                "timestamp": now_utc
            }

    driver.quit()
    return {
        "updated_at": now_utc,
        "currencies": result
    }

if __name__ == "__main__":
    data = get_currencies_bonbast()
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "price_data")

    with open(os.path.join(data_dir, "bonbast_live.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    all_data = []
    historical_file = os.path.join(data_dir, "bonbast_historical.json")
    if os.path.exists(historical_file):
        with open(historical_file, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except Exception:
                all_data = []
    all_data.append(data)
    with open(historical_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)