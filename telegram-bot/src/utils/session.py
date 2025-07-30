"""
User session management utilities
"""
from typing import Dict, Any, Optional

# In-memory storage for user sessions (temporary data only)
user_sessions: Dict[int, Dict[str, Any]] = {}

def get_user_session(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user session data"""
    return user_sessions.get(user_id)

def set_user_session(user_id: int, session_data: Dict[str, Any]) -> None:
    """Set user session data"""
    user_sessions[user_id] = session_data

def update_user_session(user_id: int, key: str, value: Any) -> None:
    """Update specific key in user session"""
    if user_id not in user_sessions:
        user_sessions[user_id] = {}
    user_sessions[user_id][key] = value

def clear_user_session(user_id: int) -> None:
    """Clear user session"""
    if user_id in user_sessions:
        del user_sessions[user_id]

def has_valid_session(user_id: int) -> bool:
    """Check if user has a valid conversion session"""
    session = get_user_session(user_id)
    return session is not None and "to" in session and "from" in session

# === DEFAULT PAIR FUNCTIONS (Delegated to persistent storage) ===

def get_user_default_pair(user_id: int) -> Optional[Dict[str, str]]:
    """Get user's default currency pair"""
    from .persistent_storage import get_user_default_pair as get_persistent_default
    return get_persistent_default(user_id)

def set_user_default_pair(user_id: int, from_currency: str, to_currency: str) -> None:
    """Set user's default currency pair"""
    from .persistent_storage import set_user_default_pair as set_persistent_default
    set_persistent_default(user_id, from_currency, to_currency)

def has_default_pair(user_id: int) -> bool:
    """Check if user has set a default currency pair"""
    from .persistent_storage import has_default_pair as has_persistent_default
    return has_persistent_default(user_id)
