# What Da Nerkh Bot (Open Source Free Tier)

A modular Telegram bot for real-time currency conversion with specialized support for Iranian Toman (IRT) and intelligent message processing capabilities.

## Features

- **Real-time Currency Conversion**: Supports 20+ major currencies with live exchange rates
- **Iranian Toman Support**: Accurate IRT rates via Bonbast integration
- **Global Currency Data**: International exchange rates via ExchangeRate API
- **Intelligent Message Processing**: LLM-powered natural language understanding via OpenRouter API
- **Persistent User Preferences**: Save default currency pairs for quick access
- **Multi-language Support**: Persian and English with advanced number parsing
- **Quick Conversion Shortcuts**: Send numbers for instant conversion using default pairs
- **Forwarded Message Processing**: Automatic currency detection in forwarded content
- **Interactive Interface**: Inline keyboard navigation
- **Production Ready**: Modular architecture with comprehensive error handling

## Architecture

```
nerkhbot/
├── bot.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── config/
│   ├── settings.py                # Configuration and message templates
│   └── storage.py                 # Data persistence configuration
├── src/
│   ├── handlers/
│   │   ├── commands.py           # Command handlers (/start, /convert, /help)
│   │   ├── callbacks.py          # Inline keyboard callback handlers
│   │   └── messages.py           # Text message processing
│   └── utils/
│       ├── bot_setup.py          # Bot initialization
│       ├── keyboards.py          # Interface generation
│       ├── session.py            # User session management
│       ├── llm_parser.py         # OpenRouter LLM integration
│       ├── currency_converter.py # Currency conversion logic
│       └── persistent_storage.py # User data persistence
└── data/
    └── user_defaults.json        # User preferences storage
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- OpenRouter API Key (optional, for LLM features)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/nerkhbot.git
   cd nerkhbot
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your credentials:
   ```bash
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here  # Optional
   ```

5. **Run the bot**
   ```bash
   python bot.py
   ```

## Configuration

### Required Configuration

- **TELEGRAM_BOT_TOKEN**: Obtain from [@BotFather](https://t.me/BotFather)

### Optional Configuration

- **OPENROUTER_API_KEY**: Register at [OpenRouter.ai](https://openrouter.ai/) for intelligent message processing
- **LOG_LEVEL**: Set logging verbosity (DEBUG, INFO, WARNING, ERROR)

### LLM Integration

The bot integrates with OpenRouter API to provide intelligent natural language processing for currency conversion requests. This enables users to send messages and receive automatic conversions.


## Usage

### Available Commands

- `/start` - Initialize bot and display welcome message
- `/convert` - Access currency conversion interface
- `/default` - Configure default currency pair
- `/help` - Display available features and commands

## Production Deployment

### Systemd Service

1. Create service file `/etc/systemd/system/nerkhbot.service`:
   ```ini
   [Unit]
   Description=What Da Nerkh Bot
   After=network.target
   
   [Service]
   Type=simple
   User=youruser
   WorkingDirectory=/path/to/nerkhbot
   Environment=PATH=/path/to/nerkhbot/venv/bin
   ExecStart=/path/to/nerkhbot/venv/bin/python bot.py
   Restart=always
   RestartSec=10
   
   [Install]
   WantedBy=multi-user.target
   ```

2. Enable and start service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable nerkhbot
   sudo systemctl start nerkhbot
   ```

3. Monitor service:
   ```bash
   sudo systemctl status nerkhbot
   journalctl -u nerkhbot -f
   ```

## Development

### Code Structure

- **Modular Design**: Clear separation of concerns across handlers and utilities
- **Asynchronous Operations**: Full async/await implementation for optimal performance
- **Type Safety**: Comprehensive type hints throughout codebase
- **Error Handling**: Robust exception management with user-friendly messages
- **Extensible Architecture**: Simple addition of new features and currencies

### Adding Features

- **Commands**: Extend `src/handlers/commands.py`
- **Callbacks**: Modify `src/handlers/callbacks.py`
- **Message Processing**: Update `src/handlers/messages.py`
- **Configuration**: Adjust `config/settings.py`
- **Utilities**: Add functionality to `src/utils/`

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [Bonbast.com](https://bonbast.com) - Iranian Toman exchange rates
- [ExchangeRate-API](https://exchangerate-api.com) - Global currency data
- [OpenRouter.ai](https://openrouter.ai) - LLM API services
