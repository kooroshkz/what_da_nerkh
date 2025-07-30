
from django.shortcuts import render
from django.http import JsonResponse
import requests

CURRENCIES = [
    {"code": "IRT", "name": "Iranian Toman (IRT)"},
    {"code": "AED", "name": "United Arab Emirates Dirham (AED)"},
    {"code": "AFN", "name": "Afghan Afghani (AFN)"},
    {"code": "ALL", "name": "Albanian Lek (ALL)"},
    {"code": "AMD", "name": "Armenian Dram (AMD)"},
    {"code": "ANG", "name": "Netherlands Antillean Guilder (ANG)"},
    {"code": "AOA", "name": "Angolan Kwanza (AOA)"},
    {"code": "ARS", "name": "Argentine Peso (ARS)"},
    {"code": "AUD", "name": "Australian Dollar (AUD)"},
    {"code": "AWG", "name": "Aruban Florin (AWG)"},
    {"code": "AZN", "name": "Azerbaijani Manat (AZN)"},
    {"code": "BAM", "name": "Bosnia-Herzegovina Convertible Mark (BAM)"},
    {"code": "BBD", "name": "Barbadian Dollar (BBD)"},
    {"code": "BDT", "name": "Bangladeshi Taka (BDT)"},
    {"code": "BGN", "name": "Bulgarian Lev (BGN)"},
    {"code": "BHD", "name": "Bahraini Dinar (BHD)"},
    {"code": "BIF", "name": "Burundian Franc (BIF)"},
    {"code": "BMD", "name": "Bermudian Dollar (BMD)"},
    {"code": "BND", "name": "Brunei Dollar (BND)"},
    {"code": "BOB", "name": "Bolivian Boliviano (BOB)"},
    {"code": "BRL", "name": "Brazilian Real (BRL)"},
    {"code": "BSD", "name": "Bahamian Dollar (BSD)"},
    {"code": "BTN", "name": "Bhutanese Ngultrum (BTN)"},
    {"code": "BWP", "name": "Botswana Pula (BWP)"},
    {"code": "BYN", "name": "Belarusian Ruble (BYN)"},
    {"code": "BZD", "name": "Belize Dollar (BZD)"},
    {"code": "CAD", "name": "Canadian Dollar (CAD)"},
    {"code": "CDF", "name": "Congolese Franc (CDF)"},
    {"code": "CHF", "name": "Swiss Franc (CHF)"},
    {"code": "CLP", "name": "Chilean Peso (CLP)"},
    {"code": "CNY", "name": "Chinese Yuan (CNY)"},
    {"code": "COP", "name": "Colombian Peso (COP)"},
    {"code": "CRC", "name": "Costa Rican Colon (CRC)"},
    {"code": "CUP", "name": "Cuban Peso (CUP)"},
    {"code": "CVE", "name": "Cape Verdean Escudo (CVE)"},
    {"code": "CZK", "name": "Czech Koruna (CZK)"},
    {"code": "DJF", "name": "Djiboutian Franc (DJF)"},
    {"code": "DKK", "name": "Danish Krone (DKK)"},
    {"code": "DOP", "name": "Dominican Peso (DOP)"},
    {"code": "DZD", "name": "Algerian Dinar (DZD)"},
    {"code": "EGP", "name": "Egyptian Pound (EGP)"},
    {"code": "ERN", "name": "Eritrean Nakfa (ERN)"},
    {"code": "ETB", "name": "Ethiopian Birr (ETB)"},
    {"code": "EUR", "name": "Euro (EUR)"},
    {"code": "FJD", "name": "Fijian Dollar (FJD)"},
    {"code": "FKP", "name": "Falkland Islands Pound (FKP)"},
    {"code": "FOK", "name": "Faroese Króna (FOK)"},
    {"code": "GBP", "name": "British Pound Sterling (GBP)"},
    {"code": "GEL", "name": "Georgian Lari (GEL)"},
    {"code": "GGP", "name": "Guernsey Pound (GGP)"},
    {"code": "GHS", "name": "Ghanaian Cedi (GHS)"},
    {"code": "GIP", "name": "Gibraltar Pound (GIP)"},
    {"code": "GMD", "name": "Gambian Dalasi (GMD)"},
    {"code": "GNF", "name": "Guinean Franc (GNF)"},
    {"code": "GTQ", "name": "Guatemalan Quetzal (GTQ)"},
    {"code": "GYD", "name": "Guyanese Dollar (GYD)"},
    {"code": "HKD", "name": "Hong Kong Dollar (HKD)"},
    {"code": "HNL", "name": "Honduran Lempira (HNL)"},
    {"code": "HRK", "name": "Croatian Kuna (HRK)"},
    {"code": "HTG", "name": "Haitian Gourde (HTG)"},
    {"code": "HUF", "name": "Hungarian Forint (HUF)"},
    {"code": "IDR", "name": "Indonesian Rupiah (IDR)"},
    {"code": "ILS", "name": "Israeli New Shekel (ILS)"},
    {"code": "IMP", "name": "Isle of Man Pound (IMP)"},
    {"code": "INR", "name": "Indian Rupee (INR)"},
    {"code": "IQD", "name": "Iraqi Dinar (IQD)"},
    {"code": "IRR", "name": "Iranian Rial (IRR)"},
    {"code": "ISK", "name": "Icelandic Krona (ISK)"},
    {"code": "JEP", "name": "Jersey Pound (JEP)"},
    {"code": "JMD", "name": "Jamaican Dollar (JMD)"},
    {"code": "JOD", "name": "Jordanian Dinar (JOD)"},
    {"code": "JPY", "name": "Japanese Yen (JPY)"},
    {"code": "KES", "name": "Kenyan Shilling (KES)"},
    {"code": "KGS", "name": "Kyrgyzstani Som (KGS)"},
    {"code": "KHR", "name": "Cambodian Riel (KHR)"},
    {"code": "KID", "name": "Kiribati Dollar (KID)"},
    {"code": "KMF", "name": "Comorian Franc (KMF)"},
    {"code": "KRW", "name": "South Korean Won (KRW)"},
    {"code": "KWD", "name": "Kuwaiti Dinar (KWD)"},
    {"code": "KYD", "name": "Cayman Islands Dollar (KYD)"},
    {"code": "KZT", "name": "Kazakhstani Tenge (KZT)"},
    {"code": "LAK", "name": "Lao Kip (LAK)"},
    {"code": "LBP", "name": "Lebanese Pound (LBP)"},
    {"code": "LKR", "name": "Sri Lankan Rupee (LKR)"},
    {"code": "LRD", "name": "Liberian Dollar (LRD)"},
    {"code": "LSL", "name": "Lesotho Loti (LSL)"},
    {"code": "LYD", "name": "Libyan Dinar (LYD)"},
    {"code": "MAD", "name": "Moroccan Dirham (MAD)"},
    {"code": "MDL", "name": "Moldovan Leu (MDL)"},
    {"code": "MGA", "name": "Malagasy Ariary (MGA)"},
    {"code": "MKD", "name": "Macedonian Denar (MKD)"},
    {"code": "MMK", "name": "Myanmar Kyat (MMK)"},
    {"code": "MNT", "name": "Mongolian Tögrög (MNT)"},
    {"code": "MOP", "name": "Macanese Pataca (MOP)"},
    {"code": "MRU", "name": "Mauritanian Ouguiya (MRU)"},
    {"code": "MUR", "name": "Mauritian Rupee (MUR)"},
    {"code": "MVR", "name": "Maldivian Rufiyaa (MVR)"},
    {"code": "MWK", "name": "Malawian Kwacha (MWK)"},
    {"code": "MXN", "name": "Mexican Peso (MXN)"},
    {"code": "MYR", "name": "Malaysian Ringgit (MYR)"},
    {"code": "MZN", "name": "Mozambican Metical (MZN)"},
    {"code": "NAD", "name": "Namibian Dollar (NAD)"},
    {"code": "NGN", "name": "Nigerian Naira (NGN)"},
    {"code": "NIO", "name": "Nicaraguan Córdoba (NIO)"},
    {"code": "NOK", "name": "Norwegian Krone (NOK)"},
    {"code": "NPR", "name": "Nepalese Rupee (NPR)"},
    {"code": "NZD", "name": "New Zealand Dollar (NZD)"},
    {"code": "OMR", "name": "Omani Rial (OMR)"},
    {"code": "PAB", "name": "Panamanian Balboa (PAB)"},
    {"code": "PEN", "name": "Peruvian Sol (PEN)"},
    {"code": "PGK", "name": "Papua New Guinean Kina (PGK)"},
    {"code": "PHP", "name": "Philippine Peso (PHP)"},
    {"code": "PKR", "name": "Pakistani Rupee (PKR)"},
    {"code": "PLN", "name": "Polish Zloty (PLN)"},
    {"code": "PYG", "name": "Paraguayan Guarani (PYG)"},
    {"code": "QAR", "name": "Qatari Riyal (QAR)"},
    {"code": "RON", "name": "Romanian Leu (RON)"},
    {"code": "RSD", "name": "Serbian Dinar (RSD)"},
    {"code": "RUB", "name": "Russian Ruble (RUB)"},
    {"code": "RWF", "name": "Rwandan Franc (RWF)"},
    {"code": "SAR", "name": "Saudi Riyal (SAR)"},
    {"code": "SBD", "name": "Solomon Islands Dollar (SBD)"},
    {"code": "SCR", "name": "Seychellois Rupee (SCR)"},
    {"code": "SDG", "name": "Sudanese Pound (SDG)"},
    {"code": "SEK", "name": "Swedish Krona (SEK)"},
    {"code": "SGD", "name": "Singapore Dollar (SGD)"},
    {"code": "SHP", "name": "Saint Helena Pound (SHP)"},
    {"code": "SLE", "name": "Sierra Leonean Leone (SLE)"},
    {"code": "SLL", "name": "Sierra Leonean Leone (SLL)"},
    {"code": "SOS", "name": "Somali Shilling (SOS)"},
    {"code": "SRD", "name": "Surinamese Dollar (SRD)"},
    {"code": "SSP", "name": "South Sudanese Pound (SSP)"},
    {"code": "STN", "name": "São Tomé and Príncipe Dobra (STN)"},
    {"code": "SYP", "name": "Syrian Pound (SYP)"},
    {"code": "SZL", "name": "Swazi Lilangeni (SZL)"},
    {"code": "THB", "name": "Thai Baht (THB)"},
    {"code": "TJS", "name": "Tajikistani Somoni (TJS)"},
    {"code": "TMT", "name": "Turkmenistani Manat (TMT)"},
    {"code": "TND", "name": "Tunisian Dinar (TND)"},
    {"code": "TOP", "name": "Tongan Paʻanga (TOP)"},
    {"code": "TRY", "name": "Turkish Lira (TRY)"},
    {"code": "TTD", "name": "Trinidad and Tobago Dollar (TTD)"},
    {"code": "TVD", "name": "Tuvaluan Dollar (TVD)"},
    {"code": "TWD", "name": "New Taiwan Dollar (TWD)"},
    {"code": "TZS", "name": "Tanzanian Shilling (TZS)"},
    {"code": "UAH", "name": "Ukrainian Hryvnia (UAH)"},
    {"code": "UGX", "name": "Ugandan Shilling (UGX)"},
    {"code": "USD", "name": "United States Dollar (USD)"},
    {"code": "UYU", "name": "Uruguayan Peso (UYU)"},
    {"code": "UZS", "name": "Uzbekistani Som (UZS)"},
    {"code": "VES", "name": "Venezuelan Bolívar (VES)"},
    {"code": "VND", "name": "Vietnamese Dong (VND)"},
    {"code": "VUV", "name": "Vanuatu Vatu (VUV)"},
    {"code": "WST", "name": "Samoan Tala (WST)"},
    {"code": "XAF", "name": "Central African CFA Franc (XAF)"},
    {"code": "XCD", "name": "East Caribbean Dollar (XCD)"},
    {"code": "XCG", "name": "International Code (XCG)"},
    {"code": "XDR", "name": "Special Drawing Rights (XDR)"},
    {"code": "XOF", "name": "West African CFA Franc (XOF)"},
    {"code": "XPF", "name": "CFP Franc (XPF)"},
    {"code": "YER", "name": "Yemeni Rial (YER)"},
    {"code": "ZAR", "name": "South African Rand (ZAR)"},
    {"code": "ZMW", "name": "Zambian Kwacha (ZMW)"},
    {"code": "ZWL", "name": "Zimbabwean Dollar (ZWL)"},
]


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
        result = round(amount / IRT_PER_EUR, 4)
        return f"{result:,.4f}".rstrip('0').rstrip('.')
    if (from_code == "EUR" and to_code == "IRT"):
        result = round(amount * IRT_PER_EUR, 2)
        return f"{result:,.0f}" if result == int(result) else f"{result:,.2f}"
    # IRT <-> other (via EUR/USD)
    if from_code == "IRT":
        eur_amount = amount / IRT_PER_EUR
        if to_code == "USD":
            rate = get_live_rate("EUR", "USD")
            if rate:
                result = round(eur_amount * rate, 4)
                return f"{result:,.4f}".rstrip('0').rstrip('.')
        else:
            rate_eur_usd = get_live_rate("EUR", "USD")
            rate_usd_target = get_live_rate("USD", to_code)
            if rate_eur_usd and rate_usd_target:
                usd_amount = eur_amount * rate_eur_usd
                result = round(usd_amount * rate_usd_target, 4)
                return f"{result:,.4f}".rstrip('0').rstrip('.')
    if to_code == "IRT":
        if from_code == "USD":
            rate = get_live_rate("EUR", "USD")
            if rate:
                eur_amount = amount / rate
                result = round(eur_amount * IRT_PER_EUR, 2)
                return f"{result:,.0f}" if result == int(result) else f"{result:,.2f}"
        else:
            rate_usd_from = get_live_rate("USD", from_code)
            rate_eur_usd = get_live_rate("EUR", "USD")
            if rate_usd_from and rate_eur_usd:
                usd_amount = amount / rate_usd_from
                eur_amount = usd_amount / rate_eur_usd
                result = round(eur_amount * IRT_PER_EUR, 2)
                return f"{result:,.0f}" if result == int(result) else f"{result:,.2f}"
    # Global pairs
    rate = get_live_rate(from_code, to_code)
    if rate:
        result = round(amount * rate, 4)
        return f"{result:,.4f}".rstrip('0').rstrip('.')
    return None

def index(request):
    """Main page: default EUR->IRT"""
    context = {
        "currencies": CURRENCIES,
        "from_code": "EUR",
        "to_code": "IRT",
        "amount": 1,
        "result": convert(1, "EUR", "IRT"),
    }
    return render(request, "convertor/index.html", context)

def convert_api(request):
    """AJAX API for conversion"""
    from_code = request.GET.get("from", "EUR")
    to_code = request.GET.get("to", "IRT")
    try:
        amount = float(request.GET.get("amount", "1"))
    except ValueError:
        amount = 1
    result = convert(amount, from_code, to_code)
    return JsonResponse({"result": result})
