"""
Bot de pêche automatique pour Minecraft
Logique principale qui orchestre toutes les actions
"""

import time
import config
from vision.fish_detector import get_fish_detector
from vision.qte_detector import get_qte_detector
from vision.screen_capture import capture_screen
from automation.controller import get_controller
from colorama import Fore, Style, init

# Détection audio (si activée)
if config.AUDIO_DETECTION_ENABLED:
    from audio.sound_detector import get_sound_detector

# Initialiser colorama pour les couleurs dans le terminal
init(autoreset=True)


class FishingBot:
    """Bot principal de pêche automatique"""

    def __init__(self):
        """Initialise le bot"""
        # Détecteurs
        self.fish_detector = get_fish_detector()
        self.qte_detector = get_qte_detector()
        self.controller = get_controller()

        # Détection audio si activée
        if config.AUDIO_DETECTION_ENABLED:
            self.sound_detector = get_sound_detector()
        else:
            self.sound_detector = None

        self.is_running = False
        self.fish_caught = 0
        self.qte_success = 0
        self.qte_failed = 0
        self.start_time = None

    def start(self):
        """Démarre le bot"""
        self.is_running = True
        self.start_time = time.time()

        print(f"{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}Bot de Pêche Automatique Minecraft - Démarré")
        print(f"{Fore.GREEN}{'='*60}")

        # Afficher le mode de détection
        if config.AUDIO_DETECTION_ENABLED:
            print(f"{Fore.CYAN}Mode: 🔊 Détection AUDIO (plus fiable!)")
            print(f"{Fore.YELLOW}Assurez-vous que le son de Minecraft est activé!")
        else:
            print(f"{Fore.CYAN}Mode: 👁️  Détection VISUELLE")

        print(f"{Fore.YELLOW}Appuyez sur '{config.EMERGENCY_STOP_KEY}' pour arrêter d'urgence")
        print()

        try:
            while self.is_running:
                # Vérifier l'arrêt d'urgence
                if self.controller.is_emergency_stop_pressed():
                    print(f"{Fore.RED}\nArrêt d'urgence détecté!")
                    break

                # Vérifier la limite d'auto-stop
                if config.AUTO_STOP_AFTER > 0 and self.fish_caught >= config.AUTO_STOP_AFTER:
                    print(f"{Fore.GREEN}\nObjectif atteint: {self.fish_caught} poissons pêchés!")
                    break

                # Cycle de pêche complet
                success = self.fishing_cycle()

                if success:
                    self.fish_caught += 1
                    print(f"{Fore.GREEN}Poisson #{self.fish_caught} attrapé avec succès!")

                    # Afficher les stats
                    if config.ENABLE_STATS and self.fish_caught % config.STATS_DISPLAY_INTERVAL == 0:
                        self.display_stats()

                # Pause humaine entre les cycles
                self.controller.wait_random_delay()

        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}\nInterruption par l'utilisateur")
        finally:
            self.stop()

    def stop(self):
        """Arrête le bot"""
        self.is_running = False

        # Arrêter le détecteur audio si actif
        if config.AUDIO_DETECTION_ENABLED and self.sound_detector:
            self.sound_detector.stop_listening()

        self.display_final_stats()

    def fishing_cycle(self) -> bool:
        """
        Exécute un cycle complet de pêche

        Returns:
            True si le cycle s'est terminé avec succès
        """
        try:
            # Étape 1: Lancer la ligne
            print(f"{Fore.CYAN}[1/4] Lancement de la ligne...")
            self.controller.cast_fishing_rod()

            # Étape 2: Attendre qu'un poisson morde
            print(f"{Fore.CYAN}[2/4] En attente d'une morsure...")

            # Utiliser la détection audio ou visuelle selon la config
            if config.AUDIO_DETECTION_ENABLED and self.sound_detector:
                bite_detected = self.sound_detector.wait_for_bite()
            else:
                bite_detected = self.fish_detector.wait_for_bite()

            if not bite_detected:
                print(f"{Fore.YELLOW}Aucune morsure détectée (timeout)")
                return False

            # Étape 3: Récupérer la ligne
            print(f"{Fore.CYAN}[3/4] Récupération de la ligne...")
            self.controller.reel_in()

            # Petit délai pour que les QTE apparaissent (réduit pour réaction plus rapide)
            time.sleep(0.1)  # Réduit de 300ms à 100ms

            # Étape 4: Exécuter les QTE (entre 1 et 6 QTE)
            print(f"{Fore.CYAN}[4/4] Exécution des QTE...")
            qte_success = self.handle_qte_sequence()

            return qte_success

        except Exception as e:
            print(f"{Fore.RED}Erreur dans le cycle de pêche: {e}")
            return False

    def handle_qte_sequence(self, max_qte: int = 6, qte_timeout: float = 3.0) -> bool:
        """
        Gère la séquence de QTE (1 à 6 QTE possibles)

        Args:
            max_qte: Nombre maximum de QTE possible
            qte_timeout: Timeout pour chaque QTE

        Returns:
            True si tous les QTE ont été réussis
        """
        qte_count = 0
        consecutive_failures = 0

        print(f"{Fore.MAGENTA}  QTE: En attente des cercles...")

        while qte_count < max_qte:
            # Vérifier l'arrêt d'urgence
            if self.controller.is_emergency_stop_pressed():
                return False

            # Capturer l'écran
            screen = capture_screen(config.QTE_DETECTION_REGION)

            # Détecter les cercles
            red_circle, white_circle = self.qte_detector.detect_circles(screen)

            # Afficher la fenêtre de debug si activée
            if config.SHOW_DEBUG_WINDOW:
                self.qte_detector.show_debug_window()

            # Vérifier si les cercles sont présents
            if red_circle is None:
                # Plus de QTE, on a terminé
                if qte_count > 0:
                    print(f"{Fore.GREEN}  QTE: Séquence terminée ({qte_count} QTE réussis)")
                    return True
                else:
                    # Aucun QTE détecté
                    consecutive_failures += 1
                    if consecutive_failures > 30:  # 3 secondes à 100ms par check
                        print(f"{Fore.YELLOW}  QTE: Aucun cercle détecté")
                        return False
                    time.sleep(0.1)
                    continue

            # Vérifier si c'est le moment de cliquer
            if self.qte_detector.is_qte_ready(red_circle, white_circle):
                # CLIC GAUCHE pour le QTE!
                self.controller.perform_qte_click()
                qte_count += 1
                self.qte_success += 1
                print(f"{Fore.GREEN}  QTE #{qte_count}: Réussi!")

                # Attendre que le QTE disparaisse avant de chercher le suivant
                time.sleep(config.POST_QTE_DELAY)
                consecutive_failures = 0
            else:
                # Continuer à surveiller
                time.sleep(0.005)  # Check ultra rapide (5ms - optimisé)

        print(f"{Fore.GREEN}  QTE: Tous les QTE terminés ({qte_count}/{max_qte})")
        return True

    def display_stats(self):
        """Affiche les statistiques actuelles"""
        elapsed_time = time.time() - self.start_time
        fish_per_hour = (self.fish_caught / elapsed_time) * 3600 if elapsed_time > 0 else 0

        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Statistiques")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"  Poissons attrapés: {Fore.GREEN}{self.fish_caught}")
        print(f"  QTE réussis: {Fore.GREEN}{self.qte_success}")
        print(f"  QTE ratés: {Fore.RED}{self.qte_failed}")
        print(f"  Temps écoulé: {Fore.YELLOW}{int(elapsed_time//60)}m {int(elapsed_time%60)}s")
        print(f"  Poissons/heure: {Fore.YELLOW}{fish_per_hour:.1f}")
        print(f"{Fore.CYAN}{'='*60}\n")

    def display_final_stats(self):
        """Affiche les statistiques finales"""
        if self.start_time is None:
            return

        elapsed_time = time.time() - self.start_time

        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}Bot arrêté - Statistiques finales")
        print(f"{Fore.GREEN}{'='*60}")
        print(f"  Poissons attrapés: {Fore.GREEN}{self.fish_caught}")
        print(f"  QTE réussis: {Fore.GREEN}{self.qte_success}")
        print(f"  QTE ratés: {Fore.RED}{self.qte_failed}")
        print(f"  Durée totale: {Fore.YELLOW}{int(elapsed_time//60)}m {int(elapsed_time%60)}s")

        if self.fish_caught > 0:
            avg_time = elapsed_time / self.fish_caught
            fish_per_hour = (self.fish_caught / elapsed_time) * 3600
            print(f"  Temps moyen/poisson: {Fore.YELLOW}{avg_time:.1f}s")
            print(f"  Poissons/heure: {Fore.YELLOW}{fish_per_hour:.1f}")

        print(f"{Fore.GREEN}{'='*60}\n")


# Instance globale
_fishing_bot_instance = None


def get_fishing_bot() -> FishingBot:
    """
    Obtient l'instance globale du bot de pêche

    Returns:
        Instance de FishingBot
    """
    global _fishing_bot_instance
    if _fishing_bot_instance is None:
        _fishing_bot_instance = FishingBot()
    return _fishing_bot_instance


if __name__ == "__main__":
    # Test du bot
    print("Démarrage du bot de pêche...")
    print("Assurez-vous que Minecraft est ouvert et que vous êtes devant l'eau!")
    print("Le bot démarrera dans 5 secondes...")

    time.sleep(5)

    bot = FishingBot()
    bot.start()
