"""
LLM-based currency message parser using OpenRouter API

This module provides functionality to analyze user messages for currency conversion intent
using large language models via the OpenRouter API.
"""

import os
import json
import logging
import aiohttp
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

@dataclass
class CurrencyIntent:
    """Data class for currency conversion intent results"""
    is_currency_exchange: bool
    amount: Optional[float] = None
    from_currency: Optional[str] = None
    to_currency: Optional[str] = None
    confidence: Optional[float] = None
    reasoning: Optional[str] = None

class OpenRouterLLMParser:
    """
    LLM-based parser for detecting currency conversion intent in user messages.
    
    Uses OpenRouter API to analyze messages in Persian and English and extract
    currency conversion information if present.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LLM parser.
        
        Args:
            api_key: OpenRouter API key. If None, will try to get from environment.
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key not provided and OPENROUTER_API_KEY env var not set")
            
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "mistralai/mistral-7b-instruct:free"  # Use free model for reliability
        self.timeout = aiohttp.ClientTimeout(total=15)  # Increase timeout
        
        # Supported currency codes for validation
        self.supported_currencies = {
            'IRT', 'USD', 'EUR', 'GBP', 'TRY', 'AED', 'CAD', 'AUD', 
            'CHF', 'JPY', 'CNY', 'RUB', 'SAR', 'INR', 'KWD', 'QAR', 
            'OMR', 'BHD'
        }
        
        logging.info("OpenRouter LLM Parser initialized")

    def _create_system_prompt(self) -> str:
        """Create the system prompt for currency intent detection"""
        return """You are a currency conversion intent detector. Analyze user messages (in Persian or English) to determine if they contain currency conversion requests.

SUPPORTED CURRENCIES: IRT, USD, EUR, GBP, TRY, AED, CAD, AUD, CHF, JPY, CNY, RUB, SAR, INR, KWD, QAR, OMR, BHD

Persian currency names mapping:
- تومان/تومن = IRT
- دلار = USD  
- یورو = EUR
- پاند = GBP
- لیر = TRY
- درهم = AED
- روبل = RUB
- ریال سعودی = SAR
- روپیه = INR

CRITICAL PERSIAN NUMBER PARSING:
- "میلیون" means million (×1,000,000)
- "هزار" means thousand (×1,000)
- "۲۰۰ میلیون" = 200 × 1,000,000 = 200000000
- "۵۰ هزار" = 50 × 1,000 = 50000
- "دویست میلیون" = 200 × 1,000,000 = 200000000
- "بیست میلیون" = 20 × 1,000,000 = 20000000

IRANIAN CULTURAL CONTEXT FOR TOMAN:
When Iranians say "تومن/تومان" without "میلیون", they usually mean a practical amount.
Use intelligence to determine the realistic amount:
- "صد تومن" (100 toman) → likely means 100,000,000 IRT (100 million)
- "پنجاه تومن" (50 toman) → likely means 50,000,000 IRT (50 million)  
- "هزار تومن" (1000 toman) → likely means 1,000,000,000 IRT (1 billion)
- "دو تومن" (2 toman) → likely means 2,000,000 IRT (2 million)

RULE: If amount + "تومن/تومان" without "میلیون" seems too small (< 1,000,000), 
multiply by 1,000,000 to make it a realistic Iranian amount.

Persian numerals conversion:
۰=0, ۱=1, ۲=2, ۳=3, ۴=4, ۵=5, ۶=6, ۷=7, ۸=8, ۹=9

TASK: Return ONLY a valid JSON object with these fields:
{
  "is_currency_exchange": boolean,
  "amount": number or null,
  "from_currency": "CURRENCY_CODE" or null,
  "to_currency": "CURRENCY_CODE" or null,
  "confidence": 0.0-1.0,
  "reasoning": "brief explanation"
}

RULES:
1. Set is_currency_exchange=true ONLY if message clearly requests currency conversion
2. Extract amount as a number - MULTIPLY by میلیون (1,000,000) or هزار (1,000) if present
3. Map currency names to exact codes from supported list
4. Default to_currency should be "IRT" if not specified
5. For STANDALONE NUMBERS (like "3637", "123") without currency context: set is_currency_exchange=false
6. Confidence: 0.9+ for clear requests, 0.5-0.8 for ambiguous, <0.5 for unclear
7. Return valid JSON only, no other text

SELLING/BUYING CONTEXT:
- "میخوام X یورو بفروشم" = "I want to sell X euros" → from_currency="EUR", to_currency="IRT"
- "میخوام X تا بفروشم" + "یورو" context = selling euros → from_currency="EUR", to_currency="IRT"
- "میخوام X دلار بخرم" = "I want to buy X dollars" → from_currency="IRT", to_currency="USD"
- When selling foreign currency, convert FROM that currency TO IRT
- When buying foreign currency, convert FROM IRT TO that currency

