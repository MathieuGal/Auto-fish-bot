"""
Script temporaire pour analyser la vidéo de pêche et extraire des frames
"""
import cv2
import os

def extract_frames(video_path, output_folder="frames_analysis", interval=30):
    """
    Extrait des frames de la vidéo à intervalles réguliers

    Args:
        video_path: Chemin vers la vidéo
        output_folder: Dossier de sortie pour les frames
        interval: Intervalle entre les frames (en nombre de frames)
    """
    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Ouvrir la vidéo
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Erreur: Impossible d'ouvrir la vidéo {video_path}")
        return

    # Obtenir les informations de la vidéo
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    print(f"Analyse de la vidéo:")
    print(f"  - FPS: {fps}")
    print(f"  - Total frames: {total_frames}")
    print(f"  - Durée: {duration:.2f} secondes")
    print(f"  - Extraction tous les {interval} frames\n")

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Sauvegarder la frame tous les X frames
        if frame_count % interval == 0:
            timestamp = frame_count / fps
            output_path = os.path.join(output_folder, f"frame_{frame_count:05d}_t{timestamp:.2f}s.jpg")
            cv2.imwrite(output_path, frame)
            saved_count += 1
            print(f"Frame sauvegardée: {output_path}")

        frame_count += 1

    cap.release()
    print(f"\nExtraction terminée: {saved_count} frames sauvegardées dans '{output_folder}'")

if __name__ == "__main__":
    video_path = "MedalTVScreenRecording20251114091159302.mp4"
    extract_frames(video_path, interval=10)  # Extrait une frame tous les 10 frames
