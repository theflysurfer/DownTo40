@echo off
REM Script de mise à jour et redéploiement du dashboard (Windows)
REM Usage: deploy-update.bat

setlocal EnableDelayedExpansion

set VPS_HOST=root@69.62.108.82
set REMOTE_DIR=/opt/energie-dashboard
set APP_NAME=energie-40eur-dashboard

echo 🚀 Démarrage du déploiement...
echo.

REM 1. Pull latest changes from GitHub
echo 📥 1/4 - Récupération des dernières modifications depuis GitHub...
ssh %VPS_HOST% "cd %REMOTE_DIR% && git pull origin main"
if errorlevel 1 (
    echo ❌ Erreur lors du pull Git
    exit /b 1
)
echo ✅ Code mis à jour
echo.

REM 2. Stop current container
echo 🛑 2/4 - Arrêt du conteneur actuel...
ssh %VPS_HOST% "docker stop %APP_NAME% 2>nul || exit 0"
ssh %VPS_HOST% "docker rm %APP_NAME% 2>nul || exit 0"
echo ✅ Conteneur arrêté
echo.

REM 3. Rebuild Docker image
echo 🔨 3/4 - Reconstruction de l'image Docker...
ssh %VPS_HOST% "cd %REMOTE_DIR% && docker-compose build --no-cache"
if errorlevel 1 (
    echo ❌ Erreur lors du build Docker
    exit /b 1
)
echo ✅ Image reconstruite
echo.

REM 4. Start new container
echo ▶️  4/4 - Démarrage du nouveau conteneur...
ssh %VPS_HOST% "cd %REMOTE_DIR% && docker-compose up -d"
if errorlevel 1 (
    echo ❌ Erreur lors du démarrage
    exit /b 1
)
echo ✅ Conteneur démarré
echo.

REM 5. Wait for startup
echo ⏳ Attente du démarrage de Streamlit (10s)...
timeout /t 10 /nobreak >nul
echo.

REM 6. Check logs
echo 📋 Dernières logs du conteneur:
ssh %VPS_HOST% "docker logs --tail 10 %APP_NAME%"
echo.

REM 7. Test the deployment
echo 🧪 Test de l'application...
curl -I -u julien:DevAccess2025 -s -o nul -w "%%{http_code}" https://energie.srv759970.hstgr.cloud/ > %TEMP%\http_code.txt
set /p HTTP_CODE=<%TEMP%\http_code.txt
del %TEMP%\http_code.txt

if "%HTTP_CODE%"=="200" (
    echo ✅ Déploiement réussi! HTTP %HTTP_CODE%
    echo.
    echo 🌐 Dashboard accessible à: https://energie.srv759970.hstgr.cloud/
    echo 🔐 Credentials: julien / DevAccess2025
) else (
    echo ❌ Erreur! HTTP %HTTP_CODE%
    echo Vérifiez les logs avec: ssh %VPS_HOST% "docker logs %APP_NAME%"
    exit /b 1
)

echo.
echo ✨ Déploiement terminé avec succès!

endlocal
