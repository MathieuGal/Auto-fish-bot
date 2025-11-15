# 🎣 Guide d'Installation - Bot de Pêche Automatique Minecraft

Guide complet pour installer et utiliser le bot de pêche, **même si vous n'y connaissez rien en programmation** !

---

## 📋 Table des Matières

1. [Prérequis](#prérequis)
2. [Installation de Python](#installation-de-python)
3. [Téléchargement du Bot](#téléchargement-du-bot)
4. [Installation des Dépendances](#installation-des-dépendances)
5. [Configuration](#configuration)
6. [Utilisation](#utilisation)
7. [Problèmes Courants](#problèmes-courants)

---

## 🔧 Prérequis

Avant de commencer, vous avez besoin de :

- ✅ **Windows 10/11** (le bot est conçu pour Windows)
- ✅ **Minecraft Java Edition** avec un serveur qui a la pêche
- ✅ **15 minutes** pour tout installer
- ✅ **Une connexion Internet**

---

## 🐍 Installation de Python

### Étape 1 : Télécharger Python

1. Allez sur : https://www.python.org/downloads/
2. Cliquez sur le gros bouton jaune **"Download Python 3.x.x"**
3. Attendez que le fichier se télécharge (environ 25 MB)

### Étape 2 : Installer Python

1. **Double-cliquez** sur le fichier téléchargé (par exemple `python-3.12.0-amd64.exe`)
2. ⚠️ **TRÈS IMPORTANT** : Cochez la case **"Add Python to PATH"** en bas de la fenêtre !
3. Cliquez sur **"Install Now"**
4. Attendez que l'installation se termine (2-3 minutes)
5. Cliquez sur **"Close"**

### Étape 3 : Vérifier l'installation

1. Appuyez sur **Windows + R** sur votre clavier
2. Tapez `cmd` et appuyez sur **Entrée**
3. Dans la fenêtre noire qui s'ouvre, tapez :
   ```
   python --version
   ```
4. Vous devriez voir quelque chose comme `Python 3.12.0`
5. ✅ Si vous voyez ça, Python est bien installé !
6. ❌ Si vous voyez une erreur, recommencez l'installation et **cochez bien "Add Python to PATH"**

---

## 📥 Téléchargement du Bot

### Option 1 : Télécharger le ZIP (plus simple)

1. Allez sur : https://github.com/MathieuGal/Auto-fish-bot
2. Cliquez sur le bouton vert **"Code"**
3. Cliquez sur **"Download ZIP"**
4. Une fois téléchargé, **faites un clic droit** sur le fichier ZIP
5. Cliquez sur **"Extraire tout..."**
6. Choisissez un dossier (par exemple `C:\Users\VotreNom\Documents\`)
7. Cliquez sur **"Extraire"**

### Option 2 : Cloner avec Git (si vous connaissez)

```bash
git clone https://github.com/MathieuGal/Auto-fish-bot.git
cd Auto-fish-bot
```

---

## 📦 Installation des Dépendances

### Étape 1 : Ouvrir le dossier dans le terminal

1. Ouvrez le dossier où vous avez extrait le bot
2. Dans la barre d'adresse en haut, **cliquez** et tapez `cmd` puis **Entrée**
3. Une fenêtre noire (terminal) s'ouvre dans le bon dossier

### Étape 2 : Installer les bibliothèques nécessaires

Dans la fenêtre noire (terminal), tapez cette commande et appuyez sur **Entrée** :

```bash
pip install -r requirements.txt
```

⏳ **Attendez 1-2 minutes** que tout s'installe. Vous allez voir plein de texte défiler, c'est normal !

✅ Quand c'est fini, vous voyez le curseur clignoter à nouveau.

---

## ⚙️ Configuration

### 1. Configuration du Son (TRÈS IMPORTANT)

Le bot **écoute le son de Minecraft** pour détecter les poissons. Il faut activer cette fonctionnalité :

#### Sur Windows 10/11 :

1. **Clic droit** sur l'icône de son 🔊 en bas à droite de Windows
2. Cliquez sur **"Paramètres de son"**
3. Descendez et cliquez sur **"Paramètres de son avancés"** ou **"Panneau de configuration Son"**
4. Dans l'onglet **"Lecture"**, trouvez votre haut-parleur/casque actuel
5. ✅ Assurez-vous qu'il est activé et défini par défaut
6. Le bot va **capturer automatiquement l'audio système** de votre PC

**Note :** Le son de Minecraft doit être **activé et audible** ! Le bot écoute TOUS les sons de votre PC.

### 2. Réglages dans Minecraft

1. **Lancez Minecraft** et connectez-vous au serveur
2. Mettez-vous **devant l'eau** avec une canne à pêche équipée
3. **Volume du jeu** : Assurez-vous que le son n'est pas coupé (au moins 50%)
4. **Position de la souris** : Pointez vers l'eau (le bot ne bouge PAS la souris)

### 3. Ajuster la sensibilité (optionnel)

Si le bot détecte trop de faux sons ou pas assez :

1. Ouvrez le fichier `config.py` avec le Bloc-notes
2. Cherchez la ligne `AUDIO_THRESHOLD = 0.001`
3. Modifiez la valeur :
   - **Trop de fausses détections ?** → Augmentez (essayez `0.002` ou `0.003`)
   - **Le bot ne détecte rien ?** → Diminuez (essayez `0.0005`)
4. Sauvegardez le fichier

---

## 🚀 Utilisation

### Démarrer le Bot

1. **Ouvrez Minecraft** et connectez-vous au serveur de pêche
2. **Équipez votre canne à pêche**
3. **Placez-vous devant l'eau** et pointez votre souris vers l'eau
4. Ouvrez le dossier du bot dans l'explorateur
5. Dans la barre d'adresse, tapez `cmd` et appuyez sur **Entrée**
6. Dans le terminal, tapez :
   ```bash
   python main.py
   ```
7. Appuyez sur la touche **`-`** (tiret du 6) pour **démarrer le bot**

### Pendant que le Bot Tourne

- ✅ **Le bot va automatiquement :**
  - Lancer la ligne
  - Détecter la morsure (par le son)
  - Récupérer le poisson
  - Faire les QTE (Quick Time Events) - jusqu'à 6 QTE
  - Recommencer automatiquement

- 🎮 **Vous pouvez :**
  - Regarder le bot travailler
  - Faire autre chose sur votre PC (mais ne minimisez pas Minecraft)

- ⛔ **NE PAS :**
  - Bouger la souris pendant que le bot clique
  - Minimiser Minecraft
  - Couper le son

### Arrêter le Bot

Appuyez sur la touche **`-`** (tiret du 6) à nouveau, ou appuyez sur **Ctrl + C** dans le terminal.

---

## 🎯 Fonctionnalités du Bot

### Détection Audio Intelligente
- ✅ Détecte le son "splash" du poisson qui mord
- ✅ Ignore le bruit du lancer de la canne (1.5 secondes)
- ✅ Ne réagit PAS aux bruits de votre micro (capture l'audio système uniquement)

### Système de QTE Robuste
- ✅ Détecte les cercles rouge et blanc
- ✅ Clique au moment parfait (alignement des cercles)
- ✅ Fait jusqu'à 6 QTE automatiquement
- ✅ Timeout de 15 secondes si aucun cercle n'apparaît

### Statistiques
- 📊 Nombre de poissons attrapés
- 📊 QTE réussis/ratés
- 📊 Temps moyen par poisson
- 📊 Poissons par heure

---

## ❌ Problèmes Courants

### Le bot ne démarre pas

**Erreur : "python n'est pas reconnu..."**
- ➡️ Python n'est pas installé ou pas dans le PATH
- ✅ Solution : Réinstallez Python et **cochez "Add Python to PATH"**

**Erreur : "No module named 'cv2'" ou similaire**
- ➡️ Les dépendances ne sont pas installées
- ✅ Solution : Tapez `pip install -r requirements.txt`

### Le bot ne détecte pas les morsures

**Le bot dit "Timeout: aucune morsure detectee"**
- ➡️ Le son de Minecraft n'est pas capturé
- ✅ Solutions :
  1. Vérifiez que le **son de Minecraft est activé** (au moins 50%)
  2. Vérifiez que votre **haut-parleur/casque est actif** dans Windows
  3. Essayez de baisser `AUDIO_THRESHOLD` dans `config.py` (par exemple `0.0005`)
  4. Lancez `python audio/sound_detector.py test` pour tester la détection

**Pour calibrer le seuil audio :**
```bash
python audio/sound_detector.py calibrate
```
Cette commande va mesurer le bruit ambiant et vous donner un seuil recommandé.

### Le bot clique à côté des QTE

- ➡️ Problème de timing ou de détection des cercles
- ✅ Solutions :
  1. Ouvrez `config.py`
  2. Augmentez `QTE_SAFETY_DELAY` (essayez `0.08` ou `0.1`)
  3. Vérifiez que Minecraft est en **plein écran** ou **fenêtré sans bordure**

### Le bot détecte des sons fantômes

**Le bot détecte une morsure alors qu'il n'y en a pas**
- ➡️ Trop de bruit ambiant ou seuil trop bas
- ✅ Solutions :
  1. Augmentez `AUDIO_THRESHOLD` dans `config.py` (essayez `0.002` ou `0.003`)
  2. Coupez la musique/vidéos sur votre PC pendant que le bot tourne
  3. Utilisez la commande `calibrate` pour trouver le bon seuil

### Le bot fait seulement 1 QTE au lieu de plusieurs

- ➡️ Ce problème devrait être résolu dans la dernière version
- ✅ Solution : Assurez-vous d'avoir la dernière version du bot (re-téléchargez)

### Minecraft freeze ou lag quand le bot tourne

- ➡️ Le bot vérifie trop rapidement (normal sur PC peu puissants)
- ✅ Solutions :
  1. Fermez les autres applications
  2. Baissez les graphismes de Minecraft
  3. Le bot est optimisé, mais demande un minimum de ressources

---

## 🔧 Configuration Avancée (Optionnel)

### Fichier `config.py`

Vous pouvez modifier ces paramètres dans `config.py` :

```python
# Arrêt automatique après X poissons (0 = infini)
AUTO_STOP_AFTER = 0  # Changez en 100 pour arrêter après 100 poissons

# Pause aléatoire entre les pêches (anti-détection)
RANDOM_DELAY_MIN = 0.5  # Minimum 0.5 secondes
RANDOM_DELAY_MAX = 2.0  # Maximum 2 secondes

# Timeout pour attendre une morsure
MAX_WAIT_FOR_BITE = 90  # 90 secondes max

# Seuil de détection audio
AUDIO_THRESHOLD = 0.001  # Plus haut = moins sensible

# Afficher les stats tous les X poissons
STATS_DISPLAY_INTERVAL = 10  # Affiche stats tous les 10 poissons
```

### Mode Debug

Pour voir plus d'informations pendant que le bot tourne :

1. Ouvrez `config.py`
2. Changez `LOG_LEVEL = 'INFO'` en `LOG_LEVEL = 'DEBUG'`
3. Vous verrez tous les détails de détection

---

## 📊 Performances Attendues

Avec un bon setup, le bot peut attraper :
- **30-60 poissons par heure** (dépend du serveur et des QTE)
- **Taux de réussite QTE : 95-100%**
- **Taux de détection morsure : 98-100%**

---

## ⚠️ Avertissements

1. **Utilisation sur serveurs** : Vérifiez que les bots sont autorisés sur votre serveur Minecraft. Certains serveurs interdisent l'utilisation de bots.

2. **Détection anti-cheat** : Ce bot simule des clics de souris. Certains anti-cheats peuvent le détecter.

3. **Utilisation responsable** : Ne laissez pas le bot tourner 24/7, cela peut être considéré comme de l'AFK farming.

---

## 🆘 Besoin d'Aide ?

Si vous avez encore des problèmes :

1. **Vérifiez la section [Problèmes Courants](#problèmes-courants)**
2. **Relisez le guide étape par étape**
3. **Consultez le fichier `AUDIO_GUIDE.md`** pour les problèmes audio spécifiques
4. **Ouvrez une issue** sur GitHub : https://github.com/MathieuGal/Auto-fish-bot/issues

---

## 📝 Récapitulatif Rapide

**Pour les pressés, voici les étapes minimales :**

```bash
# 1. Installer Python (avec "Add to PATH" !)
# 2. Télécharger le bot et extraire le ZIP
# 3. Ouvrir un terminal dans le dossier du bot
# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Lancer Minecraft, équiper la canne, pointer vers l'eau
# 6. Lancer le bot
python main.py

# 7. Appuyer sur '-' pour démarrer/arrêter
```

---

**Bon fishing ! 🎣**
