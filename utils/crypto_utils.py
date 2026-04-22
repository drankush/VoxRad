"""Utility functions for encryption and decryption operations."""

import os
import tempfile
from cryptography.fernet import Fernet
from config.config import config
import logging

logger = logging.getLogger(__name__)


def decrypt_audio_file(encrypted_audio_path, decryption_key, audio_format=".mp3"):
    """
    Decrypt an encrypted audio file and return the path to a temporary decrypted file.

    Args:
        encrypted_audio_path: Path to the encrypted audio file
        decryption_key: Fernet key for decryption
        audio_format: File extension for the temporary decrypted file

    Returns:
        Path to the temporary decrypted file, or None if decryption fails

    Raises:
        FileNotFoundError: If encrypted file doesn't exist
        cryptography.fernet.InvalidToken: If decryption fails
    """
    try:
        cipher_suite = Fernet(decryption_key)

        with open(encrypted_audio_path, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()

        decrypted_data = cipher_suite.decrypt(encrypted_data)

        with tempfile.NamedTemporaryFile(suffix=audio_format, delete=False) as tmp_file:
            tmp_file.write(decrypted_data)
            decrypted_path = tmp_file.name

        logger.debug(f"Successfully decrypted audio file to {decrypted_path}")
        return decrypted_path

    except FileNotFoundError as e:
        logger.error(f"Encrypted audio file not found: {encrypted_audio_path}")
        raise
    except Exception as e:
        logger.error(f"Failed to decrypt audio file: {e}")
        raise


def cleanup_temp_file(file_path):
    """
    Safely remove a temporary file if it exists.

    Args:
        file_path: Path to the file to remove
    """
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
            logger.debug(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to clean up temporary file {file_path}: {e}")


def encrypt_and_store_report(report_text):
    """
    Encrypt a report and store it in the config.

    Args:
        report_text: The plain text report to encrypt

    Returns:
        Tuple of (encrypted_report, encryption_key) as strings
    """
    try:
        report_key = Fernet.generate_key()
        report_cipher = Fernet(report_key)
        encrypted_report = report_cipher.encrypt(report_text.encode()).decode()

        config.current_encrypted_report = encrypted_report
        config.current_report_encryption_key = report_key.decode()

        logger.debug("Report encrypted and stored in config")
        return encrypted_report, report_key.decode()

    except Exception as e:
        logger.error(f"Failed to encrypt report: {e}")
        raise


def decrypt_report(encrypted_report, encryption_key):
    """
    Decrypt an encrypted report.

    Args:
        encrypted_report: Encrypted report string
        encryption_key: Fernet key for decryption

    Returns:
        Decrypted report text

    Raises:
        cryptography.fernet.InvalidToken: If decryption fails
    """
    try:
        cipher_suite = Fernet(encryption_key.encode() if isinstance(encryption_key, str) else encryption_key)
        decrypted_report = cipher_suite.decrypt(encrypted_report.encode()).decode()
        return decrypted_report

    except Exception as e:
        logger.error(f"Failed to decrypt report: {e}")
        raise
