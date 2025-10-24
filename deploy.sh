#!/bin/bash
# Script de deploiement Dashboard Energie - srv759970.hstgr.cloud
# Usage: bash deploy.sh

set -e

echo "================================================================================"
echo "  DEPLOIEMENT DASHBOARD ENERGIE - srv759970.hstgr.cloud"
echo "================================================================================"
echo ""

VPS_HOST="root@69.62.108.82"
APP_NAME="energie-dashboard"
REMOTE_DIR="/opt/${APP_NAME}"
LOCAL_DIR="."

echo "[1/8] Verification connexion SSH..."
ssh -o ConnectTimeout=5 ${VPS_HOST} "echo 'SSH OK'" || {
    echo "[ERREUR] Impossible de se connecter au VPS"
    echo "Verifiez votre connexion SSH avec: ssh ${VPS_HOST}"
    exit 1
}
echo "[OK] Connexion SSH etablie"
echo ""

echo "[2/8] Creation repertoire distant..."
ssh ${VPS_HOST} "mkdir -p ${REMOTE_DIR}"
echo "[OK] Repertoire ${REMOTE_DIR} cree"
echo ""

echo "[3/8] Transfert fichiers application..."
# Transfert fichiers essentiels
scp dashboard_entso_prices.py ${VPS_HOST}:${REMOTE_DIR}/
scp Dockerfile ${VPS_HOST}:${REMOTE_DIR}/
scp docker-compose.yml ${VPS_HOST}:${REMOTE_DIR}/
scp requirements.txt ${VPS_HOST}:${REMOTE_DIR}/

# Transfert donnees
scp -r data ${VPS_HOST}:${REMOTE_DIR}/

echo "[OK] Fichiers transferes"
echo ""

echo "[4/8] Build image Docker sur le serveur..."
ssh ${VPS_HOST} "cd ${REMOTE_DIR} && docker-compose build" || {
    echo "[ERREUR] Echec du build Docker"
    exit 1
}
echo "[OK] Image Docker construite"
echo ""

echo "[5/8] Demarrage conteneur..."
ssh ${VPS_HOST} "cd ${REMOTE_DIR} && docker-compose up -d" || {
    echo "[ERREUR] Echec demarrage conteneur"
    exit 1
}
echo "[OK] Conteneur demarre"
echo ""

echo "[6/8] Attente demarrage application (15s)..."
sleep 15
echo ""

echo "[7/8] Creation configuration Nginx..."
ssh ${VPS_HOST} "cat > /etc/nginx/sites-available/energie << 'EOF'
server {
    listen 443 ssl http2;
    server_name energie.srv759970.hstgr.cloud;

    ssl_certificate /etc/letsencrypt/live/srv759970.hstgr.cloud/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/srv759970.hstgr.cloud/privkey.pem;

    # Basic Auth
    include snippets/basic-auth.conf;

    # Streamlit WebSocket support
    location / {
        proxy_pass http://localhost:8508;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \\\$http_upgrade;
        proxy_set_header Connection \"upgrade\";
        proxy_set_header Host \\\$host;
        proxy_set_header X-Real-IP \\\$remote_addr;
        proxy_set_header X-Forwarded-For \\\$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \\\$scheme;
        proxy_read_timeout 86400;
    }

    # Health check endpoint
    location /_stcore/health {
        proxy_pass http://localhost:8508/_stcore/health;
        proxy_http_version 1.1;
        access_log off;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name energie.srv759970.hstgr.cloud;
    return 301 https://\\\$server_name\\\$request_uri;
}
EOF"

echo "[OK] Configuration Nginx creee"
echo ""

echo "[8/8] Activation site et rechargement Nginx..."
ssh ${VPS_HOST} "ln -sf /etc/nginx/sites-available/energie /etc/nginx/sites-enabled/energie"
ssh ${VPS_HOST} "nginx -t && systemctl reload nginx" || {
    echo "[ERREUR] Configuration Nginx invalide"
    ssh ${VPS_HOST} "cat /var/log/nginx/error.log | tail -20"
    exit 1
}
echo "[OK] Nginx reconfigure et recharge"
echo ""

echo "================================================================================"
echo "  DEPLOIEMENT TERMINE AVEC SUCCES!"
echo "================================================================================"
echo ""
echo "URL Dashboard: https://energie.srv759970.hstgr.cloud/"
echo ""
echo "Credentials Basic Auth:"
echo "  Username: julien"
echo "  Password: DevAccess2025"
echo ""
echo "Commandes utiles:"
echo "  - Logs dashboard:  ssh ${VPS_HOST} 'docker logs -f ${APP_NAME}'"
echo "  - Restart:         ssh ${VPS_HOST} 'docker restart ${APP_NAME}'"
echo "  - Stop:            ssh ${VPS_HOST} 'docker stop ${APP_NAME}'"
echo "  - Status:          ssh ${VPS_HOST} 'docker ps | grep ${APP_NAME}'"
echo ""
echo "Tester maintenant:"
echo "  curl -I -u julien:DevAccess2025 https://energie.srv759970.hstgr.cloud/"
echo ""
echo "================================================================================"
