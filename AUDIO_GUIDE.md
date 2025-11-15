# 🔊 Guide de Détection Audio

La détection audio est maintenant **activée par défaut** car elle est **beaucoup plus fiable** que la détection visuelle!

## 🎉 NOUVEAU : Capture Audio Directe (WASAPI Loopback)

Le bot capture maintenant **directement l'audio de sortie de votre PC** via WASAPI loopback !

✅ **Plus besoin de microphone !**
✅ **Plus besoin de câble loopback !**
✅ **Plus besoin de Stereo Mix !**
✅ **Capture directe de l'audio système de Windows**

## Pourquoi l'Audio?

✅ **Aucun faux positif** - Le son de splash est unique et reconnaissable
✅ **Plus rapide** - Pas besoin d'analyser des images
✅ **Fonctionne en arrière-plan** - Même si Minecraft n'est pas au premier plan
✅ **Pas de calibration complexe** - Juste ajuster un seuil simple
✅ **Capture directe** - Écoute directement la sortie audio du système (WASAPI)

## Configuration Requise

### 1. Son de Minecraft Activé

**IMPORTANT:** Assurez-vous que le son de Minecraft est activé!

Dans Minecraft:
- **Menu** → **Options** → **Music & Sounds**
- Vérifiez que **"Master Volume"** n'est pas à 0%
- Vérifiez que **"Friendly Creatures"** n'est pas à 0% (c'est la catégorie des sons de pêche)

### 2. Audio Système (WASAPI Loopback)

Le bot utilise maintenant **WASAPI loopback** pour capturer directement l'audio de sortie de Windows.

**Aucune configuration nécessaire !** Le bot détecte automatiquement votre sortie audio par défaut.

⚠️ **Important:**
- Le bot capte **TOUT l'audio système** (pas seulement Minecraft)
- Pour de meilleurs résultats, évitez d'avoir d'autres applications qui font du bruit pendant que vous pêchez
- Le volume de Minecraft doit être suffisamment élevé pour être détecté

## Première Utilisation

### Étape 1: Calibration

Avant la première utilisation, calibrez le seuil de détection :

```bash
python audio/sound_detector.py calibrate
```

Cela va :
1. Mesurer le bruit ambiant pendant 10 secondes
2. Vous donner un seuil recommandé
3. Exemple de résultat :
   ```
   Bruit moyen: 0.002341
   Bruit maximum: 0.005123
   Seuil recommandé: 0.025615

   💡 Ajoutez cette ligne dans config.py:
      AUDIO_THRESHOLD = 0.025615
   ```

### Étape 2: Appliquer le Seuil

Copiez la valeur recommandée dans `config.py` :

```python
AUDIO_THRESHOLD = 0.025615  # Remplacez par votre valeur
```

### Étape 3: Tester

Testez la détection avant de lancer le bot complet :

```bash
python audio/sound_detector.py test
```

Pendant le test :
- Lancez une ligne dans Minecraft
- Attendez qu'un poisson morde
- Vérifiez que le bot détecte le splash

Si ça fonctionne → Vous êtes prêt!

## Utilisation Normale

Une fois calibré, lancez simplement le bot :

```bash
python main.py
```

Le bot affichera :
```
Mode: 🔊 Détection AUDIO (plus fiable!)
Assurez-vous que le son de Minecraft est activé!
```

## Réglage Fin

### Le bot ne détecte RIEN

**Seuil trop élevé** - Diminuez `AUDIO_THRESHOLD` :

```python
AUDIO_THRESHOLD = 0.01  # Essayez plus bas
```

Activez le mode DEBUG pour voir les valeurs :

```python
LOG_LEVEL = 'DEBUG'
```

Vous verrez :
```
[SoundDetector] RMS: 0.008234, dB: -41.69, Seuil: 0.025615
```

Si le RMS est **toujours en dessous** du seuil → Diminuez le seuil

### Le bot détecte TOUT

**Seuil trop bas** - Augmentez `AUDIO_THRESHOLD` :

```python
AUDIO_THRESHOLD = 0.05  # Essayez plus haut
```

### Ajustement du Ratio de Pic

Le bot détecte les "pics" sonores (son soudain 3x plus fort que la moyenne).

Si vous avez des problèmes, modifiez dans `audio/sound_detector.py` ligne ~100 :

```python
amplitude_ratio > 3.0  # Changez 3.0 en 2.5 (plus sensible) ou 4.0 (moins sensible)
```

## Dépannage

### Erreur: "No module named 'soundcard'"

Installez les dépendances :

```bash
pip install soundcard scipy
```

Ou utilisez le fichier requirements.txt :

```bash
pip install -r requirements.txt
```

### Erreur: "Aucun haut-parleur par défaut trouvé"

Vérifiez que vous avez une sortie audio configurée dans Windows :

1. **Paramètres Windows** → **Son**
2. Assurez-vous qu'un périphérique de sortie est défini par défaut
3. Vérifiez que le périphérique n'est pas désactivé

### Le bot n'entend rien

1. Vérifiez que le son de Minecraft est activé et **assez fort**
2. Augmentez le volume des "Friendly Creatures" dans Minecraft
3. **NOUVEAU:** Vérifiez que le volume système de Windows n'est pas coupé
4. Testez en jouant de la musique - si vous l'entendez, le bot devrait aussi la capter

### Sons parasites détectés

Si d'autres sons déclenchent le bot :
1. Augmentez `AUDIO_THRESHOLD`
2. Augmentez le ratio de pic dans le code
3. Fermez les autres applications qui font du bruit

## Mode Debug

Pour voir en temps réel ce que détecte le bot :

```python
# Dans config.py
LOG_LEVEL = 'DEBUG'
```

Vous verrez :
```
[SoundDetector] RMS: 0.003421, dB: -49.32, Seuil: 0.025615
[SoundDetector] RMS: 0.003890, dB: -48.20, Seuil: 0.025615
[SoundDetector] 🎣 SPLASH DÉTECTÉ! RMS: 0.034567, Ratio: 8.51x
```

## Comparaison Audio vs Visuel

| Critère | Audio 🔊 | Visuel 👁️ |
|---------|----------|-----------|
| Fiabilité | ⭐⭐⭐⭐⭐ Excellente | ⭐⭐⭐ Bonne |
| Faux positifs | ❌ Presque aucun | ⚠️ Possibles |
| Performance CPU | ✅ Légère | 🔥 Moyenne |
| Calibration | 🔧 Simple (1 seuil) | 🔧🔧 Complexe (couleurs) |
| Arrière-plan | ✅ Fonctionne | ❌ Nécessite focus |

## Basculer entre Audio et Visuel

Dans `config.py` :

```python
# Détection AUDIO (recommandé)
AUDIO_DETECTION_ENABLED = True

# Détection VISUELLE (ancien mode)
AUDIO_DETECTION_ENABLED = False
```

## Sons de Minecraft

Le son de morsure s'appelle **`entity.bobber.splash`** dans Minecraft.

C'est un son court, fort, caractéristique d'un splash d'eau.

---

**Astuce:** Une fois calibré correctement, la détection audio est ultra-fiable et ne nécessite plus d'ajustements!

Pour plus d'aide, consultez le **README.md** principal.
