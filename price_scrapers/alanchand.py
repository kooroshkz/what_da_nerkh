from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
from datetime import datetime, timezone
import time
import os

DIVIDE_100 = ["JPY", "KRW", "SYP", "AMD", "IQD"]

def get_currency_prices_selenium():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    url = "https://alanchand.com/currencies-price"
    driver.get(url)
    time.sleep(3) 

    now_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    result = {}
    rows = driver.find_elements(By.CSS_SELECTOR, "a.tableRow.data.arz_sync")

    for row in rows:
        slug = row.get_attribute("slug")
        if not slug or '-' in slug:
            continue

        try:
            buy_cell = row.find_element(By.CSS_SELECTOR, "div.cell.side.buy")
            buy_text = buy_cell.text.strip().split()[0].replace(",", "")
            buy_price = int(buy_text)
        except Exception:
            buy_price = None

        try:
            sell_cell = row.find_element(By.CSS_SELECTOR, "div.cell.side.sell")
            sell_text = sell_cell.text.strip().split()[0].replace(",", "")
            sell_price = int(sell_text)
        except Exception:
            sell_price = None

        slug_upper = slug.upper()
        if slug_upper in DIVIDE_100:
            if buy_price is not None:
                buy_price = buy_price / 100
            if sell_price is not None:
                sell_price = sell_price / 100

        result[slug_upper] = {
            "buy": buy_price,
            "sell": sell_price,
            "timestamp": now_utc
        }

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
