"""
Détecteur audio pour les morsures de poisson
Détecte le son "entity.bobber.splash" de Minecraft
Utilise WASAPI loopback pour capturer l'audio système (sortie audio)
"""

import sys
import os

# Ajouter le dossier parent au path pour pouvoir importer config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import soundcard as sc
from scipy import signal
import time
import queue
import threading
import config


class SoundDetector:
    """Détecteur audio pour les sons de morsure de poisson (via WASAPI loopback)"""

    def __init__(self):
        """Initialise le détecteur audio"""
        self.sample_rate = config.AUDIO_SAMPLE_RATE
        self.chunk_size = config.AUDIO_CHUNK_SIZE
        self.threshold = config.AUDIO_THRESHOLD

        # Périphérique loopback (audio système)
        self.loopback_mic = None
        self.recorder = None
        self.is_listening = False
        self.recording_thread = None
        self.stop_recording = threading.Event()

        # Buffer pour stocker les données audio (taille augmentée pour éviter pertes)
        self.audio_queue = queue.Queue(maxsize=100)  # Buffer plus grand pour gérer les pics

        # Historique des amplitudes pour détecter les pics
        self.amplitude_history = []
        self.history_size = 20

        # Dernière détection
        self.last_detection_time = 0
        self.detection_cooldown = 0.3  # Éviter les doubles détections (réduit pour meilleure réactivité)

        # Temps de démarrage de l'écoute (pour ignorer le bruit du lancer)
        self.listening_start_time = 0

        # Initialiser le périphérique loopback
        self._init_loopback_device()

    def _init_loopback_device(self):
        """Initialise le périphérique de loopback (audio système)"""
        try:
            # Obtenir le haut-parleur par défaut comme source d'enregistrement (loopback)
            default_speaker = sc.default_speaker()
            if default_speaker is None:
                raise RuntimeError("Aucun haut-parleur par défaut trouvé")

            # Créer le microphone loopback
            self.loopback_mic = sc.get_microphone(
                id=str(default_speaker.name),
                include_loopback=True
            )
            print(f"[SoundDetector] Périphérique loopback initialisé: {default_speaker.name}")

        except Exception as e:
            print(f"[SoundDetector] ERREUR lors de l'initialisation du loopback: {e}")
            print("[SoundDetector] Assurez-vous que:")
            print("  1. Votre système a une sortie audio active")
            print("  2. Le son système n'est pas coupé")
            print("  3. La bibliothèque soundcard est installée (pip install soundcard)")
            raise

    def _recording_loop(self):
        """Boucle d'enregistrement en arrière-plan"""
        try:
            with self.loopback_mic.recorder(samplerate=self.sample_rate) as recorder:
                self.recorder = recorder
                print(f"[SoundDetector] Enregistrement démarré (loopback WASAPI)")

                while not self.stop_recording.is_set():
                    # Enregistrer un bloc audio
                    data = recorder.record(numframes=self.chunk_size)

                    # Convertir en mono si nécessaire (moyenne des canaux)
                    if len(data.shape) > 1 and data.shape[1] > 1:
                        data = np.mean(data, axis=1)

                    # Ajouter à la queue (avec gestion si pleine)
                    try:
                        self.audio_queue.put(data.copy(), timeout=0.1)
                    except queue.Full:
                        # Queue pleine, supprimer ancien élément et réessayer
                        try:
                            self.audio_queue.get_nowait()
                            self.audio_queue.put(data.copy(), timeout=0.1)
                        except (queue.Empty, queue.Full):
                            pass  # Ignorer si échec

        except Exception as e:
            print(f"[SoundDetector] Erreur dans la boucle d'enregistrement: {e}")
        finally:
            self.recorder = None

    def start_listening(self):
        """Démarre l'écoute audio (loopback système)"""
        if self.is_listening:
            return

        try:
            self.stop_recording.clear()
            self.recording_thread = threading.Thread(target=self._recording_loop, daemon=True)
            self.recording_thread.start()
            self.is_listening = True
            print(f"[SoundDetector] Capture audio système démarrée (WASAPI loopback)")
            print(f"[SoundDetector] 🔊 Le bot écoute maintenant la SORTIE AUDIO de votre PC!")

        except Exception as e:
            print(f"[SoundDetector] Erreur lors du démarrage: {e}")
            raise

    def stop_listening(self):
        """Arrête l'écoute audio"""
        if not self.is_listening:
            return

        self.stop_recording.set()
        if self.recording_thread:
            self.recording_thread.join(timeout=2.0)
            self.recording_thread = None

        self.is_listening = False
        print("[SoundDetector] Capture audio système arrêtée")

    def detect_splash_sound(self) -> bool:
        """
        Détecte un son de splash (morsure de poisson)

        Returns:
            True si un splash est détecté
        """
        if not self.is_listening:
            return False

        try:
            # Récupérer les données audio
            audio_data = self.audio_queue.get(timeout=0.1)

            # Calculer l'amplitude RMS (Root Mean Square)
            rms = np.sqrt(np.mean(audio_data**2))

            # Convertir en décibels
            if rms > 0:
                db = 20 * np.log10(rms)
            else:
                db = -100

            # Ajouter à l'historique
            self.amplitude_history.append(rms)
            if len(self.amplitude_history) > self.history_size:
                self.amplitude_history.pop(0)

            # Logger en mode DEBUG
            if config.LOG_LEVEL == 'DEBUG':
                print(f"[SoundDetector] RMS: {rms:.6f}, dB: {db:.2f}, Seuil: {self.threshold}")

            # Détecter un pic sonore
            if len(self.amplitude_history) >= 3:
                # Moyenne des dernières valeurs
                avg_amplitude = np.mean(self.amplitude_history[:-1])
                current_amplitude = self.amplitude_history[-1]

                # Vérifier si c'est un pic significatif
                # Le son doit être au moins 3x plus fort que la moyenne
                amplitude_ratio = current_amplitude / (avg_amplitude + 1e-6)

                # Cooldown pour éviter les doubles détections
                time_since_last = time.time() - self.last_detection_time

                # Ignorer les sons pendant les premières secondes (bruit du lancer)
                time_since_start = time.time() - self.listening_start_time
                if time_since_start < config.AUDIO_IGNORE_AFTER_CAST:
                    if config.LOG_LEVEL == 'DEBUG':
                        print(f"[SoundDetector] Son ignoré (période de démarrage: {time_since_start:.1f}s / {config.AUDIO_IGNORE_AFTER_CAST}s)")
                    return False

                if (current_amplitude > self.threshold and
                    amplitude_ratio > 3.0 and
                    time_since_last > self.detection_cooldown):

                    self.last_detection_time = time.time()
                    print(f"[SoundDetector] 🎣 SPLASH DÉTECTÉ! RMS: {current_amplitude:.6f}, Ratio: {amplitude_ratio:.2f}x")
                    return True

            return False

        except queue.Empty:
            return False
        except Exception as e:
            if config.LOG_LEVEL == 'DEBUG':
                print(f"[SoundDetector] Erreur: {e}")
            return False

    def wait_for_bite(self, timeout: float = None) -> bool:
        """
        Attend qu'un poisson morde (détection audio)

        Args:
            timeout: Temps d'attente maximum en secondes

        Returns:
            True si une morsure est détectée, False si timeout
        """
        if timeout is None:
            timeout = config.MAX_WAIT_FOR_BITE

        start_time = time.time()

        # Démarrer l'écoute si pas déjà active
        if not self.is_listening:
            self.start_listening()
            time.sleep(0.5)  # Laisser le temps au stream de démarrer

        # VIDER la queue audio pour éviter de traiter de vieilles données du cycle précédent
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break

        if config.LOG_LEVEL == 'DEBUG':
            print("[SoundDetector] Queue audio vidée - Prêt pour nouvelle détection")

        # Réinitialiser l'historique et le temps de démarrage (pour ignorer le bruit du lancer)
        self.amplitude_history = []
        self.listening_start_time = time.time()

        print(f"[SoundDetector] En attente d'un splash (timeout: {timeout}s)...")
        print(f"[SoundDetector] 🔊 Assurez-vous que le son de Minecraft est activé et audible!")
        print(f"[SoundDetector] ⏱️  Ignorer le son pendant {config.AUDIO_IGNORE_AFTER_CAST}s (bruit du lancer)...")

        while (time.time() - start_time) < timeout:
            if self.detect_splash_sound():
                print("[SoundDetector] OK - Morsure detectee par audio!")
                return True

            # Petit délai pour ne pas surcharger le CPU (réduit pour meilleure réactivité)
            time.sleep(0.005)  # Réduit de 10ms à 5ms

        print("[SoundDetector] Timeout: aucune morsure detectee")
        return False

    def calibrate_threshold(self, duration: float = 10.0):
        """
        Calibre le seuil de détection en mesurant le bruit ambiant

        Args:
            duration: Durée de calibration en secondes
        """
        print(f"\n[SoundDetector] CALIBRATION DU SEUIL")
        print("=" * 60)
        print("Ne faites AUCUN bruit pendant la calibration...")
        print(f"Mesure du bruit ambiant pendant {duration} secondes...")
        print()

        if not self.is_listening:
            self.start_listening()
            time.sleep(0.5)

        amplitudes = []
        start_time = time.time()

        while (time.time() - start_time) < duration:
            try:
                audio_data = self.audio_queue.get(timeout=0.1)
                rms = np.sqrt(np.mean(audio_data**2))
                amplitudes.append(rms)

                # Afficher la progression
                progress = (time.time() - start_time) / duration * 100
                print(f"\rProgression: {progress:.0f}% | RMS actuel: {rms:.6f}", end="")

            except queue.Empty:
                continue

        print("\n")

        if amplitudes:
            avg_noise = np.mean(amplitudes)
            max_noise = np.max(amplitudes)
            std_noise = np.std(amplitudes)

            # Le seuil recommandé est 5x le bruit maximum
            recommended_threshold = max_noise * 5

            print("Resultats de calibration:")
            print(f"   Bruit moyen: {avg_noise:.6f}")
            print(f"   Bruit maximum: {max_noise:.6f}")
            print(f"   Ecart-type: {std_noise:.6f}")
            print(f"   Seuil recommande: {recommended_threshold:.6f}")
            print()
            print(f"Ajoutez cette ligne dans config.py:")
            print(f"   AUDIO_THRESHOLD = {recommended_threshold:.6f}")
            print()
        else:
            print("ERREUR - Aucune donnee collectee!")

    def test_detection(self, duration: float = 30.0):
        """
        Mode test pour vérifier la détection

        Args:
            duration: Durée du test en secondes
        """
        print(f"\n[SoundDetector] MODE TEST")
        print("=" * 60)
        print(f"Test de detection pendant {duration} secondes...")
        print("Faites du bruit ou lancez une ligne de peche dans Minecraft!")
        print("Les detections seront affichees en temps reel.")
        print()

        if not self.is_listening:
            self.start_listening()
            time.sleep(0.5)

        start_time = time.time()
        detection_count = 0

        while (time.time() - start_time) < duration:
            if self.detect_splash_sound():
                detection_count += 1
                elapsed = time.time() - start_time
                print(f"[{elapsed:.1f}s] Detection #{detection_count}")

            time.sleep(0.01)

        print()
        print(f"Test termine: {detection_count} detections en {duration}s")


# Instance globale
_sound_detector_instance = None


def get_sound_detector() -> SoundDetector:
    """
    Obtient l'instance globale du détecteur audio

    Returns:
        Instance de SoundDetector
    """
    global _sound_detector_instance
    if _sound_detector_instance is None:
        _sound_detector_instance = SoundDetector()
    return _sound_detector_instance


if __name__ == "__main__":
    import sys

    print("Detecteur Audio de Morsure - Minecraft")
    print()

    if len(sys.argv) > 1 and sys.argv[1] == "calibrate":
        # Mode calibration
        detector = SoundDetector()
        detector.calibrate_threshold(duration=10.0)
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        # Mode test
        detector = SoundDetector()
        detector.test_detection(duration=30.0)
    else:
        # Mode normal
        print("Usage:")
        print("  python audio/sound_detector.py calibrate  - Calibrer le seuil")
        print("  python audio/sound_detector.py test       - Tester la detection")
        print()
        print("Ou utilisez directement le bot avec audio active!")
