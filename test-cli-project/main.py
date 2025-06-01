"""
Basic Norma application example.
"""

import asyncio
from norma import NormaClient
from config.database import DATABASE_CONFIG, MONGODB_DATABASE_NAME
from models.user import User
from models.post import Post


async def main():
    """Main application function."""
    
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
    
    # Connect to database
    async with client:
        # Create tables/collections
        user_client = client.get_model_client(User)
        post_client = client.get_model_client(Post)
        
        await user_client.create_table()
        await post_client.create_table()
        
        # Create a user
        user = User(
            name="John Doe",
            email="john@example.com",
            age=30
        )
        
        created_user = await user_client.insert(user)
        print(f"Created user: {created_user}")
        
        # Create a post
        post = Post(
            title="Hello Norma!",
            content="This is my first post using Norma ORM.",
            author_id=created_user.id,
            published=True
        )
        
        created_post = await post_client.insert(post)
        print(f"Created post: {created_post}")
        
        # Find users
        users = await user_client.find_many()
        print(f"Found {len(users)} users")
        
        # Find posts
        posts = await post_client.find_many({"published": True})
        print(f"Found {len(posts)} published posts")


if __name__ == "__main__":
    asyncio.run(main())
