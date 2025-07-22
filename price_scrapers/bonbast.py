import json
from datetime import datetime, timezone
import os
import subprocess
import ast

def get_currencies_bonbast():
    now_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    result = {}

    try:
        # Run bonbast command and parse output
        process_result = subprocess.run(
            ["python", "-m", "bonbast", "export"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the Python dictionary output (not JSON)
        bonbast_data = ast.literal_eval(process_result.stdout.strip())
        
        # Process only currency data (skip coins and gold)
        currency_codes = {
            "USD", "EUR", "GBP", "CHF", "CAD", "AUD", "SEK", "NOK", "RUB", 
            "THB", "SGD", "HKD", "AZN", "AMD", "DKK", "AED", "JPY", "TRY", 
            "CNY", "SAR", "INR", "MYR", "AFN", "KWD", "IQD", "BHD", "OMR", "QAR"
        }
        
        for code, currency_data in bonbast_data.items():
            if code not in currency_codes:
                continue
                
            name = currency_data.get('name', '')
            sell = currency_data.get('sell')
            buy = currency_data.get('buy')
            
            # Apply price corrections based on currency
            # The library already shows "10 Armenian Dram", "10 Japanese Yen", "100 Iraqi Dinar"
            # So we need to divide by those amounts to get the actual per-unit rates
            if code == "AMD":  # Armenian Dram (shown as "10 Armenian Dram")
                if sell: sell = sell / 10
                if buy: buy = buy / 10
                name = "Armenian Dram"  # Clean up the name
            elif code == "JPY":  # Japanese Yen (shown as "10 Japanese Yen")
                if sell: sell = sell / 10
                if buy: buy = buy / 10
                name = "Japanese Yen"  # Clean up the name
            elif code == "IQD":  # Iraqi Dinar (shown as "100 Iraqi Dinar")
                if sell: sell = sell / 100
                if buy: buy = buy / 100
                name = "Iraqi Dinar"  # Clean up the name

            result[code] = {
                "buy": buy,
                "sell": sell,
                "timestamp": now_utc
            }
            
    except Exception as e:
        print(f"Error getting bonbast data: {e}")
        return {
            "updated_at": now_utc,
            "currencies": {}
        }

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
