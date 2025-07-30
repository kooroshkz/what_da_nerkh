"""
Persistent user data storage using JSON files
"""
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

# Create data directory if it doesn't exist
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USER_DEFAULTS_FILE = DATA_DIR / "user_defaults.json"

# In-memory cache for active sessions (temporary data)
user_sessions: Dict[int, Dict[str, Any]] = {}

# Load user defaults from file on startup
def load_user_defaults() -> Dict[int, Dict[str, Any]]:
    """Load user defaults from JSON file"""
    try:
        if USER_DEFAULTS_FILE.exists():
            with open(USER_DEFAULTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert string keys back to integers
                return {int(k): v for k, v in data.items()}
    except Exception as e:
        print(f"Error loading user defaults: {e}")
    return {}

# Save user defaults to file
def save_user_defaults(defaults: Dict[int, Dict[str, Any]]) -> None:
    """Save user defaults to JSON file"""
    try:
        # Convert integer keys to strings for JSON
        data = {str(k): v for k, v in defaults.items()}
        with open(USER_DEFAULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving user defaults: {e}")

# Load defaults on module import
user_defaults = load_user_defaults()

def get_user_session(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user session data (temporary)"""
    return user_sessions.get(user_id)

def set_user_session(user_id: int, session_data: Dict[str, Any]) -> None:
    """Set user session data (temporary)"""
    user_sessions[user_id] = session_data

def update_user_session(user_id: int, key: str, value: Any) -> None:
    """Update specific key in user session (temporary)"""
    if user_id not in user_sessions:
        user_sessions[user_id] = {}
    user_sessions[user_id][key] = value

def clear_user_session(user_id: int) -> None:
    """Clear user session (temporary)"""
    if user_id in user_sessions:
        del user_sessions[user_id]

def has_valid_session(user_id: int) -> bool:
    """Check if user has a valid conversion session"""
    session = get_user_session(user_id)
    return session is not None and "to" in session and "from" in session

# === PERSISTENT DEFAULT PAIR FUNCTIONS ===

def get_user_default_pair(user_id: int) -> Optional[Dict[str, str]]:
    """Get user's default currency pair (persistent)"""
    return user_defaults.get(user_id, {}).get("default_pair")

def set_user_default_pair(user_id: int, from_currency: str, to_currency: str) -> None:
    """Set user's default currency pair (persistent)"""
    global user_defaults
    
    if user_id not in user_defaults:
        user_defaults[user_id] = {}
    
    user_defaults[user_id]["default_pair"] = {
        "from": from_currency,
        "to": to_currency
    }
    
    # Save to file immediately
    save_user_defaults(user_defaults)

def has_default_pair(user_id: int) -> bool:
    """Check if user has set a default currency pair (persistent)"""
    default_pair = get_user_default_pair(user_id)
    return default_pair is not None and "from" in default_pair and "to" in default_pair

def get_user_stats(user_id: int) -> Dict[str, Any]:
    """Get user statistics (persistent)"""
    return user_defaults.get(user_id, {})

def update_user_stats(user_id: int, key: str, value: Any) -> None:
    """Update user statistics (persistent)"""
    global user_defaults
    
    if user_id not in user_defaults:
        user_defaults[user_id] = {}
    
    user_defaults[user_id][key] = value
    save_user_defaults(user_defaults)
