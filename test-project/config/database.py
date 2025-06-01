"""
Database configuration for Norma ORM.
"""

import os
from typing import Dict, Any

# Database configuration
DATABASE_CONFIG: Dict[str, Any] = {
    "type": "postgresql",
    "url": os.getenv("DATABASE_URL", _get_default_url()),
    "echo": os.getenv("DB_ECHO", "false").lower() == "true",
}

def _get_default_url() -> str:
    """Get default database URL based on type."""
    if "postgresql" == "sqlite":
        return "sqlite:///./app.db"
    elif "postgresql" == "postgresql":
        return "postgresql://user:password@localhost/dbname"
    elif "postgresql" == "mongodb":
        return "mongodb://localhost:27017"
    else:
        return "sqlite:///./app.db"

# MongoDB specific configuration
MONGODB_DATABASE_NAME = os.getenv("MONGODB_DATABASE", "norma_db")
