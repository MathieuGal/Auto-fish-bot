"""
Détecteur de morsure de poisson
Détecte visuellement quand un poisson mord à l'hameçon
"""

import cv2
import numpy as np
from typing import Optional
import time
import config
from vision.screen_capture import capture_screen


class FishDetector:
    """Détecteur de morsure de poisson"""

    def __init__(self):
        """Initialise le détecteur"""
        self.baseline_frame = None
        self.last_detection_time = None

    def set_baseline(self):
        """
        Capture une frame de référence (après avoir lancé la ligne)
        """
        screen = capture_screen(config.SCREEN_REGION)
        self.baseline_frame = screen.copy()

    def detect_bite(self, threshold: float = None) -> bool:
        """
        Détecte si un poisson a mordu en comparant avec la baseline

        Args:
            threshold: Seuil de différence pour détecter un changement (0-1)
                      Si None, utilise config.BITE_DETECTION_THRESHOLD

        Returns:
            True si une morsure est détectée
        """
        if threshold is None:
            threshold = config.BITE_DETECTION_THRESHOLD
        if self.baseline_frame is None:
            return False

        # Capturer la frame actuelle
        current_frame = capture_screen(config.SCREEN_REGION)

        # Calculer la différence
        difference = self._calculate_frame_difference(self.baseline_frame, current_frame)

        # Logger les valeurs si en mode DEBUG
        if config.LOG_LEVEL == 'DEBUG':
            print(f"[FishDetector] Différence: {difference:.3f} / Seuil: {threshold:.3f}")

        # Détecter si la différence dépasse le seuil
        if difference > threshold:
            self.last_detection_time = time.time()
            print(f"[FishDetector] Morsure détectée! Différence: {difference:.3f} > Seuil: {threshold:.3f}")
            return True

        return False

    def _calculate_frame_difference(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        """
        Calcule la différence entre deux frames

        Args:
            frame1: Première frame
            frame2: Deuxième frame

        Returns:
            Score de différence (0-1)
        """
        # Convertir en niveaux de gris
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # Calculer la différence absolue
        diff = cv2.absdiff(gray1, gray2)

        # Appliquer un seuil
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # Calculer le pourcentage de pixels différents
        total_pixels = thresh.shape[0] * thresh.shape[1]
        changed_pixels = np.sum(thresh == 255)
        difference_ratio = changed_pixels / total_pixels

        return difference_ratio

    def wait_for_bite(self, timeout: float = None) -> bool:
        """
        Attend qu'un poisson morde

        Args:
            timeout: Temps d'attente maximum en secondes (None = infini)

        Returns:
            True si une morsure est détectée, False si timeout
        """
        if timeout is None:
            timeout = config.MAX_WAIT_FOR_BITE

        start_time = time.time()

        # Définir la baseline
        self.set_baseline()
        time.sleep(2.0)  # Attendre que tout se stabilise (augmenté pour éviter faux positifs)

        print(f"En attente d'une morsure (timeout: {timeout}s)...")

        while (time.time() - start_time) < timeout:
            # Vérifier la morsure
            if self.detect_bite():
                print("Morsure détectée!")
                return True

            # Petit délai pour ne pas surcharger le CPU
            time.sleep(config.BITE_CHECK_INTERVAL)

        print("Timeout: aucune morsure détectée")
        return False

    def detect_bite_with_particle_detection(self) -> bool:
        """
        Détection alternative basée sur les particules d'eau
        (Les mods Minecraft affichent souvent des particules quand un poisson mord)

        Returns:
            True si des particules sont détectées
        """
        # Capturer la frame actuelle
        current_frame = capture_screen(config.SCREEN_REGION)

        # Convertir en HSV
        hsv = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)

        # Détecter les particules bleues/blanches (eau)
        # Plage pour les particules d'eau
        lower_particle = np.array([90, 50, 200])
        upper_particle = np.array([130, 255, 255])

        # Créer le masque
        mask = cv2.inRange(hsv, lower_particle, upper_particle)

        # Compter les pixels détectés
        particle_pixels = np.sum(mask == 255)

        # Seuil pour considérer qu'il y a assez de particules
        if particle_pixels > 100:
            return True

        return False


# Instance globale
_fish_detector_instance = None


def get_fish_detector() -> FishDetector:
    """
    Obtient l'instance globale du détecteur de poisson

    Returns:
        Instance de FishDetector
    """
    global _fish_detector_instance
    if _fish_detector_instance is None:
        _fish_detector_instance = FishDetector()
    return _fish_detector_instance


if __name__ == "__main__":
    # Test du module
    print("Test du détecteur de morsure...")
    print("Lancez Minecraft et préparez-vous à pêcher!")

    detector = FishDetector()

    # Attendre une morsure
    if detector.wait_for_bite(timeout=30):
        print("Poisson détecté!")
    else:
        print("Aucun poisson détecté dans les 30 secondes")
