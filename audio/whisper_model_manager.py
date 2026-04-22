"""Singleton manager for caching Whisper model to avoid repeated loading."""

import logging
from typing import Optional
from faster_whisper import WhisperModel
from config.config import config

logger = logging.getLogger(__name__)


class WhisperModelManager:
    """Manages a cached instance of the Whisper model."""

    _instance: Optional['WhisperModelManager'] = None
    _model: Optional[WhisperModel] = None
    _current_model_size: Optional[str] = None
    _current_device: Optional[str] = None
    _current_compute_type: Optional[str] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WhisperModelManager, cls).__new__(cls)
        return cls._instance

    def get_model(self, force_reload: bool = False) -> WhisperModel:
        """
        Get the cached Whisper model, loading it if necessary.

        Args:
            force_reload: Force reload the model even if already cached

        Returns:
            WhisperModel instance
        """
        model_size = getattr(config, 'WHISPER_MODEL_SIZE', 'base')
        device = 'auto'
        compute_type = getattr(config, 'WHISPER_QUANTIZATION', 'auto')

        needs_reload = (
            force_reload or
            self._model is None or
            self._current_model_size != model_size or
            self._current_device != device or
            self._current_compute_type != compute_type
        )

        if needs_reload:
            logger.info(f"Loading Whisper model: size={model_size}, device={device}, compute_type={compute_type}")
            self._model = WhisperModel(
                model_size,
                device=device,
                compute_type=compute_type
            )
            self._current_model_size = model_size
            self._current_device = device
            self._current_compute_type = compute_type
            logger.info("Whisper model loaded successfully")

        return self._model

    def unload_model(self):
        """Unload the cached model to free memory."""
        if self._model is not None:
            logger.info("Unloading cached Whisper model")
            self._model = None
            self._current_model_size = None
            self._current_device = None
            self._current_compute_type = None

    @classmethod
    def get_singleton(cls) -> 'WhisperModelManager':
        """Get or create the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def get_whisper_model(force_reload: bool = False) -> WhisperModel:
    """
    Convenience function to get the cached Whisper model.

    Args:
        force_reload: Force reload the model

    Returns:
        WhisperModel instance
    """
    manager = WhisperModelManager.get_singleton()
    return manager.get_model(force_reload=force_reload)
