
from django.shortcuts import render
from django.http import JsonResponse
import requests

# Supported currencies
CURRENCIES = [
    {"code": "IRT", "name": "Iranian Toman"},
    {"code": "AED", "name": "AED"},
    {"code": "AFN", "name": "AFN"},
    {"code": "ALL", "name": "ALL"},
    {"code": "AMD", "name": "AMD"},
    {"code": "ANG", "name": "ANG"},
    {"code": "AOA", "name": "AOA"},
    {"code": "ARS", "name": "ARS"},
    {"code": "AUD", "name": "AUD"},
    {"code": "AWG", "name": "AWG"},
    {"code": "AZN", "name": "AZN"},
    {"code": "BAM", "name": "BAM"},
    {"code": "BBD", "name": "BBD"},
    {"code": "BDT", "name": "BDT"},
    {"code": "BGN", "name": "BGN"},
    {"code": "BHD", "name": "BHD"},
    {"code": "BIF", "name": "BIF"},
    {"code": "BMD", "name": "BMD"},
    {"code": "BND", "name": "BND"},
    {"code": "BOB", "name": "BOB"},
    {"code": "BRL", "name": "BRL"},
    {"code": "BSD", "name": "BSD"},
    {"code": "BTN", "name": "BTN"},
    {"code": "BWP", "name": "BWP"},
    {"code": "BYN", "name": "BYN"},
    {"code": "BZD", "name": "BZD"},
    {"code": "CAD", "name": "CAD"},
    {"code": "CDF", "name": "CDF"},
    {"code": "CHF", "name": "CHF"},
    {"code": "CLP", "name": "CLP"},
    {"code": "CNY", "name": "CNY"},
    {"code": "COP", "name": "COP"},
    {"code": "CRC", "name": "CRC"},
    {"code": "CUP", "name": "CUP"},
    {"code": "CVE", "name": "CVE"},
    {"code": "CZK", "name": "CZK"},
    {"code": "DJF", "name": "DJF"},
    {"code": "DKK", "name": "DKK"},
    {"code": "DOP", "name": "DOP"},
    {"code": "DZD", "name": "DZD"},
    {"code": "EGP", "name": "EGP"},
    {"code": "ERN", "name": "ERN"},
    {"code": "ETB", "name": "ETB"},
    {"code": "EUR", "name": "Euro"},
    {"code": "FJD", "name": "FJD"},
    {"code": "FKP", "name": "FKP"},
    {"code": "FOK", "name": "FOK"},
    {"code": "GBP", "name": "GBP"},
    {"code": "GEL", "name": "GEL"},
    {"code": "GGP", "name": "GGP"},
    {"code": "GHS", "name": "GHS"},
    {"code": "GIP", "name": "GIP"},
    {"code": "GMD", "name": "GMD"},
    {"code": "GNF", "name": "GNF"},
    {"code": "GTQ", "name": "GTQ"},
    {"code": "GYD", "name": "GYD"},
    {"code": "HKD", "name": "HKD"},
    {"code": "HNL", "name": "HNL"},
    {"code": "HRK", "name": "HRK"},
    {"code": "HTG", "name": "HTG"},
    {"code": "HUF", "name": "HUF"},
    {"code": "IDR", "name": "IDR"},
    {"code": "ILS", "name": "ILS"},
    {"code": "IMP", "name": "IMP"},
    {"code": "INR", "name": "INR"},
    {"code": "IQD", "name": "IQD"},
    {"code": "IRR", "name": "IRR"},
    {"code": "ISK", "name": "ISK"},
    {"code": "JEP", "name": "JEP"},
    {"code": "JMD", "name": "JMD"},
    {"code": "JOD", "name": "JOD"},
    {"code": "JPY", "name": "JPY"},
    {"code": "KES", "name": "KES"},
    {"code": "KGS", "name": "KGS"},
    {"code": "KHR", "name": "KHR"},
    {"code": "KID", "name": "KID"},
    {"code": "KMF", "name": "KMF"},
    {"code": "KRW", "name": "KRW"},
    {"code": "KWD", "name": "KWD"},
    {"code": "KYD", "name": "KYD"},
    {"code": "KZT", "name": "KZT"},
    {"code": "LAK", "name": "LAK"},
    {"code": "LBP", "name": "LBP"},
    {"code": "LKR", "name": "LKR"},
    {"code": "LRD", "name": "LRD"},
    {"code": "LSL", "name": "LSL"},
    {"code": "LYD", "name": "LYD"},
    {"code": "MAD", "name": "MAD"},
    {"code": "MDL", "name": "MDL"},
    {"code": "MGA", "name": "MGA"},
    {"code": "MKD", "name": "MKD"},
    {"code": "MMK", "name": "MMK"},
    {"code": "MNT", "name": "MNT"},
    {"code": "MOP", "name": "MOP"},
    {"code": "MRU", "name": "MRU"},
    {"code": "MUR", "name": "MUR"},
    {"code": "MVR", "name": "MVR"},
    {"code": "MWK", "name": "MWK"},
    {"code": "MXN", "name": "MXN"},
    {"code": "MYR", "name": "MYR"},
    {"code": "MZN", "name": "MZN"},
    {"code": "NAD", "name": "NAD"},
    {"code": "NGN", "name": "NGN"},
    {"code": "NIO", "name": "NIO"},
    {"code": "NOK", "name": "NOK"},
    {"code": "NPR", "name": "NPR"},
    {"code": "NZD", "name": "NZD"},
    {"code": "OMR", "name": "OMR"},
    {"code": "PAB", "name": "PAB"},
    {"code": "PEN", "name": "PEN"},
    {"code": "PGK", "name": "PGK"},
    {"code": "PHP", "name": "PHP"},
    {"code": "PKR", "name": "PKR"},
    {"code": "PLN", "name": "PLN"},
    {"code": "PYG", "name": "PYG"},
    {"code": "QAR", "name": "QAR"},
    {"code": "RON", "name": "RON"},
    {"code": "RSD", "name": "RSD"},
    {"code": "RUB", "name": "RUB"},
    {"code": "RWF", "name": "RWF"},
    {"code": "SAR", "name": "SAR"},
    {"code": "SBD", "name": "SBD"},
    {"code": "SCR", "name": "SCR"},
    {"code": "SDG", "name": "SDG"},
    {"code": "SEK", "name": "SEK"},
    {"code": "SGD", "name": "SGD"},
    {"code": "SHP", "name": "SHP"},
    {"code": "SLE", "name": "SLE"},
    {"code": "SLL", "name": "SLL"},
    {"code": "SOS", "name": "SOS"},
    {"code": "SRD", "name": "SRD"},
    {"code": "SSP", "name": "SSP"},
    {"code": "STN", "name": "STN"},
    {"code": "SYP", "name": "SYP"},
    {"code": "SZL", "name": "SZL"},
    {"code": "THB", "name": "THB"},
    {"code": "TJS", "name": "TJS"},
    {"code": "TMT", "name": "TMT"},
    {"code": "TND", "name": "TND"},
    {"code": "TOP", "name": "TOP"},
    {"code": "TRY", "name": "TRY"},
    {"code": "TTD", "name": "TTD"},
    {"code": "TVD", "name": "TVD"},
    {"code": "TWD", "name": "TWD"},
    {"code": "TZS", "name": "TZS"},
    {"code": "UAH", "name": "UAH"},
    {"code": "UGX", "name": "UGX"},
    {"code": "USD", "name": "US Dollar"},
    {"code": "UYU", "name": "UYU"},
    {"code": "UZS", "name": "UZS"},
    {"code": "VES", "name": "VES"},
    {"code": "VND", "name": "VND"},
    {"code": "VUV", "name": "VUV"},
    {"code": "WST", "name": "WST"},
    {"code": "XAF", "name": "XAF"},
    {"code": "XCD", "name": "XCD"},
    {"code": "XCG", "name": "XCG"},
    {"code": "XDR", "name": "XDR"},
    {"code": "XOF", "name": "XOF"},
    {"code": "XPF", "name": "XPF"},
    {"code": "YER", "name": "YER"},
    {"code": "ZAR", "name": "ZAR"},
    {"code": "ZMW", "name": "ZMW"},
    {"code": "ZWL", "name": "ZWL"},
]

