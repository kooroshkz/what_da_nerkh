"""
Message handlers for text input processing
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes

from config.settings import (
    ERROR_NO_SESSION, ERROR_INVALID_NUMBER, ERROR_POSITIVE_NUMBER,
    CONVERTING_MESSAGE, ERROR_NETWORK, ERROR_GENERAL,
    LLM_PROCESSING_MESSAGE, LLM_NO_CURRENCY_DETECTED, LLM_ERROR_MESSAGE
)
from src.utils.keyboards import create_convert_again_keyboard
from src.utils.session import get_user_session, has_valid_session
from src.utils.keyboards import validate_amount, format_conversion_result
from src.utils.currency_converter import convert_currency_with_rate, get_currency_name
from src.utils.llm_parser import get_llm_parser
from src.utils.persistent_storage import get_user_default_pair

async def handle_amount_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle amount input from user"""
    user_id = update.message.from_user.id

    # Check if user has a valid session
    if not has_valid_session(user_id):
        await update.message.reply_text(ERROR_NO_SESSION)
        return

    session = get_user_session(user_id)
    from_currency = session["from"]
    to_currency = session["to"]
    amount_text = update.message.text

    # Validate amount input
    is_valid, amount, error_msg = validate_amount(amount_text)
    if not is_valid:
        await update.message.reply_text(error_msg)
        return

    # Show converting message
    converting_msg = await update.message.reply_text(CONVERTING_MESSAGE)

    try:
        # Perform currency conversion
        result, conversion_rate = convert_currency_with_rate(amount, from_currency, to_currency)
        
        if result and conversion_rate:
            from_name = get_currency_name(from_currency)
            to_name = get_currency_name(to_currency)
            
            response_text = format_conversion_result(
                amount, from_currency, to_currency, result, 
                conversion_rate, from_name, to_name
            )
            
            keyboard = create_convert_again_keyboard()
            
            await converting_msg.edit_text(
                response_text, 
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        else:
            keyboard = create_convert_again_keyboard()
            
            await converting_msg.edit_text(
                ERROR_NETWORK,
                reply_markup=keyboard
            )
    except Exception as e:
        logging.error(f"Error in currency conversion: {e}")
        keyboard = create_convert_again_keyboard()
        
        await converting_msg.edit_text(
            ERROR_GENERAL,
            reply_markup=keyboard
        )


async def handle_general_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle general text messages with smart processing.
    
    Processing priority:
    1. Check if user has an active session for amount input
    2. Check if message is a simple number for default pair conversion
    3. Try LLM analysis for natural language currency detection
    4. Show help message if no intent detected
    """
    user_id = update.message.from_user.id
    message_text = update.message.text.strip()

    # Skip commands (they're handled separately)
    if message_text.startswith('/'):
        return

    # Handle forwarded messages - always pass to LLM
    if update.message.forward_origin:
        await handle_llm_processing(update, context, force_llm=True)
        return

    # Priority 1: Check if user has an active session for amount input
    if has_valid_session(user_id):
        is_valid, amount, error_msg = validate_amount(message_text)
        if is_valid:
            await handle_amount_message(update, context)
            return

    # Priority 2: Check if message is a simple number without active session
    is_valid, amount, error_msg = validate_amount(message_text)
    if is_valid:
        # Get user's default pair or use EUR → IRT as fallback
        default_pair = get_user_default_pair(user_id)
        if default_pair:
            from_currency = default_pair["from"]
            to_currency = default_pair["to"]
            conversion_note = f"_Using your default pair: {from_currency} → {to_currency}_"
        else:
            from_currency = "EUR"
            to_currency = "IRT"
            conversion_note = f"_Default conversion: {from_currency} → {to_currency}_\n💡 _Set your preferred pair with /default_"
        
        logging.info(f"Number conversion triggered - User: {user_id}, Amount: {amount} {from_currency} → {to_currency}")
        
        converting_msg = await update.message.reply_text("🔄 Converting...")
        
        try:
            result, conversion_rate = convert_currency_with_rate(amount, from_currency, to_currency)
            
            if result and conversion_rate:
                from_name = get_currency_name(from_currency)
                to_name = get_currency_name(to_currency)
                
                response_text = format_conversion_result(
                    amount, from_currency, to_currency, result, 
                    conversion_rate, from_name, to_name
                )
                
                # Add note about conversion type
                response_text += f"\n\n💡 {conversion_note}"
                
                keyboard = create_convert_again_keyboard()
                
                await converting_msg.edit_text(
                    response_text,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
                return
            else:
                keyboard = create_convert_again_keyboard()
                await converting_msg.edit_text(
                    ERROR_NETWORK,
                    reply_markup=keyboard
                )
                return
                
        except Exception as e:
            logging.error(f"Error in number conversion: {e}")
            keyboard = create_convert_again_keyboard()
            await converting_msg.edit_text(
                ERROR_GENERAL,
                reply_markup=keyboard
            )
            return

    # Priority 3: Try LLM processing for non-numeric messages
    await handle_llm_processing(update, context, force_llm=False)


async def handle_llm_processing(update: Update, context: ContextTypes.DEFAULT_TYPE, force_llm: bool = False) -> None:
    """Handle LLM-based message processing"""
    user_id = update.message.from_user.id
    message_text = update.message.text.strip()
    
    # Try LLM processing if available
    llm_parser = get_llm_parser()
    if llm_parser:
        try:
            processing_msg = await update.message.reply_text(LLM_PROCESSING_MESSAGE)
            
            # Parse the message using LLM
            intent = await llm_parser.parse_message(message_text)
            
            # Check if currency conversion intent was detected with good confidence
            if intent.is_currency_exchange and intent.amount and intent.from_currency and intent.confidence > 0.6:
                # Set default target currency to IRT if not specified
                to_currency = intent.to_currency or "IRT"
                
                # Log the detection for monitoring
                logging.info(
                    f"LLM detected currency intent - User: {user_id}, "
                    f"Amount: {intent.amount}, From: {intent.from_currency}, "
                    f"To: {to_currency}, Confidence: {intent.confidence}"
                )
                
                # Perform the currency conversion
                await processing_msg.edit_text("🔄 Converting...")
                
                try:
                    result, conversion_rate = convert_currency_with_rate(
                        intent.amount, intent.from_currency, to_currency
                    )
                    
                    if result and conversion_rate:
                        from_name = get_currency_name(intent.from_currency)
                        to_name = get_currency_name(to_currency)
                        
                        response_text = format_conversion_result(
                            intent.amount, intent.from_currency, to_currency,
                            result, conversion_rate, from_name, to_name
                        )
                        
                        # Add a note that this was auto-detected
                        response_text += f"\n\n🤖 _Auto-detected from your message_"
                        
                        keyboard = create_convert_again_keyboard()
                        
                        await processing_msg.edit_text(
                            response_text,
                            reply_markup=keyboard,
                            parse_mode='Markdown'
                        )
                        return  # Successfully processed by LLM
                    else:
                        keyboard = create_convert_again_keyboard()
                        await processing_msg.edit_text(
                            ERROR_NETWORK,
                            reply_markup=keyboard
                        )
                        return
                        
                except Exception as e:
                    logging.error(f"Error in LLM-triggered conversion: {e}")
                    keyboard = create_convert_again_keyboard()
                    await processing_msg.edit_text(
                        ERROR_GENERAL,
                        reply_markup=keyboard
                    )
                    return
            else:
                # LLM didn't detect strong currency intent, remove processing message
                await processing_msg.delete()
                
        except Exception as e:
            logging.error(f"Error in LLM message processing: {e}")
            await processing_msg.delete()

    # No currency intent detected - show help
    if llm_parser:
        logging.info(
            f"LLM detected no currency intent - User: {user_id}, "
            f"Message: {message_text[:50]}..."
        )
    await update.message.reply_text(LLM_NO_CURRENCY_DETECTED, parse_mode='Markdown')
