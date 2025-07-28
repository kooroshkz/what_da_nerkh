# What Da Nerkh Telegram Bot
### Free Open Source Tier

A Telegram bot for real-time currency conversion with special support for Iranian Toman (IRT) using Bonbast and EchangeRate-API.

## Architecture 🏗️

- `bot.py` - Main Telegram bot interface and user interaction
- `currency_converter.py` - Currency conversion logic and API handling

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

## Deploy and running in background

#### **1. Systemd service file location**

* **Path:** `/etc/systemd/system/whatdanerkhbot.service`

#### **2. Basic Commands**

| Action                      | Command                                 |
| --------------------------- | --------------------------------------- |
| **Start the bot**           | `sudo systemctl start whatdanerkhbot`   |
| **Stop the bot**            | `sudo systemctl stop whatdanerkhbot`    |
| **Restart (after updates)** | `sudo systemctl restart whatdanerkhbot` |
| **Check if running**        | `sudo systemctl status whatdanerkhbot`  |
| **Live logs (follow):**     | `journalctl -u whatdanerkhbot -f`       |
| **Full logs (scroll):**     | `journalctl -u whatdanerkhbot`          |

#### **3. After Editing Service File**

If you ever change the `.service` file:

```bash
sudo systemctl daemon-reexec
sudo systemctl restart whatdanerkhbot
```



## Commands 📋

- `/start` - Start currency conversion
- `/help` - Show help message

## Error Handling

- Network timeouts and connection errors
- Invalid currency pairs
- API failures with graceful fallbacks
- User input validation

## Contributing

Feel free to contribute by:
- Improving error handling
- Adding new features
- Fixing bugs
