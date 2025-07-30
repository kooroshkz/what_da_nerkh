"""
Configuration settings for the What Da Nerkh Bot
"""
import os
from typing import List

# Bot configuration
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# OpenRouter LLM API configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Currency configuration
MAX_CURRENCIES = 18

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# API configuration
BONBAST_URL = "https://www.bonbast.com/"
EXCHANGE_RATE_API_URL = "https://api.exchangerate-api.com/v4/latest/"

# Bot messages
WELCOME_MESSAGE = """🏦 **Welcome to What Da Nerkh Bot!**

💰 **Currency Converter with Real-time exchange rates**

📊 **Sources:**
• 🌍 ExchangeRate-API for global rates
• 🇮🇷 bonbast.com for Iranian Toman (IRT) rates

🚀 **Ready to convert?** Click the button below!"""

HELP_MESSAGE = """🏦 **What Da Nerkh Bot Help**

💱 **Commands:**
• `/start` - Welcome message with bot info
• `/convert` - Start currency conversion directly
• `/default` - Set your default currency pair for quick access
• `/help` - Show this help message

📊 **Features:**
• Real-time currency conversion
• Support for 18+ major currencies
• Special Iranian Toman (IRT) support via Bonbast
• Fallback to global exchange rates
• Quick conversion with default pairs ⚡

🔄 **How to use:**
1. Type `/start`
2. Choose source currency
3. Choose target currency
4. Enter amount to convert

💬 **Smart Message Processing:**
Send any message in Persian or English containing currency amounts and I'll automatically detect and convert them for you!

⚡ **Quick Conversion:**
1. Set your favorite pair with `/default`
2. Use `/convert` to see your quick conversion button
3. Click the ⚡ button for instant access to your default pair

� **Number Shortcut:**
Just send a number (like "45") and I'll convert it using your default pair, or EUR → IRT if not set!

�💰 **Supported currencies include:**
IRT, USD, EUR, GBP, TRY, AED, CAD, AUD, CHF, JPY, CNY, RUB, SAR, INR, KWD, QAR, OMR, BHD and more!

_For IRT conversions, we use Bonbast for the most accurate rates._"""

# Default pair messages
DEFAULT_HELP_MESSAGE = """🎯 **Set Your Default Currency Pair**

Choose your most frequently used currency conversion pair to get quick access!

After setting defaults, you'll see a quick conversion button at the top of the currency selection.

💡 **Example:** If you often convert EUR to IRT, set EUR as FROM and IRT as TO currency."""

DEFAULT_SET_SUCCESS = "✅ **Default pair saved!**\n\n🔄 Your quick conversion: **{from_currency}** → **{to_currency}**\n\nUse /convert to see your quick conversion button!"

DEFAULT_NOT_SET = "❌ You haven't set a default currency pair yet.\n\nUse /default to set one!"

# Error messages
ERROR_NETWORK = """❌ Could not fetch exchange rate. This might be due to:
• Network connectivity issues
• Currency pair not supported
• External API temporarily unavailable

Please try again later."""

ERROR_GENERAL = "❌ An error occurred during conversion. Please try again later."
ERROR_INVALID_NUMBER = "Please enter a valid number."
ERROR_POSITIVE_NUMBER = "Please enter a positive number."
ERROR_NO_SESSION = "Please start with /start first."

# Success messages
CONVERTING_MESSAGE = "🔄 Converting..."

# LLM parsing messages
LLM_PROCESSING_MESSAGE = "🤖 Analyzing your message..."
LLM_NO_CURRENCY_DETECTED = """🤔 I didn't detect any currency conversion request in your message.

💡 **Here's what I can help you with:**

**Commands:**
• `/start` - Start currency conversion
• `/convert` - Quick convert with your default pair
• `/default` - Set your default currency pair
• `/help` - Show help message

**Smart Messages:**
Just type something like:
• "100 dollars to toman"
• "صد دلار چند تومنه؟"
• "50 euros"

**Number Shortcut:**
Send just a number like "45" and I'll convert it using your default pair!

I'll automatically detect and convert currencies for you! 🚀"""

LLM_ERROR_MESSAGE = "❌ I couldn't process your message right now. Please try using `/convert` or `/help` for assistance."
