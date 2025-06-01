# test-norma-project

A Norma ORM project using basic template with sqlite database.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Generate schemas:
   ```bash
   norma generate --models ./models --output ./schemas
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Project Structure

- `models/` - Norma model definitions
- `schemas/` - Generated Pydantic schemas
- `config/` - Configuration files
- `main.py` - Main application file

## Norma ORM Features

- Type-safe dataclass-based models
- Automatic Pydantic schema generation
- Support for PostgreSQL, SQLite, and MongoDB
- Async and sync operations
- Field validation and constraints

## Models

### User
- `id`: Primary key (auto-generated)
- `name`: User's full name (indexed)
- `email`: Unique email address with validation
- `age`: Age with range validation (0-150)
- `is_active`: Account status
- `created_at`: Creation timestamp

### Post
- `id`: Primary key (auto-generated)
- `title`: Post title (indexed)
- `content`: Post content
- `author_id`: Foreign key to User
- `published`: Publication status (indexed)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Usage Examples

```python
from norma import NormaClient
from models.user import User

# Initialize client
client = NormaClient(
    adapter_type="sql",  # or "mongo"
    database_url="sqlite:///./app.db"
)

# Create a user
user = User(name="John Doe", email="john@example.com", age=30)
created_user = await client.insert(user)

# Find users
users = await client.find_many(User, {"age": {"$gte": 18}})
```

For more information, visit: https://github.com/norma-orm/norma
