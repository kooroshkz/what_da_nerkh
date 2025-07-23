#!/usr/bin/env python3
"""
Test script for currency converter functionality
"""

from currency_converter import convert_currency, get_currency_list, get_currency_name

def test_currency_converter():
    print("🧪 Testing Currency Converter...")
    print("=" * 50)
    
    # Test 1: USD to EUR (global conversion)
    print("\n📊 Test 1: USD to EUR")
    result = convert_currency(100, "USD", "EUR")
    print(f"100 USD = {result} EUR")
    
    # Test 2: EUR to IRT (Bonbast conversion)
    print("\n📊 Test 2: EUR to IRT")
    result = convert_currency(1, "EUR", "IRT")
    print(f"1 EUR = {result} IRT")
    
    # Test 3: IRT to USD (Bonbast conversion)
    print("\n📊 Test 3: IRT to USD")
    result = convert_currency(100000, "IRT", "USD")
    print(f"100,000 IRT = {result} USD")
    
    # Test 4: Same currency
    print("\n📊 Test 4: Same currency")
    result = convert_currency(100, "USD", "USD")
    print(f"100 USD = {result} USD")
    
    # Test 5: Invalid conversion
    print("\n📊 Test 5: TRY to GBP")
    result = convert_currency(100, "TRY", "GBP")
    print(f"100 TRY = {result} GBP")
    
    # Test currency list
    print("\n📋 Supported currencies:")
    currencies = get_currency_list()
    print(f"Total: {len(currencies)} currencies")
    print(currencies[:10], "...")
    
    # Test currency names
    print("\n🏷️ Currency names:")
    for code in ["USD", "EUR", "IRT", "GBP"]:
        name = get_currency_name(code)
        print(f"{code}: {name}")
    
    print("\n✅ Testing complete!")

if __name__ == "__main__":
    test_currency_converter()
