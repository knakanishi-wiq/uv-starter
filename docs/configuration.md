# Configuration Management

This project uses pydantic-settings for robust, type-safe configuration management with automatic environment variable loading.

## Overview

The configuration system provides:
- **Type safety** with automatic validation
- **Environment variable** support with `.env` files
- **Default values** for development
- **Documentation** through field descriptions
- **Caching** for performance

## Configuration File

The main configuration is in `src/uv-starter/config.py`:

```python
from functools import lru_cache
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Application settings
    app_name: str = Field(default="uv-starter", description="Application name")
    debug: bool = Field(default=False, description="Debug mode")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

## Usage

### Basic Usage

```python
from uv_starter.config import settings

# Access configuration values
print(f"App: {settings.app_name}")
print(f"Debug mode: {settings.debug}")
print(f"Log level: {settings.log_level}")
```

### In Application Code

```python
from uv_starter.config import settings
from loguru import logger

# Configure logging based on settings
logger.remove()
logger.add(
    sys.stderr,
    level=settings.log_level,
    format="<green>{time}</green> | <level>{level: <8}</level> | {message}"
)

# Use debug mode
if settings.debug:
    logger.debug("Debug mode enabled")
```

## Environment Variables

### Automatic Loading

pydantic-settings automatically loads environment variables:

```bash
# Environment variables override defaults
export DEBUG=true
export LOG_LEVEL=debug
export API_PORT=3000

python script.py  # Uses environment values
```

### Case Insensitivity

Environment variables are case-insensitive by default:

```bash
# All of these work the same:
export DEBUG=true
export debug=true
export Debug=true
```

## .env Files

### Local Development

Create `.env` for local development:

```bash
# .env
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///./dev.db
API_KEY=dev-api-key-12345
SECRET_KEY=dev-secret-for-local-only
```

### Multiple Environments

```bash
# .env.development
DEBUG=true
DATABASE_URL=sqlite:///./dev.db

# .env.testing
DEBUG=false
DATABASE_URL=sqlite:///./test.db

# .env.production
DEBUG=false
DATABASE_URL=postgresql://user:pass@prod-db:5432/app
```

Load specific environment:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.production"  # Specific environment
    )
```

## Configuration Categories

### Application Settings

```python
class Settings(BaseSettings):
    # Basic app configuration
    app_name: str = "uv-starter"
    version: str = "0.1.0"
    debug: bool = False
    environment: Literal["development", "testing", "production"] = "development"
```

### Logging Configuration

```python
class Settings(BaseSettings):
    # Logging settings
    log_level: str = "INFO"
    log_format: str = "{time} | {level} | {message}"
    log_file: Optional[str] = None
```

### Database Configuration

```python
class Settings(BaseSettings):
    # Database settings
    database_url: str = "sqlite:///./app.db"
    database_echo: bool = False
    max_connections: int = 10
```

### API Configuration

```python
class Settings(BaseSettings):
    # API settings
    api_host: str = "localhost"
    api_port: int = 8000
    api_workers: int = 1
    api_reload: bool = False
```

### Security Settings

```python
class Settings(BaseSettings):
    # Security settings
    secret_key: str = Field(..., description="Secret key for signing")
    api_key: str = Field(default="", description="External API key")
    allowed_hosts: List[str] = Field(default_factory=list)
```

## Advanced Configuration

### Nested Settings

```python
class DatabaseSettings(BaseSettings):
    url: str = "sqlite:///./app.db"
    echo: bool = False
    pool_size: int = 5

class APISettings(BaseSettings):
    host: str = "localhost"
    port: int = 8000
    workers: int = 1

class Settings(BaseSettings):
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    api: APISettings = Field(default_factory=APISettings)
```

### Custom Validation

```python
from pydantic import validator

class Settings(BaseSettings):
    api_port: int = 8000
    
    @validator('api_port')
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v
```

### Environment-Specific Loading

```python
import os
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('ENVIRONMENT', 'development')}"
    )
```

## Testing Configuration

### Test Settings

```python
# tests/conftest.py
import pytest
from uv_starter.config import Settings

@pytest.fixture
def test_settings():
    """Override settings for testing."""
    return Settings(
        debug=True,
        database_url="sqlite:///:memory:",
        api_key="test-key",
    )
```

### Mocking Settings

```python
# tests/test_config.py
from unittest.mock import patch
from uv_starter.config import get_settings

def test_with_mocked_settings():
    with patch('uv_starter.config.get_settings') as mock_settings:
        mock_settings.return_value.debug = True
        mock_settings.return_value.api_key = "test-key"
        
        # Test code using mocked settings
        pass
```

## Production Deployment

### Environment Variables

Set environment variables in production:

```bash
# Container environment
ENV DEBUG=false
ENV LOG_LEVEL=INFO
ENV DATABASE_URL=postgresql://user:pass@db:5432/app
ENV SECRET_KEY=your-production-secret-key
```

### Docker Configuration

```dockerfile
# Dockerfile
ENV DEBUG=false
ENV LOG_LEVEL=INFO
COPY .env.production .env
```

### Kubernetes ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DEBUG: "false"
  LOG_LEVEL: "INFO"
  API_PORT: "8000"
```

## Security Best Practices

### Secrets Management

```python
class Settings(BaseSettings):
    # Use separate fields for secrets
    secret_key: SecretStr = Field(..., description="Application secret")
    database_password: SecretStr = Field(..., description="Database password")
    
    def get_database_url(self) -> str:
        return f"postgresql://user:{self.database_password.get_secret_value()}@host/db"
```

### .env File Security

```bash
# Add to .gitignore
.env
.env.local
.env.*.local

# Never commit production secrets
# Use environment variables or secret management systems
```

## Troubleshooting

### Common Issues

**Environment variables not loading:**
```python
# Check if .env file exists and is readable
from pathlib import Path
print(Path(".env").exists())
print(Path(".env").read_text())
```

**Type validation errors:**
```python
# Check the actual values being loaded
settings = Settings()
print(settings.model_dump())
```

**Case sensitivity issues:**
```python
# Ensure case_sensitive=False in config
class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)
```

### Debugging Configuration

```python
from uv_starter.config import settings

# Print all configuration values (be careful with secrets!)
print("Configuration:")
for key, value in settings.model_dump().items():
    if "secret" in key.lower() or "password" in key.lower():
        print(f"{key}: ***")
    else:
        print(f"{key}: {value}")
```

## Configuration Validation

### Startup Validation

```python
def validate_configuration():
    """Validate configuration at startup."""
    try:
        settings = get_settings()
        
        # Test database connection
        if settings.database_url.startswith("postgresql"):
            # Test PostgreSQL connection
            pass
            
        # Validate required API keys
        if not settings.api_key and settings.environment == "production":
            raise ValueError("API key required in production")
            
        logger.info("Configuration validation successful")
        
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        raise

# Call during application startup
if __name__ == "__main__":
    validate_configuration()
```