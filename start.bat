@echo off
echo ========================================
echo Bot de Peche Automatique Minecraft
echo ========================================
echo.
echo IMPORTANT avant de demarrer:
echo 1. Minecraft est ouvert et connecte au serveur
echo 2. Vous etes devant l'eau avec une canne a peche equipee
echo 3. Le SON de Minecraft est ACTIVE (important!)
echo.
echo Appuyez sur '-' dans le jeu pour demarrer/arreter le bot
echo Appuyez sur Ctrl+C ici pour arreter completement
echo.
echo ========================================
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ERREUR lors du lancement!
    echo Verifiez que vous avez bien installe les dependances avec install.bat
    echo.
    pause
)
