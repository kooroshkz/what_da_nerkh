import json
import os
import sys

FILES = ["alanchand_live.json", "bonbast_live.json", "tgju_live.json"]

def validate_json(file_path):
    if not os.path.exists(file_path):
        print(f"ERROR: {file_path} is missing.")
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "updated_at" not in data or "currencies" not in data:
            print(f"ERROR: {file_path} missing 'updated_at' or 'currencies'.")
            return False

        currencies = data["currencies"]

        if len(currencies) < 3:
            print(f"ERROR: {file_path} has too few currencies.")
            return False

        for code, details in currencies.items():
            buy = details.get("buy")
            sell = details.get("sell")

            if not isinstance(buy, (int, float)) or buy <= 0:
                print(f"ERROR: {file_path}: {code} has invalid 'buy' = {buy}")
                return False

            if not isinstance(sell, (int, float)) or sell <= 0:
                print(f"ERROR: {file_path}: {code} has invalid 'sell' = {sell}")
                return False

        print(f"SUCCESS: {file_path} looks good.")
        return True

    except Exception as e:
        print(f"ERROR: Failed to read {file_path}: {e}")
        return False


def main():
    all_good = True
    for file in FILES:
        if not validate_json(file):
            all_good = False

    if not all_good:
        sys.exit(1)
    else:
        print("SUCCESS: All files validated successfully.")


if __name__ == "__main__":
    main()
