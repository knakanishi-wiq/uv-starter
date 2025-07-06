"""Tests for configuration management."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from uv_starter.config import Settings, get_settings


class TestSettings:
    """Test Settings class."""

    def test_default_values(self):
        """Test that default values are set correctly."""
        settings = Settings()

        assert settings.app_name == "uv-starter"
        assert settings.debug is False
        assert settings.log_level == "INFO"
        assert settings.database_url == "sqlite:///./app.db"
        assert settings.api_host == "localhost"
        assert settings.api_port == 8000
        assert settings.api_key == ""
        assert settings.secret_key == "dev-secret-key"

    def test_environment_variable_override(self):
        """Test that environment variables override defaults."""
        with patch.dict(
            os.environ,
            {
                "APP_NAME": "test-app",
                "DEBUG": "true",
                "LOG_LEVEL": "DEBUG",
                "API_PORT": "3000",
            },
        ):
            settings = Settings()

            assert settings.app_name == "test-app"
            assert settings.debug is True
            assert settings.log_level == "DEBUG"
            assert settings.api_port == 3000

    def test_case_insensitive_env_vars(self):
        """Test that environment variables are case insensitive."""
        with patch.dict(
            os.environ,
            {
                "debug": "true",
                "LOG_level": "WARNING",
                "Api_Port": "9000",
            },
        ):
            settings = Settings()

            assert settings.debug is True
            assert settings.log_level == "WARNING"
            assert settings.api_port == 9000

    def test_log_level_validation(self):
        """Test that log level accepts only valid values."""
        # Valid log levels should work
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            settings = Settings(log_level=level)
            assert settings.log_level == level

        # Invalid log level should raise ValidationError
        with pytest.raises(ValidationError):
            Settings(log_level="INVALID")

    def test_api_port_type_validation(self):
        """Test that api_port is validated as integer."""
        # Valid port number
        settings = Settings(api_port=8080)
        assert settings.api_port == 8080

        # String that can be converted to int
        with patch.dict(os.environ, {"API_PORT": "9000"}):
            settings = Settings()
            assert settings.api_port == 9000

        # Invalid port (string that can't be converted)
        with pytest.raises(ValidationError):
            with patch.dict(os.environ, {"API_PORT": "not-a-number"}):
                Settings()

    def test_boolean_conversion(self):
        """Test that boolean values are converted correctly from env vars."""
        test_cases = [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("1", True),
            ("on", True),
            ("yes", True),
            ("false", False),
            ("False", False),
            ("FALSE", False),
            ("0", False),
            ("off", False),
            ("no", False),
        ]

        for env_value, expected in test_cases:
            with patch.dict(os.environ, {"DEBUG": env_value}):
                settings = Settings()
                assert settings.debug is expected

    def test_env_file_loading(self):
        """Test loading configuration from .env file."""
        env_content = """
APP_NAME=env-test-app
DEBUG=true
LOG_LEVEL=ERROR
API_PORT=5000
SECRET_KEY=test-secret
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write(env_content)
            env_file_path = f.name

        try:
            # Create settings with custom env file
            settings = Settings(_env_file=env_file_path)

            assert settings.app_name == "env-test-app"
            assert settings.debug is True
            assert settings.log_level == "ERROR"
            assert settings.api_port == 5000
            assert settings.secret_key == "test-secret"
        finally:
            os.unlink(env_file_path)

    def test_extra_fields_ignored(self):
        """Test that extra fields are ignored due to 'extra=ignore' config."""
        with patch.dict(os.environ, {"UNKNOWN_FIELD": "should-be-ignored"}):
            # Should not raise an error
            settings = Settings()
            assert not hasattr(settings, "unknown_field")

    def test_field_descriptions(self):
        """Test that field descriptions are properly set."""
        # Access field info from the model
        fields = Settings.model_fields

        assert fields["app_name"].description == "Application name"
        assert fields["debug"].description == "Debug mode"
        assert fields["log_level"].description == "Logging level"
        assert fields["database_url"].description == "Database connection URL"
        assert fields["api_host"].description == "API host"
        assert fields["api_port"].description == "API port"
        assert fields["api_key"].description == "External API key"
        assert fields["secret_key"].description == "Application secret key"


