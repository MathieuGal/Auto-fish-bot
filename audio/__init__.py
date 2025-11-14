"""
Module audio pour le bot de pêche automatique
Détection audio des morsures de poisson
"""

from .sound_detector import SoundDetector, get_sound_detector

__all__ = [
    'SoundDetector',
    'get_sound_detector',
]
