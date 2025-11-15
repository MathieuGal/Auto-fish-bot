"""
Script de test pour vérifier que le loopback audio fonctionne
Ce script affiche en temps réel le niveau audio capturé depuis la sortie système
"""

import soundcard as sc
import numpy as np
import time

def test_loopback():
    """Test le loopback audio et affiche les niveaux en temps réel"""

    print("=" * 70)
    print("🔊 TEST DE CAPTURE AUDIO SYSTÈME (WASAPI Loopback)")
    print("=" * 70)
    print()

    # Obtenir le haut-parleur par défaut
    try:
        default_speaker = sc.default_speaker()
        if default_speaker is None:
            print("❌ ERREUR: Aucun haut-parleur par défaut trouvé!")
            print()
            print("Solutions:")
            print("  1. Ouvrez Paramètres Windows → Son")
            print("  2. Configurez un périphérique de sortie par défaut")
            print("  3. Assurez-vous que le périphérique est activé")
            return False

        print(f"✅ Haut-parleur détecté: {default_speaker.name}")
        print()

    except Exception as e:
        print(f"❌ ERREUR lors de la détection du haut-parleur: {e}")
        return False

    # Créer le microphone loopback
    try:
        loopback = sc.get_microphone(
            id=str(default_speaker.name),
            include_loopback=True
        )
        print(f"✅ Loopback initialisé avec succès!")
        print()

    except Exception as e:
        print(f"❌ ERREUR lors de l'initialisation du loopback: {e}")
        print()
        print("Solutions:")
        print("  1. Installez soundcard: pip install soundcard")
        print("  2. Redémarrez votre terminal/IDE")
        print("  3. Vérifiez que Windows Audio est démarré")
        return False

    # Lancer le test
    print("📊 TEST EN COURS - Faites du bruit avec Minecraft ou jouez de la musique!")
    print("   (Le script s'arrêtera automatiquement après 30 secondes)")
    print()
    print("Niveau audio capturé:")
    print("-" * 70)

    try:
        with loopback.recorder(samplerate=44100) as recorder:
            start_time = time.time()
            max_level = 0

            while (time.time() - start_time) < 30:
                # Enregistrer un petit bloc
                data = recorder.record(numframes=1024)

                # Convertir en mono si nécessaire
                if len(data.shape) > 1 and data.shape[1] > 1:
                    data = np.mean(data, axis=1)

                # Calculer le niveau RMS
                rms = np.sqrt(np.mean(data**2))

                # Calculer dB
                if rms > 0:
                    db = 20 * np.log10(rms)
                else:
                    db = -100

                # Tracker le max
                if rms > max_level:
                    max_level = rms

                # Créer une barre visuelle
                bar_length = int(min(rms * 1000, 50))
                bar = "█" * bar_length

                # Afficher avec code couleur
                if rms > 0.05:
                    status = "🔴 FORT"
                elif rms > 0.01:
                    status = "🟡 MOYEN"
                elif rms > 0.001:
                    status = "🟢 FAIBLE"
                else:
                    status = "⚪ SILENCE"

                # Afficher (écrase la ligne précédente)
                print(f"\r{status} | RMS: {rms:.6f} | dB: {db:6.2f} | {bar:<50}", end="", flush=True)

                time.sleep(0.05)

        print()
        print()
        print("-" * 70)
        print(f"✅ Test terminé!")
        print(f"   Niveau maximum capturé: {max_level:.6f}")
        print()

        if max_level > 0.001:
            print("✅ Le loopback fonctionne correctement!")
            print(f"   Seuil recommandé pour config.py: AUDIO_THRESHOLD = {max_level * 0.5:.6f}")
        else:
            print("⚠️  Aucun son détecté!")
            print()
            print("Solutions possibles:")
            print("  1. Augmentez le volume système de Windows")
            print("  2. Jouez de la musique ou du son pendant le test")
            print("  3. Vérifiez que Minecraft a le son activé")

        print()
        return True

    except Exception as e:
        print()
        print()
        print(f"❌ ERREUR pendant l'enregistrement: {e}")
        return False


if __name__ == "__main__":
    try:
        test_loopback()
    except KeyboardInterrupt:
        print()
        print()
        print("⚠️  Test interrompu par l'utilisateur")
    except Exception as e:
        print()
        print(f"❌ ERREUR inattendue: {e}")
        import traceback
        traceback.print_exc()
