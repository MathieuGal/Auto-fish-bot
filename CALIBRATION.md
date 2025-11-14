# Guide de Calibration

## Problème : Faux positifs de détection de morsure

Si le bot détecte des morsures alors qu'il n'y en a pas, suivez ce guide.

## Modifications Appliquées

### ✅ Timeouts augmentés dans `config.py` :

```python
CAST_DELAY = 1.0  # Augmenté de 0.5 à 1.0 seconde
POST_QTE_DELAY = 0.5  # Augmenté de 0.3 à 0.5 seconde
BITE_CHECK_INTERVAL = 0.2  # Augmenté de 0.1 à 0.2 seconde
MAX_WAIT_FOR_BITE = 60  # Augmenté de 30 à 60 secondes
BITE_DETECTION_THRESHOLD = 0.25  # Nouveau paramètre (était 0.15 en dur)
```

### ✅ Délai de stabilisation augmenté :
- Le bot attend maintenant **2 secondes** (au lieu de 0.5s) après avoir lancé la ligne avant de commencer à détecter les morsures

## Calibration du Seuil de Détection

### Étape 1: Activer le mode DEBUG

Dans `config.py`, changez :

```python
LOG_LEVEL = 'DEBUG'  # Changez 'INFO' en 'DEBUG'
```

### Étape 2: Observer les valeurs

Lancez le bot. Vous verrez maintenant :

```
[FishDetector] Différence: 0.087 / Seuil: 0.250
[FishDetector] Différence: 0.092 / Seuil: 0.250
[FishDetector] Différence: 0.105 / Seuil: 0.250
```

### Étape 3: Analyser les résultats

**Si vous voyez des faux positifs :**
- Notez la valeur de "Différence" quand le faux positif se produit
- Exemple : `[FishDetector] Morsure détectée! Différence: 0.280 > Seuil: 0.250`

**Si vous ratez de vraies morsures :**
- Le seuil est trop élevé, il faut le diminuer

### Étape 4: Ajuster le seuil

Dans `config.py`, modifiez `BITE_DETECTION_THRESHOLD` :

```python
# Valeurs recommandées selon votre situation :

# Beaucoup de faux positifs
BITE_DETECTION_THRESHOLD = 0.30  # ou 0.35

# Quelques faux positifs
BITE_DETECTION_THRESHOLD = 0.25  # (valeur actuelle)

# Rate des vraies morsures
BITE_DETECTION_THRESHOLD = 0.20  # ou 0.18

# Très sensible (beaucoup de détection)
BITE_DETECTION_THRESHOLD = 0.15  # (valeur d'origine)
```

### Étape 5: Tester et affiner

1. Modifiez le seuil
2. Relancez le bot
3. Observez les résultats
4. Ajustez si nécessaire

## Autres Paramètres à Ajuster

### Délai de stabilisation

Si l'écran met du temps à se stabiliser après le lancement de la ligne :

Dans `vision/fish_detector.py`, ligne 103 :
```python
time.sleep(2.0)  # Augmentez à 2.5 ou 3.0 si nécessaire
```

### Intervalle de vérification

Si le CPU est surchargé :

```python
BITE_CHECK_INTERVAL = 0.3  # Augmentez de 0.2 à 0.3
```

## Diagnostic Rapide

### Symptôme : Faux positif immédiat après le lancement
→ Augmentez le délai de stabilisation (time.sleep dans fish_detector.py)

### Symptôme : Faux positifs réguliers pendant l'attente
→ Augmentez BITE_DETECTION_THRESHOLD

### Symptôme : Ne détecte jamais les vraies morsures
→ Diminuez BITE_DETECTION_THRESHOLD
→ Vérifiez que Minecraft est en plein écran

### Symptôme : Détection très lente
→ Diminuez BITE_CHECK_INTERVAL (mais augmente l'usage CPU)

## Valeurs Recommandées par Situation

### Serveur avec animations fluides
```python
BITE_DETECTION_THRESHOLD = 0.20
BITE_CHECK_INTERVAL = 0.15
```

### Serveur avec beaucoup d'effets visuels
```python
BITE_DETECTION_THRESHOLD = 0.30
BITE_CHECK_INTERVAL = 0.2
```

### PC lent / Lag réseau
```python
BITE_DETECTION_THRESHOLD = 0.35
BITE_CHECK_INTERVAL = 0.3
CAST_DELAY = 1.5
```

### Performance maximale (PC puissant)
```python
BITE_DETECTION_THRESHOLD = 0.25
BITE_CHECK_INTERVAL = 0.1
```

## Test Manuel

Pour tester uniquement la détection de morsure :

```bash
python -c "from vision.fish_detector import get_fish_detector; detector = get_fish_detector(); detector.wait_for_bite()"
```

Cela vous permet de tester sans lancer le bot complet.

---

**Note :** Les valeurs actuelles ont déjà été optimisées pour réduire les faux positifs. Commencez par tester avec ces valeurs avant de faire d'autres ajustements.
