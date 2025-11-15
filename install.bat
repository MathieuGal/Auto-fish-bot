@echo off
echo ========================================
echo Installation Bot de Peche Minecraft
echo ========================================
echo.

echo [1/3] Verification de Python...
python --version
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH!
    echo.
    echo Installez Python 3.10, 3.11 ou 3.12 depuis:
    echo https://www.python.org/downloads/
    echo.
    echo N'oubliez pas de cocher "Add Python to PATH" lors de l'installation!
    echo.
    pause
    exit /b 1
)
echo.
echo IMPORTANT: Ce bot necessite Python 3.10, 3.11 ou 3.12
echo Si vous avez une version plus ancienne, le bot ne fonctionnera pas!
echo.
echo OK - Python detecte!
echo.

echo [2/3] Mise a jour de pip...
python -m pip install --upgrade pip
echo.

echo [3/3] Installation des dependances...
python -m pip install -r requirements.txt
echo.

if errorlevel 1 (
    echo.
    echo ERREUR lors de l'installation!
    echo Verifiez votre connexion Internet et reessayez.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation terminee avec succes!
echo ========================================
echo.
echo Vous pouvez maintenant lancer le bot avec: python main.py
echo Ou double-cliquez sur start.bat
echo.
pause