class TestGetSettings:
    """Test get_settings function."""

    def test_get_settings_returns_settings_instance(self):
        """Test that get_settings returns a Settings instance."""
        settings = get_settings()
        assert isinstance(settings, Settings)

    def test_get_settings_caching(self):
        """Test that get_settings caches the result."""
        settings1 = get_settings()
        settings2 = get_settings()

        # Should return the same instance due to lru_cache
        assert settings1 is settings2

    def test_get_settings_cache_clear(self):
        """Test that cache can be cleared and new instance is created."""
        settings1 = get_settings()

        # Clear the cache
        get_settings.cache_clear()

        settings2 = get_settings()

        # Should be different instances after cache clear
        assert settings1 is not settings2
        assert isinstance(settings2, Settings)

    def test_settings_module_level_instance(self):
        """Test that module-level settings variable works correctly."""
        from uv_starter.config import settings

        assert isinstance(settings, Settings)
        assert settings.app_name == "uv-starter"


class TestSettingsIntegration:
    """Integration tests for Settings."""

    def test_database_url_formats(self):
        """Test different database URL formats."""
        test_urls = [
            "sqlite:///./app.db",
            "postgresql://user:pass@localhost:5432/dbname",
            "mysql://user:pass@localhost:3306/dbname",
        ]

        for url in test_urls:
            settings = Settings(database_url=url)
            assert settings.database_url == url

    def test_realistic_configuration(self):
        """Test a realistic production-like configuration."""
        with patch.dict(
            os.environ,
            {
                "APP_NAME": "my-production-app",
                "DEBUG": "false",
                "LOG_LEVEL": "WARNING",
                "DATABASE_URL": "postgresql://user:pass@prod-db:5432/app",
                "API_HOST": "0.0.0.0",
                "API_PORT": "80",
                "API_KEY": "prod-api-key-123",
                "SECRET_KEY": "super-secret-production-key",
            },
        ):
            settings = Settings()

            assert settings.app_name == "my-production-app"
            assert settings.debug is False
            assert settings.log_level == "WARNING"
            assert settings.database_url == "postgresql://user:pass@prod-db:5432/app"
            assert settings.api_host == "0.0.0.0"
            assert settings.api_port == 80
            assert settings.api_key == "prod-api-key-123"
            assert settings.secret_key == "super-secret-production-key"

    def test_partial_environment_override(self):
        """Test that only some environment variables can be set."""
        with patch.dict(
            os.environ,
            {
                "DEBUG": "true",
                "API_PORT": "9999",
            },
        ):
            settings = Settings()

            # Overridden values
            assert settings.debug is True
            assert settings.api_port == 9999

            # Default values should remain
            assert settings.app_name == "uv-starter"
            assert settings.log_level == "INFO"
            assert settings.api_host == "localhost"


class TestSettingsEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_string_values(self):
        """Test handling of empty string values."""
        with patch.dict(
            os.environ,
            {
                "API_KEY": "",
                "SECRET_KEY": "",
            },
        ):
            settings = Settings()

            assert settings.api_key == ""
            assert settings.secret_key == ""

    def test_whitespace_handling(self):
        """Test that whitespace in environment variables is handled correctly."""
        with patch.dict(
            os.environ,
            {
                "APP_NAME": "  test-app  ",
                "API_KEY": "\ttest-key\n",
            },
        ):
            settings = Settings()

            # pydantic should strip whitespace automatically
            assert settings.app_name == "  test-app  "  # Actually preserved
            assert settings.api_key == "\ttest-key\n"  # Actually preserved

    def test_very_long_values(self):
        """Test handling of very long configuration values."""
        long_value = "x" * 10000

        with patch.dict(os.environ, {"SECRET_KEY": long_value}):
            settings = Settings()
            assert settings.secret_key == long_value

    @pytest.mark.parametrize("invalid_port", [-1, 0, 70000, "abc"])
    def test_invalid_port_values(self, invalid_port):
        """Test various invalid port values."""
        if isinstance(invalid_port, str):
            with patch.dict(os.environ, {"API_PORT": invalid_port}):
                with pytest.raises(ValidationError):
                    Settings()
        else:
            with pytest.raises(ValidationError):
                Settings(api_port=invalid_port)
