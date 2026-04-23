"""Unit tests for encryption utilities."""

import pytest
import os
import tempfile
from cryptography.fernet import Fernet, InvalidToken
from unittest.mock import patch, MagicMock
from config.config import config
from utils.crypto_utils import (
    decrypt_audio_file,
    cleanup_temp_file,
    encrypt_and_store_report,
    decrypt_report
)


class TestDecryptAudioFile:
    """Tests for decrypt_audio_file function."""

    def test_decrypt_audio_file_success(self):
        """Test successful audio file decryption."""
        key = Fernet.generate_key()
        cipher = Fernet(key)
        test_data = b"test audio data"
        encrypted_data = cipher.encrypt(test_data)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as enc_file:
            enc_file.write(encrypted_data)
            encrypted_path = enc_file.name

        try:
            decrypted_path = decrypt_audio_file(encrypted_path, key, ".mp3")
            assert decrypted_path is not None
            assert os.path.exists(decrypted_path)

            with open(decrypted_path, "rb") as f:
                decrypted_data = f.read()
            assert decrypted_data == test_data

            cleanup_temp_file(decrypted_path)
        finally:
            cleanup_temp_file(encrypted_path)

    def test_decrypt_audio_file_missing_file(self):
        """Test decryption with missing file."""
        key = Fernet.generate_key()
        with pytest.raises(FileNotFoundError):
            decrypt_audio_file("/nonexistent/path.mp3", key)

    def test_decrypt_audio_file_invalid_key(self):
        """Test decryption with invalid key."""
        key = Fernet.generate_key()
        wrong_key = Fernet.generate_key()
        cipher = Fernet(key)
        encrypted_data = cipher.encrypt(b"test data")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as enc_file:
            enc_file.write(encrypted_data)
            encrypted_path = enc_file.name

        try:
            with pytest.raises(InvalidToken):
                decrypt_audio_file(encrypted_path, wrong_key)
        finally:
            cleanup_temp_file(encrypted_path)


class TestCleanupTempFile:
    """Tests for cleanup_temp_file function."""

    def test_cleanup_existing_file(self):
        """Test cleanup of existing file."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test content")
            tmp_path = tmp.name

        assert os.path.exists(tmp_path)
        cleanup_temp_file(tmp_path)
        assert not os.path.exists(tmp_path)

    def test_cleanup_nonexistent_file(self):
        """Test cleanup of non-existent file (should not raise)."""
        cleanup_temp_file("/nonexistent/path.tmp")

    def test_cleanup_none(self):
        """Test cleanup with None path."""
        cleanup_temp_file(None)


class TestEncryptAndStoreReport:
    """Tests for encrypt_and_store_report function."""

    def test_encrypt_and_store_report_success(self):
        """Test successful report encryption and storage."""
        test_report = "This is a test medical report."

        encrypted_report, encryption_key = encrypt_and_store_report(test_report)

        assert encrypted_report is not None
        assert encryption_key is not None
        assert config.current_encrypted_report == encrypted_report
        assert config.current_report_encryption_key == encryption_key

    def test_encrypt_and_store_report_retrieval(self):
        """Test that encrypted report can be decrypted."""
        test_report = "Patient presents with symptoms..."

        encrypted_report, encryption_key = encrypt_and_store_report(test_report)
        decrypted = decrypt_report(encrypted_report, encryption_key)

        assert decrypted == test_report


class TestDecryptReport:
    """Tests for decrypt_report function."""

    def test_decrypt_report_success(self):
        """Test successful report decryption."""
        key = Fernet.generate_key()
        cipher = Fernet(key)
        original_text = "Test report content"
        encrypted_text = cipher.encrypt(original_text.encode()).decode()

        decrypted = decrypt_report(encrypted_text, key)
        assert decrypted == original_text

    def test_decrypt_report_with_string_key(self):
        """Test decryption with string key (common case)."""
        key = Fernet.generate_key()
        cipher = Fernet(key)
        original_text = "Another test"
        encrypted_text = cipher.encrypt(original_text.encode()).decode()

        decrypted = decrypt_report(encrypted_text, key.decode())
        assert decrypted == original_text

    def test_decrypt_report_invalid_token(self):
        """Test decryption with wrong key."""
        key = Fernet.generate_key()
        wrong_key = Fernet.generate_key()
        cipher = Fernet(key)
        encrypted_text = cipher.encrypt(b"test").decode()

        with pytest.raises(InvalidToken):
            decrypt_report(encrypted_text, wrong_key)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
