"""
Configuration pour le bot de pêche automatique Minecraft
"""

# ==================== CONTRÔLES ====================
# IMPORTANT: Clic DROIT pour lancer la ligne et quand le poisson mord
#            Clic GAUCHE pour les QTE (Quick Time Events)

# Touches et boutons
CAST_BUTTON = 'right'  # Bouton pour lancer la ligne de pêche
REEL_BUTTON = 'right'  # Bouton pour récupérer quand le poisson mord
QTE_BUTTON = 'left'    # Bouton pour les QTE (clic gauche)

# Hotkeys
START_STOP_KEY = '-'  # Touche pour démarrer/arrêter le bot
EMERGENCY_STOP_KEY = 'esc'  # Touche d'arrêt d'urgence

# ==================== TIMINGS ====================
# Délais en secondes
CAST_DELAY = 1.0  # Délai après avoir lancé la ligne (augmenté pour stabilisation)
QTE_REACTION_TIME = 0.05  # Temps de réaction pour les QTE (50ms)
POST_QTE_DELAY = 0.5  # Délai après un QTE avant le prochain
BITE_CHECK_INTERVAL = 0.2  # Intervalle de vérification pour les morsures (200ms)
MAX_WAIT_FOR_BITE = 60  # Temps d'attente maximum pour une morsure (secondes)
BITE_DETECTION_THRESHOLD = 0.25  # Seuil de différence pour détecter une morsure (0-1) - Augmenté pour éviter faux positifs

# ==================== DÉTECTION VISUELLE ====================
# Zone de capture d'écran (None = plein écran, sinon (x, y, width, height))
SCREEN_REGION = None  # Plein écran par défaut

# Paramètres de détection des cercles QTE
QTE_DETECTION_REGION = None  # Zone spécifique pour les QTE (à calibrer)

# Couleurs des cercles (en HSV pour OpenCV)
# Cercle rouge
RED_CIRCLE_HSV_LOWER = (0, 100, 100)
RED_CIRCLE_HSV_UPPER = (10, 255, 255)

# Cercle blanc
WHITE_CIRCLE_HSV_LOWER = (0, 0, 200)
WHITE_CIRCLE_HSV_UPPER = (180, 30, 255)

# Seuils de détection
CIRCLE_DETECTION_THRESHOLD = 0.7  # Confiance minimum pour la détection (0-1)
CIRCLE_MATCH_THRESHOLD = 0.85  # Seuil pour considérer que les cercles sont alignés

# ==================== DÉTECTION AUDIO ====================
# Paramètres audio - ACTIVÉ par défaut (plus fiable que visuel!)
AUDIO_DETECTION_ENABLED = True  # Utilise la détection audio au lieu de visuelle
AUDIO_SAMPLE_RATE = 44100  # Taux d'échantillonnage (Hz)
AUDIO_CHUNK_SIZE = 1024  # Taille des blocs audio
AUDIO_THRESHOLD = 0.01  # Seuil RMS pour détecter le son de splash (à calibrer!)
# Pour calibrer: python audio/sound_detector.py calibrate

# ==================== LOGGING ====================
# Niveau de logging (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL = 'INFO'
LOG_TO_FILE = True
LOG_FILE = 'fishing_bot.log'

# Affichage visuel de debug
SHOW_DEBUG_WINDOW = False  # Afficher une fenêtre avec la détection en temps réel
DEBUG_WINDOW_SCALE = 0.5  # Échelle de la fenêtre de debug (0.5 = 50%)

# ==================== STATISTIQUES ====================
# Activer le suivi des statistiques
ENABLE_STATS = True
STATS_DISPLAY_INTERVAL = 10  # Afficher les stats tous les X poissons

# ==================== SÉCURITÉ ====================
# Arrêt automatique après X poissons (0 = désactivé)
AUTO_STOP_AFTER = 0

# Pause aléatoire entre les pêches pour simuler un comportement humain
RANDOM_DELAY_ENABLED = True
RANDOM_DELAY_MIN = 0.5
RANDOM_DELAY_MAX = 2.0

# ==================== CALIBRATION ====================
# Mode calibration pour ajuster les paramètres
CALIBRATION_MODE = False

# Dossier pour les templates d'images de référence
TEMPLATES_FOLDER = "vision/templates"

# Créer le dossier templates s'il n'existe pas
import os
if not os.path.exists(TEMPLATES_FOLDER):
    os.makedirs(TEMPLATES_FOLDER)
