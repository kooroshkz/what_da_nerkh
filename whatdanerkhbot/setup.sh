#!/bin/bash

echo "Setting up What Da Nerkh Bot..."
echo "Installing dependencies..."
pip install -r requirements.txt
read -p "Enter your Telegram Bot Token: " TELEGRAM_BOT_TOKEN
echo "export TELEGRAM_BOT_TOKEN=\"$TELEGRAM_BOT_TOKEN\"" >> ~/.bashrc
export TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN"
echo "Starting bot.py..."
python bot.py