# Fixed IRT rate
IRT_PER_EUR = 101290

def get_live_rate(base, target):
    """Fetch live rate from open.er-api.com"""
    url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if data.get("result") == "success":
            return data["rates"].get(target)
    except Exception:
        pass
    return None

def convert(amount, from_code, to_code):
    """Main conversion logic"""
    # IRT <-> EUR direct
    if (from_code == "IRT" and to_code == "EUR"):
        return round(amount / IRT_PER_EUR, 4)
    if (from_code == "EUR" and to_code == "IRT"):
        return round(amount * IRT_PER_EUR, 2)
    # IRT <-> other (via EUR/USD)
    if from_code == "IRT":
        eur_amount = amount / IRT_PER_EUR
        if to_code == "USD":
            rate = get_live_rate("EUR", "USD")
            if rate:
                return round(eur_amount * rate, 4)
        else:
            rate_eur_usd = get_live_rate("EUR", "USD")
            rate_usd_target = get_live_rate("USD", to_code)
            if rate_eur_usd and rate_usd_target:
                usd_amount = eur_amount * rate_eur_usd
                return round(usd_amount * rate_usd_target, 4)
    if to_code == "IRT":
        if from_code == "USD":
            rate = get_live_rate("EUR", "USD")
            if rate:
                eur_amount = amount / rate
                return round(eur_amount * IRT_PER_EUR, 2)
        else:
            rate_usd_from = get_live_rate("USD", from_code)
            rate_eur_usd = get_live_rate("EUR", "USD")
            if rate_usd_from and rate_eur_usd:
                usd_amount = amount / rate_usd_from
                eur_amount = usd_amount / rate_eur_usd
                return round(eur_amount * IRT_PER_EUR, 2)
    # Global pairs
    rate = get_live_rate(from_code, to_code)
    if rate:
        return round(amount * rate, 4)
    return None

def index(request):
    """Main page: default IRT->EUR"""
    context = {
        "currencies": CURRENCIES,
        "from_code": "IRT",
        "to_code": "EUR",
        "amount": 1,
        "result": convert(1, "IRT", "EUR"),
    }
    return render(request, "convertor/index.html", context)

def convert_api(request):
    """AJAX API for conversion"""
    from_code = request.GET.get("from", "IRT")
    to_code = request.GET.get("to", "EUR")
    try:
        amount = float(request.GET.get("amount", "1"))
    except ValueError:
        amount = 1
    result = convert(amount, from_code, to_code)
    return JsonResponse({"result": result})
