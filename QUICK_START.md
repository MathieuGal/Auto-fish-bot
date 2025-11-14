# Guide de Démarrage Rapide

## ⚠️ IMPORTANT - Nouvelle Version Audio!

Le bot utilise maintenant la **détection AUDIO** par défaut (plus fiable que la détection visuelle)!

### Avant de démarrer:
1. **Activez le son de Minecraft** (Volume Master + Friendly Creatures)
2. **Calibrez le seuil audio** (une seule fois):
   ```bash
   python audio/sound_detector.py calibrate
   ```
3. Copiez le seuil recommandé dans `config.py`

Voir **AUDIO_GUIDE.md** pour plus de détails.

## Installation (Déjà fait!)

Les dépendances sont déjà installées. Vous êtes prêt à utiliser le bot!

## Utilisation Immédiate

### Méthode 1: Double-cliquer sur `start_bot.bat`

C'est la manière la plus simple! Double-cliquez simplement sur le fichier `start_bot.bat`.

### Méthode 2: Ligne de commande

```bash
python main.py
```

## Instructions Étape par Étape

1. **Lancez Minecraft** et connectez-vous à votre serveur moddé
2. **Équipez votre canne à pêche**
3. **Placez-vous devant l'eau** avec une bonne vue
4. **Lancez le bot** (double-clic sur `start_bot.bat` ou `python main.py`)
5. **Appuyez sur F6** pour démarrer
6. **Le bot fait tout automatiquement** :
   - Lance la ligne (clic droit)
   - Attend qu'un poisson morde
   - Récupère la ligne (clic droit)
   - Fait les QTE (clic gauche au bon moment)
   - Répète!

## Contrôles

- **F6** : Démarrer/Arrêter le bot
- **ESC** : Arrêt d'urgence
- **Ctrl+C** : Fermer le programme

## Configuration Actuelle

### Actions
- **Lancer ligne** : Clic DROIT
- **Quand poisson mord** : Clic DROIT
- **QTE (cercles)** : Clic GAUCHE ← IMPORTANT!

### Mode Debug (Optionnel)

Pour voir la détection en temps réel, éditez `config.py` :

```python
SHOW_DEBUG_WINDOW = True  # Changez False en True
```

Cela affichera une fenêtre montrant les cercles détectés.

## Calibration

Si les QTE ne fonctionnent pas bien :

1. Activez le mode debug (voir ci-dessus)
2. Regardez si les cercles rouge et blanc sont bien détectés
3. Si non, ajustez les seuils de couleur dans `config.py` :

```python
# Ajustez ces valeurs si la détection ne fonctionne pas
RED_CIRCLE_HSV_LOWER = (0, 100, 100)
RED_CIRCLE_HSV_UPPER = (10, 255, 255)
WHITE_CIRCLE_HSV_LOWER = (0, 0, 200)
WHITE_CIRCLE_HSV_UPPER = (180, 30, 255)
```

## Analyse de Votre Vidéo

Vous avez fourni une vidéo de pêche. Le bot a extrait 854 frames dans le dossier `frames_analysis/` pour analyser le système de QTE de votre serveur.

Vous pouvez examiner ces frames pour comprendre exactement comment fonctionnent les QTE sur votre serveur.

## Problèmes Courants

### Le bot ne clique pas
→ Assurez-vous que Minecraft a le focus (fenêtre active)

### Les cercles ne sont pas détectés
→ Activez `SHOW_DEBUG_WINDOW = True` dans config.py
→ Ajustez les seuils de couleur HSV

### Le bot clique trop tôt/tard
→ Ajustez `QTE_REACTION_TIME` dans config.py

### Minecraft ne répond pas aux clics
→ Essayez de lancer le script en tant qu'administrateur

## Statistiques

Le bot affiche en temps réel :
- Nombre de poissons attrapés
- QTE réussis/ratés
- Temps de pêche
- Taux de pêche (poissons/heure)

## Prochaines Étapes

1. Testez le bot sur votre serveur
2. Ajustez les paramètres si nécessaire
3. Activez le mode debug pour calibrer
4. Profitez de la pêche automatique!

---

**Bonne pêche! 🎣**

Pour plus d'informations, consultez le **README.md** complet.
