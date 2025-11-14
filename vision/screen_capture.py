"""
Module de capture d'écran ultra-rapide pour le bot de pêche
Utilise mss pour des performances optimales
"""

import mss
import numpy as np
import cv2
from typing import Optional, Tuple
import config


class ScreenCapture:
    """Gestionnaire de capture d'écran optimisé"""

    def __init__(self):
        """Initialise le captureur d'écran"""
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]  # Écran principal

    def capture(self, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """
        Capture une région de l'écran

        Args:
            region: Tuple (x, y, width, height) ou None pour plein écran

        Returns:
            Image sous forme de tableau numpy (BGR format pour OpenCV)
        """
        if region is None:
            # Plein écran
            monitor = self.monitor
        else:
            # Région spécifique
            x, y, width, height = region
            monitor = {
                "top": y,
                "left": x,
                "width": width,
                "height": height
            }

        # Capture l'écran
        screenshot = self.sct.grab(monitor)

        # Convertit en numpy array (BGRA)
        img = np.array(screenshot)

        # Convertit de BGRA à BGR (format OpenCV)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        return img

    def capture_gray(self, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """
        Capture une région de l'écran en niveaux de gris

        Args:
            region: Tuple (x, y, width, height) ou None pour plein écran

        Returns:
            Image en niveaux de gris
        """
        img = self.capture(region)
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def get_screen_size(self) -> Tuple[int, int]:
        """
        Obtient la taille de l'écran

        Returns:
            Tuple (width, height)
        """
        return (self.monitor["width"], self.monitor["height"])

    def close(self):
        """Ferme le captureur d'écran"""
        self.sct.close()


# Instance globale pour réutilisation
_screen_capture_instance = None


def get_screen_capture() -> ScreenCapture:
    """
    Obtient l'instance globale du captureur d'écran

    Returns:
        Instance de ScreenCapture
    """
    global _screen_capture_instance
    if _screen_capture_instance is None:
        _screen_capture_instance = ScreenCapture()
    return _screen_capture_instance


def capture_screen(region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
    """
    Fonction helper pour capturer rapidement l'écran

    Args:
        region: Tuple (x, y, width, height) ou None pour plein écran

    Returns:
        Image capturée
    """
    return get_screen_capture().capture(region)


if __name__ == "__main__":
    # Test du module
    print("Test de capture d'écran...")

    sc = ScreenCapture()
    print(f"Taille de l'écran: {sc.get_screen_size()}")

    # Capture plein écran
    img = sc.capture()
    print(f"Image capturée: {img.shape}")

    # Sauvegarde pour test
    cv2.imwrite("test_capture.jpg", img)
    print("Image sauvegardée dans test_capture.jpg")

    sc.close()
