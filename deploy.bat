@echo off
REM Script de deploiement Dashboard Energie (Windows)
REM Usage: deploy.bat

setlocal enabledelayedexpansion

set VPS_HOST=root@69.62.108.82
set APP_NAME=energie-dashboard
set REMOTE_DIR=/opt/%APP_NAME%

echo ================================================================================
echo   DEPLOIEMENT DASHBOARD ENERGIE - srv759970.hstgr.cloud
echo ================================================================================
echo.

echo [1/8] Verification connexion SSH...
ssh -o ConnectTimeout=5 %VPS_HOST% "echo SSH OK" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Impossible de se connecter au VPS
    echo Verifiez: ssh %VPS_HOST%
    pause
    exit /b 1
)
echo [OK] Connexion SSH etablie
echo.

echo [2/8] Creation repertoire distant...
ssh %VPS_HOST% "mkdir -p %REMOTE_DIR%"
echo [OK] Repertoire %REMOTE_DIR% cree
echo.

echo [3/8] Transfert fichiers application...
scp dashboard_entso_prices.py %VPS_HOST%:%REMOTE_DIR%/
scp Dockerfile %VPS_HOST%:%REMOTE_DIR%/
scp docker-compose.yml %VPS_HOST%:%REMOTE_DIR%/
scp requirements.txt %VPS_HOST%:%REMOTE_DIR%/
scp -r data %VPS_HOST%:%REMOTE_DIR%/
echo [OK] Fichiers transferes
echo.

echo [4/8] Build image Docker sur le serveur...
echo (Cette etape peut prendre 2-5 minutes)
ssh %VPS_HOST% "cd %REMOTE_DIR% && docker-compose build"
if %errorlevel% neq 0 (
    echo [ERREUR] Echec du build Docker
    pause
    exit /b 1
)
echo [OK] Image Docker construite
echo.

echo [5/8] Demarrage conteneur...
ssh %VPS_HOST% "cd %REMOTE_DIR% && docker-compose up -d"
if %errorlevel% neq 0 (
    echo [ERREUR] Echec demarrage conteneur
    pause
    exit /b 1
)
echo [OK] Conteneur demarre
echo.

echo [6/8] Attente demarrage application (15s)...
timeout /t 15 /nobreak >nul
echo.

echo [7/8] Creation configuration Nginx...
ssh %VPS_HOST% "cat > /etc/nginx/sites-available/energie << 'EOFNGINX'
server {
    listen 443 ssl http2;
    server_name energie.srv759970.hstgr.cloud;

    ssl_certificate /etc/letsencrypt/live/srv759970.hstgr.cloud/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/srv759970.hstgr.cloud/privkey.pem;

    include snippets/basic-auth.conf;

    location / {
        proxy_pass http://localhost:8508;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection \"upgrade\";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    location /_stcore/health {
        proxy_pass http://localhost:8508/_stcore/health;
        proxy_http_version 1.1;
        access_log off;
    }
}

server {
    listen 80;
    server_name energie.srv759970.hstgr.cloud;
    return 301 https://$server_name$request_uri;
}
EOFNGINX"
echo [OK] Configuration Nginx creee
echo.

echo [8/8] Activation site et rechargement Nginx...
ssh %VPS_HOST% "ln -sf /etc/nginx/sites-available/energie /etc/nginx/sites-enabled/energie"
ssh %VPS_HOST% "nginx -t && systemctl reload nginx"
if %errorlevel% neq 0 (
    echo [ERREUR] Configuration Nginx invalide
    ssh %VPS_HOST% "cat /var/log/nginx/error.log | tail -20"
    pause
    exit /b 1
)
echo [OK] Nginx reconfigure et recharge
echo.

echo ================================================================================
echo   DEPLOIEMENT TERMINE AVEC SUCCES!
echo ================================================================================
echo.
echo URL Dashboard: https://energie.srv759970.hstgr.cloud/
echo.
echo Credentials Basic Auth:
echo   Username: julien
echo   Password: DevAccess2025
echo.
echo Commandes utiles:
echo   - Logs:    ssh %VPS_HOST% "docker logs -f %APP_NAME%"
echo   - Restart: ssh %VPS_HOST% "docker restart %APP_NAME%"
echo   - Stop:    ssh %VPS_HOST% "docker stop %APP_NAME%"
echo   - Status:  ssh %VPS_HOST% "docker ps | grep %APP_NAME%"
echo.
echo Tester maintenant:
echo   curl -I -u julien:DevAccess2025 https://energie.srv759970.hstgr.cloud/
echo.
echo ================================================================================
echo.

set /p OPEN="Ouvrir dans le navigateur ? (O/N): "
if /i "%OPEN%"=="O" (
    start https://energie.srv759970.hstgr.cloud/
)

pause
