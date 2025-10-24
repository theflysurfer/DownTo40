#!/bin/bash

# Script de mise à jour et redéploiement du dashboard
# Usage: ./deploy-update.sh

set -e  # Exit on error

VPS_HOST="root@69.62.108.82"
REMOTE_DIR="/opt/energie-dashboard"
APP_NAME="energie-40eur-dashboard"

echo "🚀 Démarrage du déploiement..."
echo ""

# 1. Pull latest changes from GitHub
echo "📥 1/4 - Récupération des dernières modifications depuis GitHub..."
ssh $VPS_HOST "cd $REMOTE_DIR && git pull origin main"
echo "✅ Code mis à jour"
echo ""

# 2. Stop current container
echo "🛑 2/4 - Arrêt du conteneur actuel..."
ssh $VPS_HOST "docker stop $APP_NAME || true"
ssh $VPS_HOST "docker rm $APP_NAME || true"
echo "✅ Conteneur arrêté"
echo ""

# 3. Rebuild Docker image
echo "🔨 3/4 - Reconstruction de l'image Docker..."
ssh $VPS_HOST "cd $REMOTE_DIR && docker-compose build --no-cache"
echo "✅ Image reconstruite"
echo ""

# 4. Start new container
echo "▶️  4/4 - Démarrage du nouveau conteneur..."
ssh $VPS_HOST "cd $REMOTE_DIR && docker-compose up -d"
echo "✅ Conteneur démarré"
echo ""

# 5. Wait for startup
echo "⏳ Attente du démarrage de Streamlit (10s)..."
sleep 10

# 6. Check logs
echo ""
echo "📋 Dernières logs du conteneur:"
ssh $VPS_HOST "docker logs --tail 10 $APP_NAME"
echo ""

# 7. Test the deployment
echo "🧪 Test de l'application..."
HTTP_CODE=$(curl -I -u julien:DevAccess2025 -s -o /dev/null -w "%{http_code}" https://energie.srv759970.hstgr.cloud/)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Déploiement réussi! HTTP $HTTP_CODE"
    echo ""
    echo "🌐 Dashboard accessible à: https://energie.srv759970.hstgr.cloud/"
    echo "🔐 Credentials: julien / DevAccess2025"
else
    echo "❌ Erreur! HTTP $HTTP_CODE"
    echo "Vérifiez les logs avec: ssh $VPS_HOST 'docker logs $APP_NAME'"
    exit 1
fi

echo ""
echo "✨ Déploiement terminé avec succès!"
