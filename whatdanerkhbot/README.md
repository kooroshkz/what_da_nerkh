# What Da Nerkh Bot 🏦

A Telegram bot for real-time currency conversion with special support for Iranian Toman (IRT) using Bonbast and global exchange APIs.

## Features 💫

- **Real-time currency conversion** for 18+ major currencies
- **Special IRT support** using Bonbast for accurate Iranian market rates
- **Hybrid fallback system** via EUR/USD when direct conversion unavailable
- **Clean and intuitive** inline keyboard interface
- **Error handling** with detailed user feedback
- **Formatted results** with proper decimal places and thousands separators

## Supported Currencies 💰

IRT, USD, EUR, GBP, TRY, AED, CAD, AUD, CHF, JPY, CNY, RUB, SAR, INR, KWD, QAR, OMR, BHD, SEK, NOK

## Architecture 🏗️

- `bot.py` - Main Telegram bot interface and user interaction
- `currency_converter.py` - Currency conversion logic and API handling
- Clean separation of concerns for maintainability

## Setup 🚀

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your bot token:**
   ```bash
   export TELEGRAM_BOT_TOKEN="your_bot_token_here"
   ```

3. **Run the bot:**
   ```bash
   python bot.py
   ```

Or use the setup script:
```bash
./setup.sh
```

## How It Works 🔄

### For IRT Conversions:
1. **Primary:** Direct conversion using Bonbast API
2. **Fallback 1:** Convert via EUR (source → EUR → IRT or IRT → EUR → target)
3. **Fallback 2:** Convert via USD (source → USD → IRT or IRT → USD → target)

### For Non-IRT Conversions:
- Uses open.er-api.com for global exchange rates

## Commands 📋

- `/start` - Start currency conversion
- `/help` - Show help message

## Dependencies 📦

- `python-telegram-bot` - Telegram Bot API wrapper
- `requests` - HTTP requests for exchange rate APIs
- `bonbast` - Iranian exchange rate data

## Error Handling 🛡️

- Network timeouts and connection errors
- Invalid currency pairs
- API failures with graceful fallbacks
- User input validation

## Contributing 🤝

Feel free to contribute by:
- Adding more currencies
- Improving error handling
- Adding new features
- Fixing bugs

## License 📄

This project is open source and available under the MIT License.
