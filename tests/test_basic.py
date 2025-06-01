"""
Basic tests for Norma ORM functionality.
"""

from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

# Import from the relative path since we're testing
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from norma import BaseModel, Field, NormaClient
from norma.exceptions import ValidationError


class TestFailure(Exception):
    """Custom test failure exception."""
    pass


def assert_equal(actual, expected, message=""):
    """Simple assertion helper."""
    if actual != expected:
        raise TestFailure(f"Expected {expected}, got {actual}. {message}")


def assert_true(condition, message=""):
    """Assert that condition is True."""
    if not condition:
        raise TestFailure(f"Expected True, got {condition}. {message}")


def assert_in(item, container, message=""):
    """Assert that item is in container."""
    if item not in container:
        raise TestFailure(f"Expected {item} to be in {container}. {message}")


def assert_raises(exception_type, func, *args, **kwargs):
    """Assert that function raises expected exception."""
    try:
        func(*args, **kwargs)
        raise TestFailure(f"Expected {exception_type.__name__} to be raised")
    except exception_type:
        pass  # Expected
    except Exception as e:
        raise TestFailure(f"Expected {exception_type.__name__}, got {type(e).__name__}: {e}")


@dataclass
class TestUser(BaseModel):
    """Test user model."""
    
    name: str = Field(
        max_length=100,
        min_length=1,
        description="User name"
    )
    
    email: str = Field(
        unique=True,
        max_length=255,
        description="User email"
    )
    
    age: int = Field(
        default=0,
        min_value=0,
        max_value=150,
        description="User age"
    )
    
    id: str = Field(
        primary_key=True,
        default_factory=lambda: uuid4().hex,
        description="User ID"
    )


def test_model_creation():
    """Test basic model creation and validation."""
    
    # Valid user
    user = TestUser(
        name="John Doe",
        email="john@example.com",
        age=30
    )
    
    assert_equal(user.name, "John Doe")
    assert_equal(user.email, "john@example.com")
    assert_equal(user.age, 30)
    assert_true(user.id is not None, "ID should be auto-generated")


def test_model_validation():
    """Test model validation."""
    
    # Test required field validation
    assert_raises(ValidationError, TestUser, name="", email="john@example.com")  # Empty name
    
    # Test age validation
    assert_raises(ValidationError, TestUser, name="John", email="john@example.com", age=-1)  # Negative age
    
    assert_raises(ValidationError, TestUser, name="John", email="john@example.com", age=200)  # Too old


def test_model_serialization():
    """Test model serialization."""
    
    user = TestUser(
        name="Jane Doe",
        email="jane@example.com", 
        age=25
    )
    
    # Test to_dict
    user_dict = user.to_dict()
    assert user_dict["name"] == "Jane Doe"
    assert user_dict["email"] == "jane@example.com"
    assert user_dict["age"] == 25
    assert "id" in user_dict
    
    # Test from_dict
    new_user = TestUser.from_dict(user_dict)
    assert new_user.name == user.name
    assert new_user.email == user.email
    assert new_user.age == user.age
    assert new_user.id == user.id


def test_model_metadata():
    """Test model metadata extraction."""
    
    # Test primary key detection
    pk_field = TestUser.get_primary_key_field()
    assert pk_field == "id"
    
    # Test unique fields
    unique_fields = TestUser.get_unique_fields()
    assert "id" in unique_fields  # Primary key is unique
    assert "email" in unique_fields  # Email is unique
    
    # Test field configuration
    email_config = TestUser.get_field_config("email")
    assert email_config is not None
    assert email_config.unique is True
    assert email_config.max_length == 255


def test_model_update():
    """Test model update functionality."""
    
    user = TestUser(
        name="Bob Smith",
        email="bob@example.com",
        age=35
    )
    
    # Update fields
    user.update(name="Robert Smith", age=36)
    
    assert user.name == "Robert Smith"
    assert user.age == 36
    assert user.email == "bob@example.com"  # Unchanged


def test_client_initialization():
    """Test client initialization."""
    
    # Test SQL client
    sql_client = NormaClient(
        adapter_type="sql",
        database_url="sqlite:///:memory:"
    )
    
    assert sql_client.adapter_type == "sql"
    assert sql_client.database_url == "sqlite:///:memory:"
    
    # Test model client creation
    user_client = sql_client.get_model_client(TestUser)
    assert user_client.model_class == TestUser


def test_field_configuration():
    """Test field configuration."""
    
    # Test field with all options
    field = Field(
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        min_length=1,
        max_length=100,
        min_value=0,
        max_value=150,
        description="Test field"
    )
    
    # The field function returns a dataclass field with metadata
    assert hasattr(field, 'metadata')
    config = field.metadata.get('norma_config')
    assert config is not None
    assert config.primary_key is True
    assert config.unique is True
    assert config.index is True
    assert config.nullable is False
    assert config.min_length == 1
    assert config.max_length == 100
    assert config.min_value == 0
    assert config.max_value == 150
    assert config.description == "Test field"


if __name__ == "__main__":
    # Run tests
    test_model_creation()
    test_model_validation()
    test_model_serialization() 
    test_model_metadata()
    test_model_update()
    test_client_initialization()
    test_field_configuration()
    
    print("All tests passed! ✅") 