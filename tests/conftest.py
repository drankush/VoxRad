"""Pytest configuration and shared fixtures."""

import pytest
import sys
import os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import config


@pytest.fixture(autouse=True)
def reset_config():
    """Reset config state before each test."""
    # Mock config for testing
    config.TRANSCRIPTION_API_KEY = None
    config.TEXT_API_KEY = None
    config.MM_API_KEY = None
    config.current_encrypted_report = None
    config.current_report_encryption_key = None
    config.config_path = os.path.expanduser("~/.voxrad/settings.ini")
    yield
    # Cleanup after test


@pytest.fixture
def mock_config(monkeypatch):
    """Provide a mock config object."""
    mock_cfg = MagicMock()
    mock_cfg.TRANSCRIPTION_API_KEY = None
    mock_cfg.TEXT_API_KEY = None
    mock_cfg.MM_API_KEY = None
    mock_cfg.config_path = os.path.expanduser("~/.voxrad/settings.ini")
    return mock_cfg


@pytest.fixture
def temp_config_dir(tmp_path):
    """Provide a temporary config directory."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    return config_dir
