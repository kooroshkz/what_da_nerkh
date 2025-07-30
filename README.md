# What Da Nerkh

Currency conversion platform specializing in Iranian Toman (IRT) exchange rates with live data collection and multiple interface options.

## Features

### Web Converter
- **Static Web Interface**: Simple Euro to Toman converter (`index.html`)
- **Django Web Application**: Full-featured web converter supporting multiple currencies
- Real-time exchange rate conversion with user-friendly interface

### Telegram Bot
Modern Telegram bot providing:
- Real-time currency conversion
- Support for Iranian Toman via Bonbast
- Global currency support via ExchangeRate API
- Persistent user preferences and settings
- Interactive keyboard navigation

### Data Collection System
Automated price scrapers for continuous data collection:
- **Bonbast**: Iranian currency exchange rates
- **TGJU**: Tehran Gold and Jewelry Union rates  
- **Alanchand**: Additional exchange rate source

### Live Datasets
Continuously updated JSON datasets containing:
- Historical exchange rate data
- Live pricing information
- Data validation and integrity checks
- Structured storage for multiple currency sources

## Repository Structure

```
├── index.html              # Static web converter
├── Django-WebApp/          # Full Django application
├── telegram-bot/           # Telegram bot implementation
├── price_scrapers/         # Data collection modules
└── price_data/            # Live datasets and validation
```

## License

This project provides currency conversion services for informational purposes. Exchange rates are sourced from public APIs and financial websites.