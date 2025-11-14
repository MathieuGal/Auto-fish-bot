"""
Détecteur de QTE (Quick Time Events) pour les cercles de pêche
Détecte les cercles rouge (cible) et blanc (curseur) et détermine le timing parfait
"""

import cv2
import numpy as np
from typing import Optional, Tuple, List
import config
from vision.screen_capture import capture_screen


class QTEDetector:
    """Détecteur de QTE pour la pêche"""

    def __init__(self):
        """Initialise le détecteur de QTE"""
        self.last_red_circle = None
        self.last_white_circle = None
        self.debug_image = None

    def detect_circles(self, image: np.ndarray) -> Tuple[Optional[Tuple], Optional[Tuple]]:
        """
        Détecte les cercles rouge et blanc dans l'image

        Args:
            image: Image BGR à analyser

        Returns:
            Tuple (red_circle, white_circle) où chaque cercle est (x, y, radius) ou None
        """
        # Convertir en HSV pour une meilleure détection des couleurs
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Détection du cercle rouge
        red_circle = self._detect_red_circle(hsv, image)

        # Détection du cercle blanc
        white_circle = self._detect_white_circle(hsv, image)

        self.last_red_circle = red_circle
        self.last_white_circle = white_circle

        if config.SHOW_DEBUG_WINDOW:
            self._create_debug_image(image, red_circle, white_circle)

        return red_circle, white_circle

    def _detect_red_circle(self, hsv: np.ndarray, original: np.ndarray) -> Optional[Tuple[int, int, int]]:
        """
        Détecte le cercle rouge (cible)

        Args:
            hsv: Image en HSV
            original: Image originale BGR

        Returns:
            (x, y, radius) ou None
        """
        # Masque pour le rouge (deux plages car le rouge wrap autour dans HSV)
        mask1 = cv2.inRange(hsv,
                           np.array(config.RED_CIRCLE_HSV_LOWER),
                           np.array(config.RED_CIRCLE_HSV_UPPER))
        mask2 = cv2.inRange(hsv,
                           np.array((170, 100, 100)),
                           np.array((180, 255, 255)))
        red_mask = cv2.bitwise_or(mask1, mask2)

        # Nettoyer le masque
        kernel = np.ones((5, 5), np.uint8)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

        # Détecter les contours
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None

        # Trouver le plus grand contour circulaire
        largest_circle = None
        max_area = 0

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 100:  # Ignorer les petits contours
                continue

            # Approximer le contour par un cercle
            ((x, y), radius) = cv2.minEnclosingCircle(contour)

            # Vérifier si c'est assez circulaire
            circularity = 4 * np.pi * area / (cv2.arcLength(contour, True) ** 2)
            if circularity > 0.7 and area > max_area:
                max_area = area
                largest_circle = (int(x), int(y), int(radius))

        return largest_circle

    def _detect_white_circle(self, hsv: np.ndarray, original: np.ndarray) -> Optional[Tuple[int, int, int]]:
        """
        Détecte le cercle blanc (curseur qui se referme)

        Args:
            hsv: Image en HSV
            original: Image originale BGR

        Returns:
            (x, y, radius) ou None
        """
        # Masque pour le blanc
        white_mask = cv2.inRange(hsv,
                                np.array(config.WHITE_CIRCLE_HSV_LOWER),
                                np.array(config.WHITE_CIRCLE_HSV_UPPER))

        # Nettoyer le masque
        kernel = np.ones((3, 3), np.uint8)
        white_mask = cv2.morphologyEx(white_mask, cv2.MORPH_CLOSE, kernel)

        # Détecter les cercles avec Hough Transform
        circles = cv2.HoughCircles(
            white_mask,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=50,
            param1=50,
            param2=15,
            minRadius=10,
            maxRadius=100
        )

        if circles is None:
            return None

        # Prendre le premier cercle détecté
        circles = np.round(circles[0, :]).astype("int")
        if len(circles) > 0:
            x, y, r = circles[0]
            return (x, y, r)

        return None

    def is_qte_ready(self, red_circle: Optional[Tuple], white_circle: Optional[Tuple]) -> bool:
        """
        Vérifie si les cercles sont alignés (moment parfait pour cliquer)

        Args:
            red_circle: Position du cercle rouge (x, y, radius)
            white_circle: Position du cercle blanc (x, y, radius)

        Returns:
            True si c'est le moment de cliquer
        """
        if red_circle is None or white_circle is None:
            return False

        red_x, red_y, red_r = red_circle
        white_x, white_y, white_r = white_circle

        # Calculer la distance entre les centres
        distance = np.sqrt((red_x - white_x)**2 + (red_y - white_y)**2)

        # Calculer la différence de rayon
        radius_diff = abs(red_r - white_r)

        # Les cercles sont alignés si:
        # 1. Les centres sont proches (distance < 20 pixels)
        # 2. Les rayons sont similaires (diff < 10 pixels)
        centers_aligned = distance < 20
        radii_similar = radius_diff < 10

        return centers_aligned and radii_similar

    def wait_for_qte(self, timeout: float = 5.0) -> bool:
        """
        Attend qu'un QTE apparaisse et soit prêt

        Args:
            timeout: Temps d'attente maximum en secondes

        Returns:
            True si le QTE est détecté et prêt, False si timeout
        """
        import time
        start_time = time.time()

        while (time.time() - start_time) < timeout:
            # Capturer l'écran
            screen = capture_screen(config.QTE_DETECTION_REGION)

            # Détecter les cercles
            red, white = self.detect_circles(screen)

            # Vérifier si c'est prêt
            if self.is_qte_ready(red, white):
                return True

            # Petit délai pour ne pas surcharger le CPU
            time.sleep(0.01)

        return False

    def _create_debug_image(self, image: np.ndarray, red_circle: Optional[Tuple], white_circle: Optional[Tuple]):
        """
        Crée une image de debug avec les cercles détectés

        Args:
            image: Image originale
            red_circle: Cercle rouge détecté
            white_circle: Cercle blanc détecté
        """
        debug_img = image.copy()

        # Dessiner le cercle rouge
        if red_circle is not None:
            x, y, r = red_circle
            cv2.circle(debug_img, (x, y), r, (0, 0, 255), 2)
            cv2.circle(debug_img, (x, y), 2, (0, 0, 255), 3)
            cv2.putText(debug_img, "RED TARGET", (x - 50, y - r - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Dessiner le cercle blanc
        if white_circle is not None:
            x, y, r = white_circle
            cv2.circle(debug_img, (x, y), r, (255, 255, 255), 2)
            cv2.circle(debug_img, (x, y), 2, (255, 255, 255), 3)
            cv2.putText(debug_img, "WHITE CURSOR", (x - 50, y + r + 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Indiquer si c'est le moment de cliquer
        if self.is_qte_ready(red_circle, white_circle):
            cv2.putText(debug_img, "CLICK NOW!", (50, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        self.debug_image = debug_img

    def show_debug_window(self):
        """Affiche la fenêtre de debug"""
        if self.debug_image is not None:
            # Redimensionner pour l'affichage
            scale = config.DEBUG_WINDOW_SCALE
            width = int(self.debug_image.shape[1] * scale)
            height = int(self.debug_image.shape[0] * scale)
            resized = cv2.resize(self.debug_image, (width, height))

            cv2.imshow("QTE Detection Debug", resized)
            cv2.waitKey(1)


# Instance globale
_qte_detector_instance = None


def get_qte_detector() -> QTEDetector:
    """
    Obtient l'instance globale du détecteur de QTE

    Returns:
        Instance de QTEDetector
    """
    global _qte_detector_instance
    if _qte_detector_instance is None:
        _qte_detector_instance = QTEDetector()
    return _qte_detector_instance


if __name__ == "__main__":
    # Test du module
    print("Test du détecteur de QTE...")
    print("Activez le mode debug dans config.py pour voir la détection en temps réel")

    detector = QTEDetector()

    # Capturer quelques frames pour tester
    import time
    for i in range(100):
        screen = capture_screen()
        red, white = detector.detect_circles(screen)

        print(f"Frame {i}: Red={red}, White={white}, Ready={detector.is_qte_ready(red, white)}")

        if config.SHOW_DEBUG_WINDOW:
            detector.show_debug_window()

        time.sleep(0.1)

    cv2.destroyAllWindows()
