"""
Utility functions for keyboard generation and message formatting
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List
from datetime import datetime

def create_currency_keyboard(currencies: List[str], prefix: str = "") -> InlineKeyboardMarkup:
    """
    Create a keyboard with currencies arranged in rows of 3
    
    Args:
        currencies: List of currency codes
        prefix: Optional prefix for callback data (e.g., "to_")
    
    Returns:
        InlineKeyboardMarkup object
    """
    keyboard = []
    for i in range(0, len(currencies), 3):
        row = []
        for currency in currencies[i:i+3]:
            callback_data = f"{prefix}{currency}" if prefix else currency
            row.append(InlineKeyboardButton(currency, callback_data=callback_data))
        keyboard.append(row)
    
    return InlineKeyboardMarkup(keyboard)

def create_convert_again_keyboard() -> InlineKeyboardMarkup:
    """Create a keyboard with 'Convert Again' button"""
    keyboard = [[InlineKeyboardButton("🔄 Convert Again", callback_data="start_convert")]]
    return InlineKeyboardMarkup(keyboard)

def create_start_keyboard() -> InlineKeyboardMarkup:
    """Create a keyboard with 'Start Converting' button"""
    keyboard = [[InlineKeyboardButton("💱 Start Converting", callback_data="start_convert")]]
    return InlineKeyboardMarkup(keyboard)

def format_conversion_result(amount: float, from_currency: str, to_currency: str, 
                           result: str, conversion_rate: float, from_name: str, 
                           to_name: str) -> str:
    """
    Format the conversion result message
    
    Args:
        amount: Original amount
        from_currency: Source currency code
        to_currency: Target currency code
        result: Converted amount
        conversion_rate: Exchange rate
        from_name: Source currency full name
        to_name: Target currency full name
    
    Returns:
        Formatted message string
    """
    # Format conversion rate based on which currency is IRT
    if to_currency == "IRT":
        rate_text = f"1 {from_currency} = {conversion_rate:,.0f} {to_currency}"
    elif from_currency == "IRT":
        inverse_rate = 1 / conversion_rate if conversion_rate != 0 else 0
        rate_text = f"1 {to_currency} = {inverse_rate:,.0f} {from_currency}"
    else:
        rate_text = f"1 {from_currency} = {conversion_rate:,.4f} {to_currency}".rstrip('0').rstrip('.')
    
    current_date = datetime.now().strftime("%d/%m/%Y")
    
    return (
        f"✅ **Conversion Result**\n\n"
        f"💰 **{amount:,.10g} {from_name}**\n"
        f"🟰 **{result} {to_name}**\n\n"
        f"📊 **Rate:** {rate_text}\n"
        f"📅 **Date:** {current_date}\n\n"
        f"_Rate calculated using Bonbast & ExchangeRate API_"
    )

def validate_amount(amount_text: str) -> tuple[bool, float, str]:
    """
    Validate and parse amount input
    
    Args:
        amount_text: Input text to validate
    
    Returns:
        Tuple of (is_valid, parsed_amount, error_message)
    """
    try:
        amount = float(amount_text)
        if amount <= 0:
            return False, 0.0, "Please enter a positive number."
        return True, amount, ""
    except ValueError:
        return False, 0.0, "Please enter a valid number."

def create_currency_keyboard_with_default(currencies: List[str], user_id: int, prefix: str = "") -> InlineKeyboardMarkup:
    """
    Create a keyboard with currencies and default pair button if user has one
    
    Args:
        currencies: List of currency codes
        user_id: User ID to check for default pair
        prefix: Optional prefix for callback data (e.g., "to_")
    
    Returns:
        InlineKeyboardMarkup object
    """
    from src.utils.session import get_user_default_pair
    from src.utils.currency_converter import get_currency_name
    
    keyboard = []
    
    # Add default pair button if user has one and no prefix (FROM currency selection)
    if not prefix:
        default_pair = get_user_default_pair(user_id)
        if default_pair:
            from_currency = default_pair["from"]
            to_currency = default_pair["to"]
            from_name = get_currency_name(from_currency)
            to_name = get_currency_name(to_currency)
            
            # Create quick conversion button
            quick_button = InlineKeyboardButton(
                f"⚡ {from_currency} → {to_currency}",
                callback_data=f"quick_{from_currency}_{to_currency}"
            )
            keyboard.append([quick_button])
    
    # Add regular currency buttons in rows of 3
    for i in range(0, len(currencies), 3):
        row = []
        for currency in currencies[i:i+3]:
            callback_data = f"{prefix}{currency}" if prefix else currency
            row.append(InlineKeyboardButton(currency, callback_data=callback_data))
        keyboard.append(row)
    
    return InlineKeyboardMarkup(keyboard)
