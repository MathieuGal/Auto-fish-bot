"""
Script de test rapide pour vérifier que la détection audio fonctionne
"""

import sys

print("Test de la Detection Audio")
print("="*60)
print()

# Test 1: Imports
print("[1/3] Test des imports...")
try:
    import sounddevice as sd
    import scipy
    from audio.sound_detector import get_sound_detector
    print("OK - Tous les modules sont importes correctement")
except ImportError as e:
    print(f"ERREUR - Import: {e}")
    print("Installez les dependances: pip install sounddevice scipy")
    sys.exit(1)

print()

# Test 2: Périphériques audio
print("[2/3] Verification des peripheriques audio...")
try:
    devices = sd.query_devices()
    print(f"OK - {len(devices)} peripheriques audio detectes")

    # Afficher le périphérique par défaut
    default_input = sd.query_devices(kind='input')
    print(f"Peripherique d'entree par defaut: {default_input['name']}")
except Exception as e:
    print(f"ERREUR: {e}")
    sys.exit(1)

print()

# Test 3: Créer le détecteur
print("[3/3] Test du detecteur audio...")
try:
    detector = get_sound_detector()
    print("OK - Detecteur audio cree avec succes")

    print()
    print("="*60)
    print("TOUS LES TESTS REUSSIS!")
    print()
    print("Prochaines étapes:")
    print("1. Calibrez le seuil:")
    print("   python audio/sound_detector.py calibrate")
    print()
    print("2. Testez la détection:")
    print("   python audio/sound_detector.py test")
    print()
    print("3. Lancez le bot:")
    print("   python main.py")

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
