#!/bin/bash

echo "🏦 Setting up What Da Nerkh Bot..."

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "🔧 To run the bot:"
echo "1. Set your TELEGRAM_BOT_TOKEN environment variable"
echo "2. Run: python bot.py"
echo ""
echo "💡 Example:"
echo "export TELEGRAM_BOT_TOKEN='your_bot_token_here'"
echo "python bot.py"
