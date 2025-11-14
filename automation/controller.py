"""
Contrôleur d'automation pour les actions souris et clavier
Utilise pydirectinput pour compatibilité avec les jeux
"""

import pydirectinput
import time
import random
import config


class Controller:
    """Contrôleur pour automatiser les actions souris/clavier"""

    def __init__(self):
        """Initialise le contrôleur"""
        # PyDirectInput est plus lent mais fonctionne avec les jeux
        pydirectinput.PAUSE = 0.01  # Réduire le délai entre les commandes

    def click_left(self):
        """Effectue un clic gauche (pour les QTE)"""
        pydirectinput.click()
        if config.LOG_LEVEL == 'DEBUG':
            print("[Controller] Clic gauche effectué")

    def click_right(self):
        """Effectue un clic droit (pour lancer/récupérer la ligne)"""
        pydirectinput.rightClick()
        if config.LOG_LEVEL == 'DEBUG':
            print("[Controller] Clic droit effectué")

    def cast_fishing_rod(self):
        """Lance la ligne de pêche (clic droit)"""
        print("[Action] Lancement de la ligne...")
        self.click_right()
        time.sleep(config.CAST_DELAY)

    def reel_in(self):
        """Récupère la ligne (clic droit quand le poisson mord)"""
        print("[Action] Récupération de la ligne...")
        self.click_right()
        time.sleep(0.05)  # Réduit de 200ms à 50ms pour réaction plus rapide

    def perform_qte_click(self):
        """Effectue le clic pour le QTE (clic gauche)"""
        print("[Action] QTE - Clic!")
        self.click_left()
        time.sleep(config.QTE_REACTION_TIME)

    def wait_random_delay(self):
        """Attend un délai aléatoire pour simuler un comportement humain"""
        if config.RANDOM_DELAY_ENABLED:
            delay = random.uniform(config.RANDOM_DELAY_MIN, config.RANDOM_DELAY_MAX)
            print(f"[Attente] Pause humaine: {delay:.2f}s")
            time.sleep(delay)

    def is_emergency_stop_pressed(self) -> bool:
        """
        Vérifie si la touche d'arrêt d'urgence est pressée

        Returns:
            True si la touche d'arrêt d'urgence est pressée
        """
        import keyboard
        return keyboard.is_pressed(config.EMERGENCY_STOP_KEY)


# Instance globale
_controller_instance = None


def get_controller() -> Controller:
    """
    Obtient l'instance globale du contrôleur

    Returns:
        Instance de Controller
    """
    global _controller_instance
    if _controller_instance is None:
        _controller_instance = Controller()
    return _controller_instance


if __name__ == "__main__":
    # Test du module
    print("Test du contrôleur...")
    print("Le curseur va effectuer quelques actions dans 3 secondes...")

    controller = Controller()

    time.sleep(3)

    print("Test clic gauche...")
    controller.click_left()
    time.sleep(1)

    print("Test clic droit...")
    controller.click_right()
    time.sleep(1)

    print("Test lancement de ligne...")
    controller.cast_fishing_rod()

    print("Tests terminés!")
