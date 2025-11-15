# Bot de Pêche Automatique Minecraft

Bot automatique pour la pêche sur serveurs Minecraft moddés avec système de QTE (Quick Time Events).

## Fonctionnalités

- **🔊 Détection audio WASAPI loopback** : capture directe de l'audio système (plus besoin de micro!)
- **Détection automatique** des morsures de poisson par son OU vision
- **Gestion intelligente des QTE** : détecte les cercles rouge et blanc et clique au moment parfait
- **Support de 1 à 6 QTE consécutifs** par poisson
- **Détection visuelle ultra-rapide** avec OpenCV et MSS
- **Simulation de comportement humain** avec délais aléatoires
- **Statistiques en temps réel** : poissons attrapés, QTE réussis/ratés, taux horaire
- **Mode debug** pour calibrer et visualiser la détection

## Configuration système

- **OS** : Windows (testé sur Windows 10/11)
- **Python** : 3.8 ou supérieur
- **Minecraft** : Serveur moddé avec système de pêche customisé

## Installation

### 1. Cloner ou télécharger le projet

```bash
cd "C:\Users\mathi\Auto fish bot"
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

Les bibliothèques nécessaires :
- `opencv-python` : Vision par ordinateur pour la détection des cercles
- `numpy` : Calculs matriciels
- `pillow` : Manipulation d'images
- `mss` : Capture d'écran ultra-rapide
- `pyautogui` : Automation souris/clavier
- `pydirectinput` : Automation compatible avec les jeux
- `keyboard` : Gestion des hotkeys
- `soundcard` : Capture audio système via WASAPI loopback
- `scipy` : Traitement du signal audio
- `colorama` : Couleurs dans le terminal

## Configuration

### Fichier `config.py`

Le fichier `config.py` contient toutes les configurations du bot :

#### Contrôles (IMPORTANT!)

```python
CAST_BUTTON = 'right'  # Clic DROIT pour lancer la ligne
REEL_BUTTON = 'right'  # Clic DROIT quand le poisson mord
QTE_BUTTON = 'left'    # Clic GAUCHE pour les QTE
```

#### Hotkeys

```python
START_STOP_KEY = 'f6'  # Démarrer/arrêter le bot
EMERGENCY_STOP_KEY = 'esc'  # Arrêt d'urgence
```

#### Timings

```python
CAST_DELAY = 0.5  # Délai après avoir lancé la ligne
QTE_REACTION_TIME = 0.05  # Temps de réaction QTE (50ms)
MAX_WAIT_FOR_BITE = 30  # Temps d'attente max pour une morsure
```

#### Détection visuelle

```python
# Activer le mode debug pour voir la détection en temps réel
SHOW_DEBUG_WINDOW = True
DEBUG_WINDOW_SCALE = 0.5
```

#### Comportement humain

```python
RANDOM_DELAY_ENABLED = True
RANDOM_DELAY_MIN = 0.5
RANDOM_DELAY_MAX = 2.0
```

## Utilisation

### Démarrage rapide

1. Lancez Minecraft et connectez-vous à votre serveur
2. Équipez votre canne à pêche
3. Placez-vous devant l'eau
4. Exécutez le bot :

```bash
python main.py
```

5. Appuyez sur **F6** pour démarrer
6. Le bot va automatiquement :
   - Lancer la ligne (clic droit)
   - Attendre qu'un poisson morde
   - Récupérer la ligne (clic droit)
   - Exécuter les QTE (clic gauche au bon moment)
   - Recommencer

### Arrêt

- **F6** : Arrêt normal avec affichage des statistiques
- **ESC** : Arrêt d'urgence immédiat
- **Ctrl+C** : Interruption du programme

## Structure du projet

```
Auto fish bot/
├── main.py                          # Point d'entrée principal
├── config.py                        # Configuration globale
├── fishing_bot.py                   # Logique principale du bot
├── requirements.txt                 # Dépendances Python
├── vision/
│   ├── screen_capture.py           # Capture d'écran ultra-rapide
│   ├── qte_detector.py             # Détection des cercles QTE
│   ├── fish_detector.py            # Détection des morsures
│   └── templates/                  # Images de référence (templates)
├── automation/
│   └── controller.py               # Contrôle souris/clavier
├── frames_analysis/                # Frames extraites de la vidéo
└── README.md                       # Cette documentation
```

## Calibration

### Mode debug

Pour calibrer la détection des QTE, activez le mode debug dans `config.py` :

```python
SHOW_DEBUG_WINDOW = True
LOG_LEVEL = 'DEBUG'
```

Cela affichera une fenêtre montrant :
- Les cercles rouge (cible) et blanc (curseur) détectés
- L'indication "CLICK NOW!" quand c'est le moment parfait

### Ajuster les seuils de couleur

Si la détection ne fonctionne pas bien, ajustez les valeurs HSV dans `config.py` :

```python
# Cercle rouge
RED_CIRCLE_HSV_LOWER = (0, 100, 100)
RED_CIRCLE_HSV_UPPER = (10, 255, 255)

