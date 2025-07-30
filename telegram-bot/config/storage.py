"""
Environment-specific storage configuration
"""
import os

# Storage configuration
STORAGE_TYPE = os.getenv("STORAGE_TYPE", "file")  # file, memory, database
DATA_DIR = os.getenv("DATA_DIR", "data")  # Can be set differently on each server

# Database configuration (if using database storage)
DATABASE_URL = os.getenv("DATABASE_URL", None)

# Storage file naming
USER_DEFAULTS_FILE = os.path.join(DATA_DIR, "user_defaults.json")
USER_SESSIONS_FILE = os.path.join(DATA_DIR, "user_sessions.json")
