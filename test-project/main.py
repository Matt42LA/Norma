"""
FastAPI application with Norma ORM.
"""

from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from contextlib import asynccontextmanager

from norma import NormaClient
from config.database import DATABASE_CONFIG, MONGODB_DATABASE_NAME
from models.user import User
from models.post import Post


# Global client instance
client: Optional[NormaClient] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global client
    
    # Initialize Norma client
    if DATABASE_CONFIG["type"] == "mongodb":
        client = NormaClient(
            adapter_type="mongo",
            database_url=DATABASE_CONFIG["url"],
            database_name=MONGODB_DATABASE_NAME
        )
    else:
        client = NormaClient(
            adapter_type="sql",
            database_url=DATABASE_CONFIG["url"]
        )
    
    # Connect and create tables
    await client.connect()
    
    user_client = client.get_model_client(User)
    post_client = client.get_model_client(Post)
    
    await user_client.create_table()
    await post_client.create_table()
    
    yield
    
    # Cleanup
    await client.disconnect()


app = FastAPI(
    title="Norma ORM API",
    description="Example API using Norma ORM",
    version="1.0.0",
    lifespan=lifespan
)


def get_client() -> NormaClient:
    """Get the global client instance."""
    if client is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    return client


@app.get("/users", response_model=List[dict])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    client: NormaClient = Depends(get_client)
):
    """Get all users."""
    user_client = client.get_model_client(User)
    users = await user_client.find_many(offset=skip, limit=limit)
    return [user.to_dict() for user in users]


@app.get("/users/{user_id}")
async def get_user(user_id: str, client: NormaClient = Depends(get_client)):
    """Get a specific user."""
    user_client = client.get_model_client(User)
    user = await user_client.find_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.to_dict()


@app.post("/users")
async def create_user(
    user_data: dict,
    client: NormaClient = Depends(get_client)
):
    """Create a new user."""
    user_client = client.get_model_client(User)
    
    try:
        user = User.from_dict(user_data)
        created_user = await user_client.insert(user)
        return created_user.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/posts", response_model=List[dict])
async def get_posts(
    published: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    client: NormaClient = Depends(get_client)
):
    """Get all posts."""
    post_client = client.get_model_client(Post)
    
    filters = {}
    if published is not None:
        filters["published"] = published
    
    posts = await post_client.find_many(filters, offset=skip, limit=limit)
    return [post.to_dict() for post in posts]


@app.post("/posts")
async def create_post(
    post_data: dict,
    client: NormaClient = Depends(get_client)
):
    """Create a new post."""
    post_client = client.get_model_client(Post)
    
    try:
        post = Post.from_dict(post_data)
        created_post = await post_client.insert(post)
        return created_post.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
