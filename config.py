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
START_STOP_KEY = '-'  # Touche pour démarrer/arrêter le bot (même touche pour les deux!)

# ==================== TIMINGS ====================
# Délais en secondes
CAST_DELAY = 1.0  # Délai après avoir lancé la ligne (augmenté pour stabilisation)
QTE_REACTION_TIME = 0.03  # Temps de réaction pour les QTE (30ms - optimisé)
QTE_SAFETY_DELAY = 0.05  # Délai de sécurité avant de cliquer sur un QTE (50ms pour être sûr de l'alignement)
POST_QTE_DELAY = 0.3  # Délai après un QTE avant le prochain (réduit pour réactivité)
BITE_CHECK_INTERVAL = 0.2  # Intervalle de vérification pour les morsures (200ms)
MAX_WAIT_FOR_BITE = 240  # Temps d'attente maximum pour une morsure (secondes)
BITE_DETECTION_THRESHOLD = 0.25  # Seuil de différence pour détecter une morsure (0-1) - Augmenté pour éviter faux positifs

# ==================== DÉTECTION VISUELLE ====================
# Zone de capture d'écran (None = plein écran, sinon (x, y, width, height))
SCREEN_REGION = None  # Plein écran par défaut

# ========== Paramètres de détection des cercles QTE ==========
# NOUVEAU : AUTO-DÉTECTION DE LA RÉSOLUTION D'ÉCRAN
# Le bot détecte automatiquement votre résolution (1080p, 1440p, 4K, etc.)
# et calcule la région de détection optimale au centre de l'écran
QTE_DETECTION_REGION = None  # Laissez None pour auto-détection (recommandé)

# Taille de la région QTE en pourcentage de l'écran (0.4 = 40% de largeur)
# Ajustez si la détection ne fonctionne pas (valeur entre 0.3 et 0.6)
QTE_REGION_SCALE = 0.4

# Couleurs des cercles (en HSV pour OpenCV)
# NOTE: Les paramètres de détection (circularity, Hough) sont maintenant
# automatiquement ajustés pour être plus permissifs avec le rendu pixelisé de Minecraft

# Cercle rouge (cible)
RED_CIRCLE_HSV_LOWER = (0, 100, 100)
RED_CIRCLE_HSV_UPPER = (10, 255, 255)

# Cercle blanc (curseur)
WHITE_CIRCLE_HSV_LOWER = (0, 0, 200)
WHITE_CIRCLE_HSV_UPPER = (180, 30, 255)

# Seuils de détection (ces paramètres sont maintenant moins critiques)
CIRCLE_DETECTION_THRESHOLD = 0.7  # Confiance minimum pour la détection (0-1)
CIRCLE_MATCH_THRESHOLD = 0.85  # Seuil pour considérer que les cercles sont alignés
QTE_END_DETECTION_DELAY = 2.5  # Temps d'attente sans cercle pour déclarer la fin des QTE (secondes)

# Détection du message de succès (DÉSACTIVÉ - cause des faux positifs)
SUCCESS_DETECTION_ENABLED = False  # Détecter le message "PÊCHE Vous avez pêché..." pour terminer les QTE
SUCCESS_CHECK_INTERVAL = 0.1  # Vérifier le message de succès toutes les X secondes

# ==================== DÉTECTION AUDIO ====================
# Paramètres audio - ACTIVÉ par défaut (plus fiable que visuel!)
AUDIO_DETECTION_ENABLED = True  # Utilise la détection audio au lieu de visuelle
AUDIO_SAMPLE_RATE = 44100  # Taux d'échantillonnage (Hz)
AUDIO_CHUNK_SIZE = 1024  # Taille des blocs audio
AUDIO_THRESHOLD = 0.001  # Seuil RMS pour détecter le son de splash (à calibrer!)
AUDIO_IGNORE_AFTER_CAST = 1.5  # Ignorer le son pendant X secondes après le lancer (évite de détecter le bruit de la canne)
# Pour calibrer: python audio/sound_detector.py calibrate

# ==================== LOGGING ====================
# Niveau de logging (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL = 'DEBUG'
LOG_TO_FILE = True
LOG_FILE = 'fishing_bot.log'

# Affichage visuel de debug
SHOW_DEBUG_WINDOW = True  # Afficher une fenêtre avec la détection en temps réel
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
