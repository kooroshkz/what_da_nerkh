#!/usr/bin/env python3
"""
What Da Nerkh Bot - Currency Converter Telegram Bot

A modern, modular Telegram bot for real-time currency conversion.
Supports Iranian Toman (IRT) via Bonbast and global currencies via ExchangeRate API.

Version: 2.0.0
"""

import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, 
    CallbackQueryHandler, filters
)

# Import configuration
from config.settings import TOKEN

# Import utilities
from src.utils.bot_setup import setup_logging, post_init

# Import handlers
from src.handlers.commands import start_command, convert_command, help_command, default_command
from src.handlers.callbacks import (
    start_convert_callback, choose_currency_callback, choose_to_currency_callback,
    quick_convert_callback
)
from src.handlers.messages import handle_general_message

def main() -> None:
    """Main function to run the What Da Nerkh Bot"""
    
    # Setup logging
    setup_logging()
    
    # Validate token
    if not TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN environment variable is not set!")
        print("Please set your bot token and try again.")
        sys.exit(1)
    
    # Build application
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("convert", convert_command))
    app.add_handler(CommandHandler("default", default_command))
    app.add_handler(CommandHandler("help", help_command))
    
    # Register callback query handlers
    app.add_handler(CallbackQueryHandler(start_convert_callback, pattern="^start_convert$"))
    app.add_handler(CallbackQueryHandler(quick_convert_callback, pattern="^quick_"))
    app.add_handler(CallbackQueryHandler(choose_currency_callback, pattern="^(?!to_|start_convert|quick_|default_to_).*"))
    app.add_handler(CallbackQueryHandler(choose_to_currency_callback, pattern="^(to_|default_to_)"))
    
    # Register message handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_general_message))

    # Start the bot
    print("🤖 What Da Nerkh Bot is starting...")
    print("📊 Currency conversion powered by Bonbast & global APIs")
    print("🧠 Smart message processing via OpenRouter LLM")
    print("🚀 Bot is ready and listening for messages!")
    
    try:
        app.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error running bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
