# Norma: A Modern Type-Safe Python ORM 🌟

![GitHub Release](https://img.shields.io/badge/Latest_Release-v1.0.0-blue)

Welcome to **Norma**, a modern, type-safe Object-Relational Mapping (ORM) library for Python. Designed with dataclass support, Norma simplifies database interactions while ensuring type safety. It works seamlessly with various databases, including PostgreSQL, SQLite, MongoDB, and Cassandra. 

You can find the latest releases of Norma [here](https://github.com/Matt42LA/Norma/releases).

## Table of Contents

- [Features](#features)
- [Supported Databases](#supported-databases)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Type Safety**: Norma ensures that your data models are type-checked, reducing runtime errors.
- **Dataclass Support**: Leverage Python's dataclasses for cleaner and more readable code.
- **Asynchronous Support**: Built-in support for async operations makes it easy to handle concurrent tasks.
- **Schema Generation**: Automatically generate database schemas from your dataclasses.
- **Validation**: Validate data easily using Pydantic models.

## Supported Databases

Norma supports the following databases:

- **PostgreSQL**
- **SQLite**
- **MongoDB**
- **Cassandra**

This versatility allows you to choose the best database for your application while maintaining a consistent API.

## Installation

To install Norma, use pip:

```bash
pip install norma
```

Make sure you have Python 3.7 or higher installed.

## Getting Started

To get started with Norma, follow these simple steps:

1. **Import the Library**:
   ```python
   from norma import Database, Model
   ```

2. **Create a Database Connection**:
   ```python
   db = Database('postgresql://user:password@localhost/dbname')
   ```

3. **Define Your Models**:
   ```python
   from dataclasses import dataclass

   @dataclass
   class User(Model):
       id: int
       name: str
       email: str
   ```

4. **Perform Database Operations**:
   ```python
   async def main():
       await db.connect()
       await User.create(name='John Doe', email='john@example.com')
       await db.disconnect()
   ```

## Usage

Norma provides a clean API for database operations. Here’s how you can use it effectively:

### Creating a Model

Define your model using Python dataclasses:

```python
from dataclasses import dataclass
from norma import Model

@dataclass
class Product(Model):
    id: int
    name: str
    price: float
```

### CRUD Operations

Perform Create, Read, Update, and Delete operations easily:

```python
async def create_product(name: str, price: float):
    await Product.create(name=name, price=price)

async def get_product(product_id: int):
    product = await Product.get(product_id)
    return product

async def update_product(product_id: int, name: str, price: float):
    product = await Product.get(product_id)
    product.name = name
    product.price = price
    await product.save()

async def delete_product(product_id: int):
    product = await Product.get(product_id)
    await product.delete()
```

### Asynchronous Operations

Norma's async capabilities allow you to perform non-blocking database operations:

```python
import asyncio

async def main():
    await db.connect()
    await create_product('Laptop', 999.99)
    product = await get_product(1)
    print(product)
    await update_product(1, 'Gaming Laptop', 1299.99)
    await delete_product(1)
    await db.disconnect()

asyncio.run(main())
```

## Examples

Here are some practical examples to help you understand how to use Norma effectively.

### Example 1: User Registration

```python
from dataclasses import dataclass
from norma import Model

@dataclass
class User(Model):
    id: int
    username: str
    password: str

async def register_user(username: str, password: str):
    await User.create(username=username, password=password)
```

### Example 2: Fetching Data

```python
async def fetch_users():
    users = await User.all()
    for user in users:
        print(user.username)
```

### Example 3: Validation with Pydantic

Integrate Pydantic for additional validation:

```python
from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    password: str

async def register_user(data: UserSchema):
    await User.create(username=data.username, password=data.password)
```

## Contributing

We welcome contributions! If you want to contribute to Norma, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your branch to your forked repository.
5. Open a pull request.

Please ensure your code follows the existing style and includes tests where applicable.

## License

Norma is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please reach out via GitHub issues or contact the maintainer directly.

You can find the latest releases of Norma [here](https://github.com/Matt42LA/Norma/releases).

Thank you for using Norma! We hope it simplifies your database interactions and enhances your development experience.