from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime, timezone
import json
import time
import os

SLUG_TO_CODE = {
    "price_dollar_rl": "USD",
    "price_eur": "EUR",
    "price_gbp": "GBP",
    "price_chf": "CHF",
    "price_cad": "CAD",
    "price_aud": "AUD",
    "price_sek": "SEK",
    "price_nok": "NOK",
    "price_rub": "RUB",
    "price_thb": "THB",
    "price_sgd": "SGD",
    "price_hkd": "HKD",
    "price_azn": "AZN",
    "price_amd": "AMD",
    "price_dkk": "DKK",
    "price_aed": "AED",
    "price_jpy": "JPY",
    "price_try": "TRY",
    "price_cny": "CNY",
    "price_sar": "SAR",
    "price_inr": "INR",
    "price_myr": "MYR",
    "price_afn": "AFN",
    "price_kwd": "KWD",
    "price_iqd": "IQD",
    "price_bhd": "BHD",
    "price_omr": "OMR",
    "price_qar": "QAR"
}

def parse_price(price_str, code):
    price = float(price_str.replace(',', '').replace('٬',''))
    price = price / 10
    if code == "JPY":
        price = price / 100
    return round(price, 2)

def get_tgju_rates():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.tgju.org/currency")
    time.sleep(2)

    result = {}
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')

    rows = driver.find_elements(By.CSS_SELECTOR, "table.data-table.market-table tbody tr")
    for row in rows:
        slug = row.get_attribute("data-market-nameslug")
        if slug not in SLUG_TO_CODE:
            continue
        code = SLUG_TO_CODE[slug]
        tds = row.find_elements(By.TAG_NAME, "td")
        if len(tds) < 2:
            continue
        price_str = tds[0].text.strip() if tds[0].text.strip() else row.get_attribute("data-price")
        if not price_str:
            continue
        price = parse_price(price_str, code)
        result[code] = {
            "buy": price,
            "sell": price,
            "timestamp": now
        }
    driver.quit()
    return {
        "updated_at": now,
        "currencies": result
    }

if __name__ == "__main__":
    data = get_tgju_rates()
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "price_data")

    with open(os.path.join(data_dir, "tgju_live.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    all_data = []
    historical_file = os.path.join(data_dir, "tgju_historical.json")
    if os.path.exists(historical_file):
        with open(historical_file, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except Exception:
                all_data = []
    all_data.append(data)
    with open(historical_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