# Cercle blanc
WHITE_CIRCLE_HSV_LOWER = (0, 0, 200)
WHITE_CIRCLE_HSV_UPPER = (180, 30, 255)
```

## Dépannage

### Le bot ne détecte pas les QTE

1. Activez le mode debug : `SHOW_DEBUG_WINDOW = True`
2. Vérifiez que les cercles sont bien détectés dans la fenêtre de debug
3. Ajustez les seuils de couleur HSV si nécessaire
4. Assurez-vous que Minecraft est en plein écran ou en mode fenêtré sans bordure

### Les clics ne fonctionnent pas dans Minecraft

1. Assurez-vous que Minecraft a le focus
2. Vérifiez que `pydirectinput` est bien installé
3. Essayez de lancer le script en tant qu'administrateur

### Le bot clique trop tôt ou trop tard

Ajustez le timing dans `config.py` :

```python
QTE_REACTION_TIME = 0.05  # Augmentez pour cliquer plus tard
```

### Erreur "No module named 'cv2'"

Réinstallez OpenCV :

```bash
pip uninstall opencv-python
pip install opencv-python
```

## Statistiques

Le bot affiche des statistiques en temps réel :

- **Poissons attrapés** : Nombre total de poissons pêchés
- **QTE réussis/ratés** : Performance sur les QTE
- **Temps écoulé** : Durée totale d'exécution
- **Poissons/heure** : Taux de pêche moyen

## Sécurité et éthique

**Attention** : L'utilisation de bots peut être contraire aux règles de certains serveurs Minecraft. Utilisez ce bot de manière responsable et respectez les règles du serveur sur lequel vous jouez.

Ce bot est fourni à des fins éducatives et de démonstration des capacités de vision par ordinateur et d'automation Python.

## Détection Audio 🔊

Le bot utilise maintenant la **capture audio système directe** via WASAPI loopback!

### Avantages
- ✅ Plus fiable que la détection visuelle
- ✅ Aucun faux positif
- ✅ Plus besoin de microphone ou câble loopback
- ✅ Capture directe de l'audio de sortie Windows
- ✅ Fonctionne même si Minecraft est en arrière-plan

### Test rapide

Pour tester que le loopback fonctionne :

```bash
python test_loopback.py
```

Ce script affichera en temps réel l'audio capturé depuis votre système.

### Configuration

La détection audio est **activée par défaut** dans `config.py` :

```python
AUDIO_DETECTION_ENABLED = True
AUDIO_THRESHOLD = 0.01  # À ajuster selon votre environnement
```

**📖 Pour plus de détails, consultez [AUDIO_GUIDE.md](AUDIO_GUIDE.md)**

## Améliorations futures possibles

- [ ] Machine Learning pour améliorer la précision des QTE
- [ ] Support multi-écran
- [ ] Interface graphique (GUI)
- [ ] Système de profils pour différents serveurs
- [ ] Détection automatique de la zone de pêche
- [ ] Isolation audio par processus (capturer uniquement Minecraft)

## Contribution

Les contributions sont les bienvenues! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Partager vos configurations optimisées

## Licence

Ce projet est fourni "tel quel" sans garantie. Utilisez-le à vos propres risques.

## Support

Pour toute question ou problème, consultez :
1. Ce README
2. Les commentaires dans le code source
3. Le fichier `config.py` pour les options disponibles

---

**Bonne pêche! 🎣**
