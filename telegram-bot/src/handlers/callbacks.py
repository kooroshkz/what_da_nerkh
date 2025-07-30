"""
Callback query handlers for currency conversion flow
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes

from config.settings import ERROR_NO_SESSION
from src.utils.keyboards import create_currency_keyboard, create_convert_again_keyboard, create_currency_keyboard_with_default
from src.utils.session import update_user_session, get_user_session
from src.utils.currency_converter import get_currency_name, get_currency_list

# Get currencies from converter module
CURRENCIES = get_currency_list()[:18]

async def start_convert_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle start_convert callback"""
    query = update.callback_query
    await query.answer()
    
    keyboard = create_currency_keyboard_with_default(CURRENCIES, query.from_user.id)
    
    await query.edit_message_text(
        "💱 Choose the currency you want to convert **FROM**:",
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

async def choose_currency_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle currency selection (FROM currency)"""
    query = update.callback_query
    await query.answer()
    
    # Check if user is setting default currencies
    session = get_user_session(query.from_user.id)
    if session and session.get("setting_default") == "from":
        # Handle default FROM currency selection
        await default_from_currency_callback(update, context)
        return
    
    # Normal conversion flow
    # Store user's FROM currency choice
    update_user_session(query.from_user.id, "from", query.data)
    
    # Create TO currency keyboard
    keyboard = create_currency_keyboard(CURRENCIES, "to_")
    
    from_name = get_currency_name(query.data)
    await query.edit_message_text(
        f"💰 **From currency:** {query.data} ({from_name})\n\n"
        f"💱 Now choose the currency you want to convert **TO**:",
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

async def choose_to_currency_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle TO currency selection"""
    query = update.callback_query
    await query.answer()

    # Check if this is for setting default TO currency
    if query.data.startswith("default_to_"):
        await default_to_currency_callback(update, context)
        return

    # Normal conversion flow
    to_currency = query.data.replace("to_", "")
    update_user_session(query.from_user.id, "to", to_currency)

    session = get_user_session(query.from_user.id)
    from_currency = session['from']
    from_name = get_currency_name(from_currency)
    to_name = get_currency_name(to_currency)
    
    await query.edit_message_text(
        f"💰 **From:** {from_currency} ({from_name})\n"
        f"💰 **To:** {to_currency} ({to_name})\n\n"
        f"💵 Please enter the amount to convert:",
        parse_mode='Markdown'
    )

async def quick_convert_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle quick conversion using default pair"""
    query = update.callback_query
    await query.answer()
    
    # Extract currencies from callback data (format: quick_FROM_TO)
    _, from_currency, to_currency = query.data.split('_')
    
    # Store the conversion pair in session
    update_user_session(query.from_user.id, "from", from_currency)
    update_user_session(query.from_user.id, "to", to_currency)
    
    from_name = get_currency_name(from_currency)
    to_name = get_currency_name(to_currency)
    
    await query.edit_message_text(
        f"⚡ **Quick Conversion**\n\n"
        f"💰 **From:** {from_currency} ({from_name})\n"
        f"💰 **To:** {to_currency} ({to_name})\n\n"
        f"💵 Please enter the amount to convert:",
        parse_mode='Markdown'
    )

async def default_from_currency_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle default FROM currency selection"""
    query = update.callback_query
    await query.answer()
    
    # Store the FROM currency for default setting
    update_user_session(query.from_user.id, "default_from", query.data)
    update_user_session(query.from_user.id, "setting_default", "to")
    
    # Show TO currency selection
    keyboard = create_currency_keyboard(CURRENCIES, "default_to_")
    
    from_name = get_currency_name(query.data)
    await query.edit_message_text(
        f"💰 **Default FROM currency:** {query.data} ({from_name})\n\n"
        f"💱 Now choose your **DEFAULT TO** currency:",
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

async def default_to_currency_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle default TO currency selection and save the pair"""
    query = update.callback_query
    await query.answer()
    
    to_currency = query.data.replace("default_to_", "")
    session = get_user_session(query.from_user.id)
    
    if session and "default_from" in session:
        from_currency = session["default_from"]
        
        # Save the default pair
        from src.utils.session import set_user_default_pair
        set_user_default_pair(query.from_user.id, from_currency, to_currency)
        
        # Clear temporary session data
        update_user_session(query.from_user.id, "default_from", None)
        update_user_session(query.from_user.id, "setting_default", None)
        
        from_name = get_currency_name(from_currency)
        to_name = get_currency_name(to_currency)
        
        from config.settings import DEFAULT_SET_SUCCESS
        
        keyboard = create_convert_again_keyboard()
        
        await query.edit_message_text(
            DEFAULT_SET_SUCCESS.format(
                from_currency=f"{from_currency} ({from_name})",
                to_currency=f"{to_currency} ({to_name})"
            ),
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
