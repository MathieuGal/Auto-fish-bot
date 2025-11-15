"""
Point d'entrée principal du Bot de Pêche Automatique Minecraft
"""

import sys
import time
import keyboard
from colorama import Fore, Style, init
import config
from fishing_bot import get_fishing_bot

# Vérifier la version de Python
PYTHON_MIN_VERSION = (3, 10)
PYTHON_MAX_VERSION = (3, 12)

if sys.version_info < PYTHON_MIN_VERSION:
    print(f"{Fore.RED}ERREUR: Python {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}+ requis!")
    print(f"{Fore.YELLOW}Vous utilisez Python {sys.version_info.major}.{sys.version_info.minor}")
    print(f"{Fore.CYAN}Téléchargez Python 3.11 depuis: https://www.python.org/downloads/")
    sys.exit(1)

if sys.version_info[:2] > PYTHON_MAX_VERSION:
    print(f"{Fore.YELLOW}ATTENTION: Python {sys.version_info.major}.{sys.version_info.minor} n'est pas testé!")
    print(f"{Fore.YELLOW}Version recommandée: Python 3.10 - 3.12")
    print(f"{Fore.CYAN}Le bot peut fonctionner mais certaines dépendances peuvent échouer...")
    print()

# Initialiser colorama
init(autoreset=True)


def print_banner():
    """Affiche la bannière du bot"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        Bot de Pêche Automatique Minecraft v1.0          ║
║                                                          ║
║    Système de QTE automatique avec détection visuelle   ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def print_instructions():
    """Affiche les instructions d'utilisation"""
    print(f"{Fore.YELLOW}Instructions:")
    print(f"  1. Lancez Minecraft et rejoignez votre serveur")
    print(f"  2. Équipez votre canne à pêche")
    print(f"  3. Placez-vous devant l'eau")
    print(f"  4. Appuyez sur '{config.START_STOP_KEY.upper()}' pour démarrer le bot")
    print(f"  5. Appuyez sur '{config.START_STOP_KEY.upper()}' pour arrêter le bot (même touche!)")
    print()

    print(f"{Fore.CYAN}Configuration:")
    print(f"  Lancer ligne: {Fore.GREEN}{config.CAST_BUTTON.upper()} (Clic droit)")
    print(f"  Récupérer: {Fore.GREEN}{config.REEL_BUTTON.upper()} (Clic droit)")
    print(f"  QTE: {Fore.GREEN}{config.QTE_BUTTON.upper()} (Clic gauche)")
    print(f"  Détection visuelle: {Fore.GREEN}Activée")

    if config.AUDIO_DETECTION_ENABLED:
        print(f"  Détection audio: {Fore.GREEN}Activée")
    else:
        print(f"  Détection audio: {Fore.RED}Désactivée")

    if config.SHOW_DEBUG_WINDOW:
        print(f"  Mode debug: {Fore.GREEN}Activé")

    if config.AUTO_STOP_AFTER > 0:
        print(f"  Arrêt automatique: {Fore.YELLOW}{config.AUTO_STOP_AFTER} poissons")

    print()


def wait_for_start():
    """Attend que l'utilisateur appuie sur la touche de démarrage"""
    print(f"{Fore.GREEN}Appuyez sur '{config.START_STOP_KEY.upper()}' pour démarrer...")

    while True:
        if keyboard.is_pressed(config.START_STOP_KEY):
            print(f"{Fore.GREEN}Démarrage dans 3 secondes...")
            time.sleep(0.5)  # Éviter les doubles pressions
            for i in range(3, 0, -1):
                print(f"{Fore.YELLOW}{i}...")
                time.sleep(1)
            return
        time.sleep(0.1)


def main():
    """Fonction principale"""
    try:
        # Afficher la bannière
        print_banner()

        # Afficher les instructions
        print_instructions()

        # Attendre le démarrage
        wait_for_start()

        # Créer et démarrer le bot
        bot = get_fishing_bot()
        bot.start()

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Arrêt par l'utilisateur...")
    except Exception as e:
        print(f"\n{Fore.RED}Erreur critique: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print(f"\n{Fore.CYAN}Au revoir!")
        time.sleep(2)


if __name__ == "__main__":
    main()
