"""
User model example.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from uuid import uuid4

from norma import BaseModel, Field


@dataclass
class User(BaseModel):
    """User model with validation and constraints."""
    
    id: str = Field(
        primary_key=True,
        default_factory=lambda: uuid4().hex,
        description="Unique user identifier"
    )
    
    name: str = Field(
        max_length=100,
        min_length=1,
        index=True,
        description="User's full name"
    )
    
    email: str = Field(
        unique=True,
        max_length=255,
        regex_pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        description="User's email address"
    )
    
    age: int = Field(
        default=0,
        min_value=0,
        max_value=150,
        description="User's age in years"
    )
    
    is_active: bool = Field(
        default=True,
        description="Whether the user account is active"
    )
    
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="Account creation timestamp"
    )
