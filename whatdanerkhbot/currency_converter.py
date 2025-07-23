import requests
import subprocess
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bonbast supported currencies
BONBAST_CURRENCIES = {
    "USD", "EUR", "GBP", "CHF", "CAD", "AUD", "SEK", "NOK", "RUB", 
    "THB", "SGD", "HKD", "AZN", "AMD", "DKK", "AED", "JPY", "TRY", 
    "CNY", "SAR", "INR", "MYR", "AFN", "KWD", "IQD", "BHD", "OMR", "QAR"
}

# Extended currency list for the bot
CURRENCIES = [
    {"code": "IRT", "name": "Iranian Toman (IRT)"},
    {"code": "USD", "name": "United States Dollar (USD)"},
    {"code": "EUR", "name": "Euro (EUR)"},
    {"code": "GBP", "name": "British Pound Sterling (GBP)"},
    {"code": "TRY", "name": "Turkish Lira (TRY)"},
    {"code": "AED", "name": "United Arab Emirates Dirham (AED)"},
    {"code": "CAD", "name": "Canadian Dollar (CAD)"},
    {"code": "AUD", "name": "Australian Dollar (AUD)"},
    {"code": "CHF", "name": "Swiss Franc (CHF)"},
    {"code": "JPY", "name": "Japanese Yen (JPY)"},
    {"code": "CNY", "name": "Chinese Yuan (CNY)"},
    {"code": "RUB", "name": "Russian Ruble (RUB)"},
    {"code": "SAR", "name": "Saudi Riyal (SAR)"},
    {"code": "INR", "name": "Indian Rupee (INR)"},
    {"code": "KWD", "name": "Kuwaiti Dinar (KWD)"},
    {"code": "QAR", "name": "Qatari Riyal (QAR)"},
    {"code": "OMR", "name": "Omani Rial (OMR)"},
    {"code": "BHD", "name": "Bahraini Dinar (BHD)"},
    {"code": "SEK", "name": "Swedish Krona (SEK)"},
    {"code": "NOK", "name": "Norwegian Krone (NOK)"},
]

