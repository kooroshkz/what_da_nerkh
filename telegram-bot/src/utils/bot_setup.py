"""
Bot setup and command registration utilities
"""
import logging
import os
from telegram import BotCommand
from telegram.ext import Application
from src.utils.llm_parser import get_llm_parser

def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

async def setup_bot_commands(app: Application) -> None:
    """Set up the bot commands menu that appears in chat input"""
    commands = [
        BotCommand("start", "Welcome message and bot info"),
        BotCommand("convert", "Start currency conversion"),
        BotCommand("default", "Set your default currency pair"),
        BotCommand("help", "Show help and features")
    ]
    await app.bot.set_my_commands(commands)

async def post_init(app: Application) -> None:
    """Called after the bot is initialized"""
    await setup_bot_commands(app)
    
    # Check LLM parser availability
    llm_parser = get_llm_parser()
    if llm_parser:
        # Test LLM API connectivity
        try:
            is_healthy = await llm_parser.is_healthy()
            if is_healthy:
                logging.info("✅ LLM parser ready - Smart message processing enabled")
            else:
                logging.warning("⚠️ LLM API not responding - Smart processing may be limited")
        except Exception as e:
            logging.warning(f"⚠️ LLM health check failed: {e}")
    else:
        logging.warning("⚠️ LLM parser not available - Missing OPENROUTER_API_KEY")
        logging.info("ℹ️ Bot will work in basic mode without smart message processing")
