"""
Détecteur de message de succès de pêche
Détecte le message "PÊCHE Vous avez pêché..." qui apparaît après les QTE
"""

import cv2
import numpy as np
from typing import Optional
import config


class SuccessDetector:
    """Détecteur de message de succès de pêche"""

    def __init__(self):
        """Initialise le détecteur de succès"""
        # Couleur du texte "PÊCHE" en HSV (cyan/turquoise)
        # Le texte "PÊCHE" est en cyan distinctif
        self.peche_text_lower = np.array([80, 100, 100])   # Cyan/turquoise
        self.peche_text_upper = np.array([100, 255, 255])

        # Zone de recherche (partie supérieure centrale de l'écran)
        # Le message apparaît généralement au centre-haut
        self.search_region_y = (0.2, 0.5)  # 20% à 50% de la hauteur
        self.search_region_x = (0.3, 0.7)  # 30% à 70% de la largeur

    def detect_success_message(self, screen: np.ndarray) -> bool:
        """
        Détecte le message de succès "PÊCHE Vous avez pêché..."

        Args:
            screen: Image BGR de l'écran

        Returns:
            True si le message de succès est détecté
        """
        try:
            height, width = screen.shape[:2]

            # Définir la zone de recherche (centre-haut de l'écran)
            y1 = int(height * self.search_region_y[0])
            y2 = int(height * self.search_region_y[1])
            x1 = int(width * self.search_region_x[0])
            x2 = int(width * self.search_region_x[1])

            # Extraire la région d'intérêt
            roi = screen[y1:y2, x1:x2]

            # Convertir en HSV
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            # Créer un masque pour la couleur cyan du texte "PÊCHE"
            mask = cv2.inRange(hsv, self.peche_text_lower, self.peche_text_upper)

            # Compter les pixels cyan
            cyan_pixels = cv2.countNonZero(mask)
            total_pixels = roi.shape[0] * roi.shape[1]
            cyan_ratio = cyan_pixels / total_pixels

            # Si plus de 0.8% de pixels cyan, c'est probablement le message "PÊCHE"
            # (Le texte "PÊCHE" en cyan est assez visible)
            # Seuil augmenté pour éviter les faux positifs
            if cyan_ratio > 0.008:  # 0.8% (plus strict)
                if config.LOG_LEVEL == 'DEBUG':
                    print(f"[SuccessDetector] Texte cyan détecté! Ratio: {cyan_ratio:.4f}")
                return True

            return False

        except Exception as e:
            if config.LOG_LEVEL == 'DEBUG':
                print(f"[SuccessDetector] Erreur: {e}")
            return False

    def detect_success_in_chat(self, screen: np.ndarray) -> bool:
        """
        Détecte le message de succès dans le chat (alternative)
        Le message "PÊCHE Félicitations!" apparaît aussi dans le chat en bas à gauche

        Args:
            screen: Image BGR de l'écran

        Returns:
            True si le message est détecté dans le chat
        """
        try:
            height, width = screen.shape[:2]

            # Zone du chat (bas gauche)
            chat_y1 = int(height * 0.7)   # 70% de la hauteur
            chat_y2 = int(height * 0.95)  # 95% de la hauteur
            chat_x1 = 0
            chat_x2 = int(width * 0.3)    # 30% de la largeur

            # Extraire la région du chat
            chat_roi = screen[chat_y1:chat_y2, chat_x1:chat_x2]

            # Convertir en HSV
            hsv = cv2.cvtColor(chat_roi, cv2.COLOR_BGR2HSV)

            # Chercher le texte cyan "PÊCHE" dans le chat
            mask = cv2.inRange(hsv, self.peche_text_lower, self.peche_text_upper)

            # Compter les pixels
            cyan_pixels = cv2.countNonZero(mask)
            total_pixels = chat_roi.shape[0] * chat_roi.shape[1]
            cyan_ratio = cyan_pixels / total_pixels

            # Seuil plus bas pour le chat car le texte est plus petit
            if cyan_ratio > 0.001:  # 0.1%
                if config.LOG_LEVEL == 'DEBUG':
                    print(f"[SuccessDetector] Message dans le chat détecté! Ratio: {cyan_ratio:.4f}")
                return True

            return False

        except Exception as e:
            if config.LOG_LEVEL == 'DEBUG':
                print(f"[SuccessDetector] Erreur (chat): {e}")
            return False

    def is_fishing_complete(self, screen: np.ndarray) -> bool:
        """
        Vérifie si la pêche est terminée en cherchant le message de succès

        Args:
            screen: Image BGR de l'écran

        Returns:
            True si la pêche est terminée (message détecté)
        """
        # Vérifier le message principal (centre-haut)
        if self.detect_success_message(screen):
            return True

        # Vérifier aussi dans le chat (fallback)
        if self.detect_success_in_chat(screen):
            return True

        return False


# Instance globale
_success_detector_instance = None


def get_success_detector() -> SuccessDetector:
    """
    Obtient l'instance globale du détecteur de succès

    Returns:
        Instance de SuccessDetector
    """
    global _success_detector_instance
    if _success_detector_instance is None:
        _success_detector_instance = SuccessDetector()
    return _success_detector_instance


if __name__ == "__main__":
    # Test du module
    import time
    from screen_capture import capture_screen

    print("Test du détecteur de message de succès...")
    print("Le script va capturer l'écran en continu et chercher le message 'PÊCHE'")
    print("Appuyez sur Ctrl+C pour arrêter")
    print()

    detector = SuccessDetector()

    try:
        while True:
            screen = capture_screen()
            success = detector.is_fishing_complete(screen)

            if success:
                print("✅ MESSAGE DE SUCCÈS DÉTECTÉ!")
            else:
                print("⚪ Pas de message détecté")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nTest terminé!")
