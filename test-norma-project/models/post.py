"""
Post model example with relationships.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from uuid import uuid4

from norma import BaseModel, Field, ManyToOne


@dataclass
class Post(BaseModel):
    """Blog post model with user relationship."""
    
    id: str = Field(
        primary_key=True,
        default_factory=lambda: uuid4().hex,
        description="Unique post identifier"
    )
    
    title: str = Field(
        max_length=200,
        min_length=1,
        index=True,
        description="Post title"
    )
    
    content: str = Field(
        min_length=1,
        description="Post content"
    )
    
    author_id: str = Field(
        relationship=ManyToOne("User", foreign_key="id"),
        description="ID of the post author"
    )
    
    published: bool = Field(
        default=False,
        index=True,
        description="Whether the post is published"
    )
    
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        index=True,
        description="Post creation timestamp"
    )
    
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="Last update timestamp"
    )
