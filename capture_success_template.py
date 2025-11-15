"""
Script pour capturer le template du message de succès de pêche
INSTRUCTIONS:
1. Lancez ce script: python capture_success_template.py
2. Lancez Minecraft et pêchez un poisson
3. Quand le message de succès apparaît, appuyez sur ESPACE
4. Le template sera sauvegardé dans vision/templates/success_message.png
"""

import cv2
import numpy as np
import keyboard
import time
from vision.screen_capture import capture_screen

def main():
    print("=" * 70)
    print("🎣 CAPTURE DU TEMPLATE DE MESSAGE DE SUCCÈS")
    print("=" * 70)
    print()
    print("INSTRUCTIONS:")
    print("  1. Lancez Minecraft et allez à l'endroit où vous pêchez")
    print("  2. Pêchez un poisson et attendez la fin des QTE")
    print("  3. Quand le MESSAGE DE SUCCÈS apparaît sur l'écran,")
    print("     appuyez sur ESPACE pour capturer le template")
    print()
    print("Le script va capturer l'écran en continu.")
    print("Appuyez sur ESPACE au bon moment!")
    print()
    print("Appuyez sur ESC pour annuler")
    print()
    print("-" * 70)
    print("En attente... (appuyez sur ESPACE quand le message apparaît)")
    print("-" * 70)

    # Créer une fenêtre de prévisualisation
    window_name = "Aperçu écran - Appuyez ESPACE pour capturer"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    captured = False

    try:
        while not captured:
            # Capturer l'écran
            screen = capture_screen()

            # Redimensionner pour l'affichage
            display = cv2.resize(screen, (960, 540))  # 50% de 1920x1080

            # Ajouter du texte d'instruction
            cv2.putText(display, "Appuyez ESPACE quand le message de succes apparait",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(display, "ESC pour annuler",
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # Afficher
            cv2.imshow(window_name, display)
            cv2.waitKey(1)

            # Vérifier les touches
            if keyboard.is_pressed('space'):
                print()
                print("📸 Capture en cours...")
                time.sleep(0.3)  # Anti-rebond

                # Capturer à nouveau pour être sûr
                screen = capture_screen()

                # Sauvegarder l'image complète
                cv2.imwrite("vision/templates/success_message_full.png", screen)
                print("✅ Image complète sauvegardée: vision/templates/success_message_full.png")
                print()

                # Demander à l'utilisateur de sélectionner la zone
                print("Maintenant, sélectionnez la zone du MESSAGE avec la souris:")
                print("  1. Cliquez et glissez pour sélectionner la zone")
                print("  2. Appuyez sur ENTRÉE pour valider")
                print("  3. Appuyez sur C pour annuler et recommencer")
                print()

                # Sélection de la zone
                roi = cv2.selectROI("Sélectionnez le message de succès", screen, False, False)
                cv2.destroyWindow("Sélectionnez le message de succès")

                if roi[2] > 0 and roi[3] > 0:  # Vérifier qu'une zone a été sélectionnée
                    x, y, w, h = roi
                    template = screen[y:y+h, x:x+w]

                    # Sauvegarder le template
                    cv2.imwrite("vision/templates/success_message.png", template)
                    print()
                    print("✅ Template sauvegardé: vision/templates/success_message.png")
                    print(f"   Taille: {w}x{h} pixels")
                    print(f"   Position: ({x}, {y})")
                    print()
                    print("Configuration recommandée pour config.py:")
                    print("-" * 70)
                    print(f"SUCCESS_MESSAGE_TEMPLATE = 'vision/templates/success_message.png'")
                    print(f"SUCCESS_DETECTION_ENABLED = True")
                    print(f"SUCCESS_DETECTION_THRESHOLD = 0.8  # Ajustez si nécessaire")
                    print("-" * 70)
                    print()

                    # Afficher le template capturé
                    print("Aperçu du template capturé:")
                    cv2.imshow("Template capturé", template)
                    print("Appuyez sur une touche pour fermer...")
                    cv2.waitKey(0)

                    captured = True
                else:
                    print("❌ Aucune zone sélectionnée. Appuyez à nouveau sur ESPACE pour réessayer.")

            elif keyboard.is_pressed('esc'):
                print()
                print("❌ Annulé par l'utilisateur")
                break

            time.sleep(0.1)

    except KeyboardInterrupt:
        print()
        print("❌ Interrompu par l'utilisateur")

    finally:
        cv2.destroyAllWindows()

    if captured:
        print()
        print("🎉 Capture réussie!")
        print()
        print("PROCHAINES ÉTAPES:")
        print("  1. Ajoutez les lignes de configuration dans config.py")
        print("  2. Relancez le bot: python main.py")
        print("  3. Le bot détectera automatiquement la fin des QTE!")
        print()

if __name__ == "__main__":
    main()
