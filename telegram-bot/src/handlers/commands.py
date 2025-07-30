"""
Command handlers for the What Da Nerkh Bot
"""
from telegram import Update
from telegram.ext import ContextTypes

from config.settings import WELCOME_MESSAGE, HELP_MESSAGE
from src.utils.keyboards import create_start_keyboard, create_currency_keyboard, create_currency_keyboard_with_default
from src.utils.session import update_user_session
from src.utils.currency_converter import get_currency_list

# Get currencies from converter module
CURRENCIES = get_currency_list()[:18]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    keyboard = create_start_keyboard()
    
    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

async def convert_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /convert command"""
    keyboard = create_currency_keyboard_with_default(CURRENCIES, update.message.from_user.id)
    
    await update.message.reply_text(
        "💱 Choose the currency you want to convert **FROM**:",
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    await update.message.reply_text(HELP_MESSAGE, parse_mode='Markdown')

async def default_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /default command"""
    from config.settings import DEFAULT_HELP_MESSAGE
    
    keyboard = create_currency_keyboard(CURRENCIES)
    
    # Store that user is setting default FROM currency
    update_user_session(update.message.from_user.id, "setting_default", "from")
    
    await update.message.reply_text(
        f"{DEFAULT_HELP_MESSAGE}\n\n💱 Choose your **DEFAULT FROM** currency:",
        reply_markup=keyboard,
        parse_mode='Markdown'
    )