def get_bonbast_rates():
    """Get live exchange rates from Bonbast for Iranian Toman"""
    try:
        # Run bonbast command and parse output
        process_result = subprocess.run(
            ["python", "-m", "bonbast", "export"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        
        # Parse the JSON output
        bonbast_data = json.loads(process_result.stdout.strip())
        
        # Process currency data and apply corrections
        processed_rates = {}
        
        for code, currency_data in bonbast_data.items():
            if code not in BONBAST_CURRENCIES:
                continue
                
            sell = currency_data.get('sell')
            buy = currency_data.get('buy')
            
            # Apply price corrections for certain currencies
            if code == "AMD":  # Armenian Dram (shown as "10 Armenian Dram")
                if sell: sell = sell / 10
                if buy: buy = buy / 10
            elif code == "JPY":  # Japanese Yen (shown as "10 Japanese Yen")
                if sell: sell = sell / 10
                if buy: buy = buy / 10
            elif code == "IQD":  # Iraqi Dinar (shown as "100 Iraqi Dinar")
                if sell: sell = sell / 100
                if buy: buy = buy / 100

            processed_rates[code] = {
                "buy": buy,
                "sell": sell,
                "name": currency_data.get('name', '')
            }
            
        logger.info(f"Successfully fetched Bonbast rates for {len(processed_rates)} currencies")
        return processed_rates
        
    except subprocess.TimeoutExpired:
        logger.error("Bonbast command timed out")
        return {}
    except subprocess.CalledProcessError as e:
        logger.error(f"Bonbast command failed: {e}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Bonbast JSON output: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error getting bonbast data: {e}")
        return {}

def get_bonbast_rate(from_code, to_code):
    """Get exchange rate between IRT and another currency using Bonbast"""
    bonbast_rates = get_bonbast_rates()
    
    if not bonbast_rates:
        return None
    
    if from_code == "IRT" and to_code in bonbast_rates:
        # IRT to other currency - use buy rate (what you get when selling IRT)
        buy_rate = bonbast_rates[to_code].get('buy')
        if buy_rate and buy_rate > 0:
            return 1 / buy_rate  # Convert IRT to foreign currency
    elif to_code == "IRT" and from_code in bonbast_rates:
        # Other currency to IRT - use sell rate (what you pay when buying foreign currency)
        sell_rate = bonbast_rates[from_code].get('sell')
        if sell_rate and sell_rate > 0:
            return sell_rate  # Convert foreign currency to IRT
    
    return None

def get_live_rate(base, target):
    """Fetch live rate from open.er-api.com"""
    url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("result") == "success":
            rate = data["rates"].get(target)
            if rate:
                logger.info(f"Fetched rate {base}->{target}: {rate}")
                return rate
    except requests.exceptions.Timeout:
        logger.error(f"Timeout fetching rate for {base}->{target}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error fetching rate for {base}->{target}: {e}")
    except Exception as e:
        logger.error(f"Error fetching rate for {base}->{target}: {e}")
    return None

def format_result(result, target_currency):
    """Format conversion result based on target currency"""
    if result is None:
        return None
    
    # Format based on target currency
    if target_currency == "IRT":
        # For IRT, show as whole numbers or with 2 decimals max
        return f"{result:,.0f}" if result == int(result) else f"{result:,.2f}"
    else:
        # For other currencies, show up to 4 decimals, removing trailing zeros
        return f"{result:,.4f}".rstrip('0').rstrip('.')

def convert_currency(amount, from_code, to_code):
    """
    Main conversion logic - prioritizes Bonbast for IRT conversions
    
    Args:
        amount (float): Amount to convert
        from_code (str): Source currency code
        to_code (str): Target currency code
    
    Returns:
        str: Formatted conversion result or None if conversion failed
    """
    
    if from_code == to_code:
        return format_result(amount, to_code)
    
    logger.info(f"Converting {amount} {from_code} to {to_code}")
    
    # Case 1: Direct IRT conversions using Bonbast
    if from_code == "IRT" or to_code == "IRT":
        bonbast_rate = get_bonbast_rate(from_code, to_code)
        if bonbast_rate:
            result = round(amount * bonbast_rate, 4)
            logger.info(f"Bonbast conversion successful: {amount} {from_code} = {result} {to_code}")
            return format_result(result, to_code)
        
        # Case 2: Fallback for IRT conversions via EUR
        logger.info("Direct Bonbast conversion failed, trying via EUR")
        
        if to_code == "IRT":
            # Convert from_code to EUR first, then EUR to IRT
            eur_rate = get_live_rate(from_code, "EUR")
            if eur_rate:
                eur_amount = amount * eur_rate
                irt_rate = get_bonbast_rate("EUR", "IRT")
                if irt_rate:
                    result = round(eur_amount * irt_rate, 4)
                    logger.info(f"EUR fallback conversion successful: {amount} {from_code} = {result} {to_code}")
                    return format_result(result, to_code)
                    
        elif from_code == "IRT":
            # Convert IRT to EUR first, then EUR to to_code
            eur_rate = get_bonbast_rate("IRT", "EUR")
            if eur_rate:
                eur_amount = amount * eur_rate
                target_rate = get_live_rate("EUR", to_code)
                if target_rate:
                    result = round(eur_amount * target_rate, 4)
                    logger.info(f"EUR fallback conversion successful: {amount} {from_code} = {result} {to_code}")
                    return format_result(result, to_code)
        
        # Case 3: USD fallback for IRT conversions
        logger.info("EUR fallback failed, trying via USD")
        
        if to_code == "IRT":
            # Convert from_code to USD first, then USD to IRT
            usd_rate = get_live_rate(from_code, "USD")
            if usd_rate:
                usd_amount = amount * usd_rate
                irt_rate = get_bonbast_rate("USD", "IRT")
                if irt_rate:
                    result = round(usd_amount * irt_rate, 4)
                    logger.info(f"USD fallback conversion successful: {amount} {from_code} = {result} {to_code}")
                    return format_result(result, to_code)
                    
        elif from_code == "IRT":
            # Convert IRT to USD first, then USD to to_code
            usd_rate = get_bonbast_rate("IRT", "USD")
            if usd_rate:
                usd_amount = amount * usd_rate
                target_rate = get_live_rate("USD", to_code)
                if target_rate:
                    result = round(usd_amount * target_rate, 4)
                    logger.info(f"USD fallback conversion successful: {amount} {from_code} = {result} {to_code}")
                    return format_result(result, to_code)
    
    # Case 4: Global pairs (non-IRT)
    rate = get_live_rate(from_code, to_code)
    if rate:
        result = round(amount * rate, 4)
        logger.info(f"Global conversion successful: {amount} {from_code} = {result} {to_code}")
        return format_result(result, to_code)
    
    logger.error(f"All conversion methods failed for {amount} {from_code} to {to_code}")
    return None

def get_currency_list():
    """Get the list of supported currencies"""
    return [currency["code"] for currency in CURRENCIES]

def get_currency_name(code):
    """Get the full name of a currency by its code"""
    for currency in CURRENCIES:
        if currency["code"] == code:
            return currency["name"]
    return code
