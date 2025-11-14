"""
Module vision pour le bot de pêche automatique
Contient les détecteurs visuels et la capture d'écran
"""

from .screen_capture import ScreenCapture, get_screen_capture, capture_screen
from .qte_detector import QTEDetector, get_qte_detector
from .fish_detector import FishDetector, get_fish_detector

__all__ = [
    'ScreenCapture',
    'get_screen_capture',
    'capture_screen',
    'QTEDetector',
    'get_qte_detector',
    'FishDetector',
    'get_fish_detector',
]