EXAMPLES:
- "100 dollar to toman" → {"is_currency_exchange": true, "amount": 100, "from_currency": "USD", "to_currency": "IRT", "confidence": 0.95, "reasoning": "Clear conversion request"}
- "صد دلار" → {"is_currency_exchange": true, "amount": 100, "from_currency": "USD", "to_currency": "IRT", "confidence": 0.9, "reasoning": "Amount and currency specified, default to IRT"}
- "۲۰۰ میلیون تومان" → {"is_currency_exchange": true, "amount": 200000000, "from_currency": "IRT", "to_currency": "EUR", "confidence": 0.95, "reasoning": "200 million toman conversion"}
- "صد تومن" → {"is_currency_exchange": true, "amount": 100000000, "from_currency": "IRT", "to_currency": "EUR", "confidence": 0.9, "reasoning": "100 toman (culturally means 100 million) conversion"}
- "میخوام صد تومن یورو بخرم" → {"is_currency_exchange": true, "amount": 100000000, "from_currency": "IRT", "to_currency": "EUR", "confidence": 0.9, "reasoning": "Want to buy euros with 100 toman (100 million)"}
- "میخوام 80 یورو بفروشم" → {"is_currency_exchange": true, "amount": 80, "from_currency": "EUR", "to_currency": "IRT", "confidence": 0.9, "reasoning": "Selling 80 euros for toman"}
- "میخوام 80 تا بفروشم یورو" → {"is_currency_exchange": true, "amount": 80, "from_currency": "EUR", "to_currency": "IRT", "confidence": 0.85, "reasoning": "Selling 80 euros for toman"}
- "3637" → {"is_currency_exchange": false, "amount": null, "from_currency": null, "to_currency": null, "confidence": 0.1, "reasoning": "Standalone number without currency context"}
- "hello" → {"is_currency_exchange": false, "amount": null, "from_currency": null, "to_currency": null, "confidence": 0.1, "reasoning": "No currency content detected"}"""

    async def parse_message(self, message: str) -> CurrencyIntent:
        """
        Parse a user message to detect currency conversion intent.
        
        Args:
            message: User message text to analyze
            
        Returns:
            CurrencyIntent object with parsed information
        """
        try:
            # Prepare the API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://nerkhbot.com",
                "X-Title": "NerkhBot Currency Parser"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self._create_system_prompt()},
                    {"role": "user", "content": message}
                ],
                "max_tokens": 200,
                "temperature": 0.1  # Low temperature for consistent parsing
            }
            
            # Make the API request
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(self.base_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result['choices'][0]['message']['content'].strip()
                        
                        # Parse the JSON response
                        parsed_data = json.loads(content)
                        
                        # Validate currencies against supported list
                        from_currency = parsed_data.get('from_currency')
                        to_currency = parsed_data.get('to_currency')
                        
                        if from_currency and from_currency not in self.supported_currencies:
                            logging.warning(f"Unsupported from_currency: {from_currency}")
                            from_currency = None
                            
                        if to_currency and to_currency not in self.supported_currencies:
                            logging.warning(f"Unsupported to_currency: {to_currency}")
                            to_currency = None
                        
                        return CurrencyIntent(
                            is_currency_exchange=parsed_data.get('is_currency_exchange', False),
                            amount=parsed_data.get('amount'),
                            from_currency=from_currency,
                            to_currency=to_currency,
                            confidence=parsed_data.get('confidence', 0.0),
                            reasoning=parsed_data.get('reasoning', '')
                        )
                    else:
                        logging.error(f"OpenRouter API error: {response.status}")
                        return self._create_fallback_intent()
                        
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse LLM response as JSON: {e}")
            return self._create_fallback_intent()
        except aiohttp.ClientError as e:
            logging.error(f"HTTP request failed: {e}")
            return self._create_fallback_intent()
        except Exception as e:
            logging.error(f"Unexpected error in LLM parsing: {e}")
            return self._create_fallback_intent()

    def _create_fallback_intent(self) -> CurrencyIntent:
        """Create a fallback intent when LLM parsing fails"""
        return CurrencyIntent(
            is_currency_exchange=False,
            confidence=0.0,
            reasoning="LLM parsing failed"
        )

    async def is_healthy(self) -> bool:
        """
        Check if the OpenRouter API is accessible.
        
        Returns:
            True if API is accessible, False otherwise
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://nerkhbot.com",
                "X-Title": "NerkhBot Health Check"
            }
            
            # Simple test request
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "hi"}],
                "max_tokens": 1
            }
            
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(self.base_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        logging.info("✅ OpenRouter API health check passed")
                        return True
                    else:
                        response_text = await response.text()
                        logging.warning(f"⚠️ OpenRouter API health check failed: {response.status} - {response_text}")
                        return False
                    
        except aiohttp.ClientError as e:
            logging.warning(f"⚠️ OpenRouter API network error: {e}")
            return False
        except Exception as e:
            logging.error(f"❌ OpenRouter API health check failed: {e}")
            return False

# Global instance for reuse across the application
_llm_parser_instance: Optional[OpenRouterLLMParser] = None

def get_llm_parser() -> Optional[OpenRouterLLMParser]:
    """
    Get the global LLM parser instance.
    
    Returns:
        OpenRouterLLMParser instance or None if API key not available
    """
    global _llm_parser_instance
    
    if _llm_parser_instance is None:
        try:
            _llm_parser_instance = OpenRouterLLMParser()
        except ValueError as e:
            logging.warning(f"LLM parser not available: {e}")
            return None
            
    return _llm_parser_instance
