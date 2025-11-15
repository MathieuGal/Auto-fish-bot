"""
Détecteur du compteur de QTE "QTE X/Y"
Lit le nombre total de QTE au début et compte les QTE effectués
"""

import cv2
import numpy as np
from typing import Optional, Tuple
import config
import re


class QTECounterDetector:
    """Détecteur du message de compteur de QTE"""

    def __init__(self):
        """Initialise le détecteur"""
        # Couleur du texte "QTE" en HSV (blanc)
        self.white_text_lower = np.array([0, 0, 200])
        self.white_text_upper = np.array([180, 30, 255])

        # Zone de recherche (partie supérieure centre de l'écran)
        # Le message "QTE X/Y" apparaît en haut au centre
        self.search_region_y = (0.05, 0.25)  # 5% à 25% de la hauteur
        self.search_region_x = (0.35, 0.65)  # 35% à 65% de la largeur

        # Variables pour compter les QTE
        self.total_qte_count = None  # Nombre total de QTE (sera détecté au début)
        self.has_detected_total = False  # A-t-on déjà détecté le total?

        # Vérifier si pytesseract est disponible
        self.ocr_available = False
        try:
            import pytesseract
            self.ocr_available = True
            print("[QTECounter] OCR disponible - Lecture du compteur activée!")
        except ImportError:
            print("[QTECounter] OCR non disponible - Utilisera la méthode de fallback")

    def try_read_total_qte_count(self, screen: np.ndarray) -> Optional[int]:
        """
        Essaie de lire le nombre total de QTE dans "QTE X/Y"

        Args:
            screen: Image BGR de l'écran complet

        Returns:
            Le nombre total de QTE (Y dans "QTE X/Y"), ou None si échec
        """
        if not self.ocr_available:
            return None

        try:
            import pytesseract

            height, width = screen.shape[:2]

            # Zone du message QTE
            y1 = int(height * self.search_region_y[0])
            y2 = int(height * self.search_region_y[1])
            x1 = int(width * self.search_region_x[0])
            x2 = int(width * self.search_region_x[1])

            roi = screen[y1:y2, x1:x2]

            # Convertir en niveaux de gris
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

            # Augmenter le contraste pour améliorer l'OCR
            _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

            # Agrandir pour améliorer l'OCR
            binary = cv2.resize(binary, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

            # Lire le texte
            text = pytesseract.image_to_string(binary, config='--psm 7 --oem 3')

            if config.LOG_LEVEL == 'DEBUG':
                print(f"[QTECounter] Texte OCR: '{text}'")

            # Chercher le pattern "QTE X/Y" ou "X/Y"
            # Exemples: "QTE 1/3", "1/3", "QTE 2/5"
            match = re.search(r'(\d+)/(\d+)', text)
            if match:
                current = int(match.group(1))
                total = int(match.group(2))
                print(f"[QTECounter] ✅ Compteur détecté: {current}/{total}")
                return total

            return None

        except Exception as e:
            if config.LOG_LEVEL == 'DEBUG':
                print(f"[QTECounter] Erreur OCR: {e}")
            return None

    def is_qte_message_visible(self, screen: np.ndarray) -> bool:
        """
        Détecte si le message "QTE X/Y" est visible en haut de l'écran

        Args:
            screen: Image BGR de l'écran complet

        Returns:
            True si le message QTE est visible (= QTE en cours)
        """
        try:
            height, width = screen.shape[:2]

            # Définir la zone de recherche (haut-centre)
            y1 = int(height * self.search_region_y[0])
            y2 = int(height * self.search_region_y[1])
            x1 = int(width * self.search_region_x[0])
            x2 = int(width * self.search_region_x[1])

            # Extraire la région d'intérêt
            roi = screen[y1:y2, x1:x2]

            # Convertir en HSV
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            # Créer un masque pour le texte blanc
            mask = cv2.inRange(hsv, self.white_text_lower, self.white_text_upper)

            # Compter les pixels blancs
            white_pixels = cv2.countNonZero(mask)
            total_pixels = roi.shape[0] * roi.shape[1]
            white_ratio = white_pixels / total_pixels

            # Si plus de 1% de pixels blancs, le message est probablement visible
            # (Le texte "QTE X/Y" en blanc est assez visible)
            if white_ratio > 0.01:  # 1%
                if config.LOG_LEVEL == 'DEBUG':
                    print(f"[QTECounter] Message QTE visible! Ratio blanc: {white_ratio:.4f}")
                return True

            if config.LOG_LEVEL == 'DEBUG':
                print(f"[QTECounter] Pas de message QTE. Ratio blanc: {white_ratio:.4f}")
            return False

        except Exception as e:
            if config.LOG_LEVEL == 'DEBUG':
                print(f"[QTECounter] Erreur: {e}")
            return False


# Instance globale
_qte_counter_detector_instance = None


def get_qte_counter_detector() -> QTECounterDetector:
    """
    Obtient l'instance globale du détecteur de compteur QTE

    Returns:
        Instance de QTECounterDetector
    """
    global _qte_counter_detector_instance
    if _qte_counter_detector_instance is None:
        _qte_counter_detector_instance = QTECounterDetector()
    return _qte_counter_detector_instance


if __name__ == "__main__":
    # Test du module
    import time
    from screen_capture import capture_screen

    print("Test du détecteur de compteur QTE...")
    print("Le script va chercher le message 'QTE X/Y' en haut de l'écran")
    print("Appuyez sur Ctrl+C pour arrêter")
    print()

    detector = QTECounterDetector()

    try:
        while True:
            screen = capture_screen()
            visible = detector.is_qte_message_visible(screen)

            if visible:
                print("✅ MESSAGE QTE VISIBLE (QTE en cours)")
            else:
                print("❌ PAS DE MESSAGE (QTE terminés)")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nTest terminé!")
