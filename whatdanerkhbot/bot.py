import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Import our currency converter
from currency_converter import convert_currency, get_currency_list, get_currency_name

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Get currencies from our converter module
CURRENCIES = get_currency_list()[:18]  # Use first 18 currencies for the bot interface

user_data = {}

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create keyboard with 3 currencies per row
    keyboard = []
    for i in range(0, len(CURRENCIES), 3):
        row = [InlineKeyboardButton(c, callback_data=c) for c in CURRENCIES[i:i+3]]
        keyboard.append(row)
    
    await update.message.reply_text(
        "🏦 **Welcome to What Da Nerkh!**\n\n"
        "💱 Choose the currency you want to convert **FROM**:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def choose_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_data[query.from_user.id] = {"from": query.data}

    # Create keyboard with 3 currencies per row
    keyboard = []
    for i in range(0, len(CURRENCIES), 3):
        row = [InlineKeyboardButton(c, callback_data=f"to_{c}") for c in CURRENCIES[i:i+3]]
        keyboard.append(row)
    
    from_name = get_currency_name(query.data)
    await query.edit_message_text(
        f"💰 **From currency:** {query.data} ({from_name})\n\n"
        f"💱 Now choose the currency you want to convert **TO**:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def choose_to_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    to_currency = query.data.replace("to_", "")
    user_data[query.from_user.id]["to"] = to_currency

    from_currency = user_data[query.from_user.id]['from']
    from_name = get_currency_name(from_currency)
    to_name = get_currency_name(to_currency)
    
    await query.edit_message_text(
        f"💰 **From:** {from_currency} ({from_name})\n"
        f"💰 **To:** {to_currency} ({to_name})\n\n"
        f"💵 Please enter the amount to convert:",
        parse_mode='Markdown'
    )

async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_data or "to" not in user_data[user_id]:
        await update.message.reply_text("Please start with /start first.")
        return

    from_currency = user_data[user_id]["from"]
    to_currency = user_data[user_id]["to"]
    amount_text = update.message.text

    try:
        amount = float(amount_text)
        if amount <= 0:
            await update.message.reply_text("Please enter a positive number.")
            return
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
        return

    # Show "converting..." message
    converting_msg = await update.message.reply_text("🔄 Converting...")

    try:
        # Use our currency converter
        result = convert_currency(amount, from_currency, to_currency)
        
        if result:
            from_name = get_currency_name(from_currency)
            to_name = get_currency_name(to_currency)
            
            response_text = (
                f"✅ **Conversion Result**\n\n"
                f"💰 **{amount:,.10g} {from_currency}** = **{result} {to_currency}**\n\n"
                f"📊 From: {from_name}\n"
                f"📊 To: {to_name}\n\n"
                f"_Rate calculated using Bonbast & global exchange APIs_"
            )
            
            await converting_msg.edit_text(response_text, parse_mode='Markdown')
        else:
            await converting_msg.edit_text(
                "❌ Could not fetch exchange rate. This might be due to:\n"
                "• Network connectivity issues\n"
                "• Currency pair not supported\n"
                "• External API temporarily unavailable\n\n"
                "Please try again later."
            )
    except Exception as e:
        logging.error(f"Error in currency conversion: {e}")
        await converting_msg.edit_text(
            "❌ An error occurred during conversion. Please try again later."
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🏦 **What Da Nerkh Bot Help**\n\n"
        "💱 **Commands:**\n"
        "• `/start` - Start currency conversion\n"
        "• `/help` - Show this help message\n\n"
        "📊 **Features:**\n"
        "• Real-time currency conversion\n"
        "• Support for 18+ major currencies\n"
        "• Special Iranian Toman (IRT) support via Bonbast\n"
        "• Fallback to global exchange rates\n\n"
        "🔄 **How to use:**\n"
        "1. Type `/start`\n"
        "2. Choose source currency\n"
        "3. Choose target currency\n"
        "4. Enter amount to convert\n\n"
        "💰 **Supported currencies include:**\n"
        "IRT, USD, EUR, GBP, TRY, AED, CAD, AUD, CHF, JPY, CNY, RUB, SAR, INR, KWD, QAR, OMR, BHD and more!\n\n"
        "_For IRT conversions, we use Bonbast for the most accurate rates._"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(choose_currency, pattern="^(?!to_).*"))
    app.add_handler(CallbackQueryHandler(choose_to_currency, pattern="^to_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount))

    print("🤖 What Da Nerkh Bot is starting...")
    print("📊 Currency conversion powered by Bonbast & global APIs")
    app.run_polling()

if __name__ == "__main__":
    main()
