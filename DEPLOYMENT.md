# 📦 Guide de Déploiement

Guide complet pour déployer et mettre à jour le dashboard ENTSO-E sur le serveur de production.

## 🌐 URLs et Accès

- **Production**: https://energie.srv759970.hstgr.cloud/
- **Credentials**: `julien` / `DevAccess2025`
- **Serveur**: `root@69.62.108.82`
- **Répertoire**: `/opt/energie-dashboard`
- **GitHub**: https://github.com/theflysurfer/DownTo40.git

---

## 🚀 Déploiement Initial (Déjà fait)

Le déploiement initial a été effectué et comprend:
- ✅ Git configuré sur le serveur
- ✅ Docker + Docker Compose installés
- ✅ Nginx configuré avec SSL (Let's Encrypt)
- ✅ Basic Auth configuré
- ✅ Dashboard en production

---

## 🔄 Workflow de Mise à Jour

### Étape 1: Développement Local

```bash
# Modifier le code
# Par exemple: éditer dashboard_entso_prices.py

# Tester localement
streamlit run dashboard_entso_prices.py

# Commiter les changements
git add .
git commit -m "feat: description des modifications"
git push origin main
```

### Étape 2: Déploiement Automatique

**Sur Windows:**
```bash
deploy-update.bat
```

**Sur Linux/Mac:**
```bash
./deploy-update.sh
```

Le script effectue automatiquement:
1. Pull des dernières modifications depuis GitHub
2. Arrêt du conteneur actuel
3. Reconstruction de l'image Docker
4. Démarrage du nouveau conteneur
5. Vérification du bon fonctionnement

---

## 🛠️ Déploiement Manuel (Avancé)

Si tu veux effectuer le déploiement manuellement:

### 1. Connexion au serveur
```bash
ssh root@69.62.108.82
cd /opt/energie-dashboard
```

### 2. Récupération du code
```bash
git pull origin main
```

### 3. Reconstruction et redémarrage
```bash
# Arrêt du conteneur
docker stop energie-40eur-dashboard
docker rm energie-40eur-dashboard

# Reconstruction
docker-compose build --no-cache

# Démarrage
docker-compose up -d
```

### 4. Vérification
```bash
# Logs du conteneur
docker logs -f energie-40eur-dashboard

# Status
docker ps | grep energie

# Test HTTP
curl -I -u julien:DevAccess2025 https://energie.srv759970.hstgr.cloud/
```

---

## 🔧 Commandes Utiles

### Gestion Docker

```bash
# Voir les logs en temps réel
ssh root@69.62.108.82 "docker logs -f energie-40eur-dashboard"

# Redémarrer le conteneur (sans rebuild)
ssh root@69.62.108.82 "docker restart energie-40eur-dashboard"

# Voir les conteneurs en cours
ssh root@69.62.108.82 "docker ps"

# Voir l'utilisation des ressources
ssh root@69.62.108.82 "docker stats energie-40eur-dashboard --no-stream"

# Shell interactif dans le conteneur
ssh root@69.62.108.82 "docker exec -it energie-40eur-dashboard /bin/bash"
```

### Gestion Git

```bash
# Voir l'état Git sur le serveur
ssh root@69.62.108.82 "cd /opt/energie-dashboard && git status"

# Voir les derniers commits
ssh root@69.62.108.82 "cd /opt/energie-dashboard && git log --oneline -5"

# Forcer la synchronisation avec GitHub
ssh root@69.62.108.82 "cd /opt/energie-dashboard && git fetch origin && git reset --hard origin/main"
```

### Gestion Nginx

```bash
# Recharger la config Nginx
ssh root@69.62.108.82 "nginx -t && systemctl reload nginx"

# Voir les logs Nginx
ssh root@69.62.108.82 "tail -f /var/log/nginx/access.log"
ssh root@69.62.108.82 "tail -f /var/log/nginx/error.log"

# Status Nginx
ssh root@69.62.108.82 "systemctl status nginx"
```

---

## 🐛 Dépannage

### Le dashboard ne répond pas

```bash
# 1. Vérifier que le conteneur tourne
ssh root@69.62.108.82 "docker ps | grep energie"

# 2. Vérifier les logs pour erreurs
ssh root@69.62.108.82 "docker logs --tail 50 energie-40eur-dashboard"

# 3. Redémarrer le conteneur
ssh root@69.62.108.82 "docker restart energie-40eur-dashboard"

# 4. Si ça ne marche toujours pas, rebuild complet
./deploy-update.bat  # ou ./deploy-update.sh
```

### Erreur de syntaxe Python

```bash
# Tester la compilation sur le serveur
ssh root@69.62.108.82 "cd /opt/energie-dashboard && python3 -m py_compile dashboard_entso_prices.py"

# Si erreur, vérifier les différences avec local
ssh root@69.62.108.82 "cd /opt/energie-dashboard && md5sum dashboard_entso_prices.py"
md5sum dashboard_entso_prices.py
```

### Problème de certificat SSL

```bash
# Renouveler le certificat Let's Encrypt
ssh root@69.62.108.82 "certbot renew --nginx"

# Vérifier la date d'expiration
ssh root@69.62.108.82 "certbot certificates"
```

### Port déjà utilisé

```bash
# Voir quel processus utilise le port 8508
ssh root@69.62.108.82 "lsof -i :8508"

# Tuer le processus si nécessaire
ssh root@69.62.108.82 "fuser -k 8508/tcp"
```

---

## 📊 Monitoring

### Vérification quotidienne

```bash
# Script de health check (créer un alias)
alias check-dashboard='curl -I -u julien:DevAccess2025 https://energie.srv759970.hstgr.cloud/ && echo "✅ Dashboard OK"'
```

### Métriques Docker

```bash
# Utilisation mémoire/CPU
ssh root@69.62.108.82 "docker stats energie-40eur-dashboard --no-stream"
```

---

## 🔐 Sécurité

### Credentials

- **Basic Auth**: Configuré dans `/etc/nginx/snippets/basic-auth.conf`
- **Mot de passe**: `DevAccess2025` (changeable via `htpasswd`)

### SSL/TLS

- **Certificat**: Let's Encrypt
- **Renouvellement**: Automatique via certbot
- **Localisation**: `/etc/letsencrypt/live/energie.srv759970.hstgr.cloud/`

### Changer le mot de passe

```bash
ssh root@69.62.108.82
htpasswd -c /etc/nginx/.htpasswd julien
# Entrer le nouveau mot de passe
systemctl reload nginx
```

---

## 📁 Structure des Fichiers sur Serveur

```
/opt/energie-dashboard/
├── .git/                          # Git repository
├── dashboard_entso_prices.py      # Application principale
├── requirements.txt               # Dépendances Python
├── Dockerfile                     # Configuration Docker
├── docker-compose.yml             # Orchestration Docker
├── deploy.sh / deploy.bat         # Scripts de déploiement initial
└── consolidated_prices_2022-2024.csv  # Données
```

---

## 🔄 Rollback (Retour arrière)

Si un déploiement pose problème:

```bash
# 1. Se connecter au serveur
ssh root@69.62.108.82
cd /opt/energie-dashboard

# 2. Voir les derniers commits
git log --oneline -10

# 3. Revenir au commit précédent
git reset --hard <commit-hash>

# 4. Redéployer
docker-compose down
docker-compose up -d --build
```

---

## 📝 Checklist de Déploiement

Avant chaque déploiement, vérifier:

- [ ] Tests locaux passent (`streamlit run dashboard_entso_prices.py`)
- [ ] Code commité et pushé sur GitHub
- [ ] Fichiers sensibles (.env, credentials) dans .gitignore
- [ ] Dashboard accessible après déploiement
- [ ] Pas d'erreurs dans les logs Docker
- [ ] Basic Auth fonctionne

---

## 🆘 Support

En cas de problème:
1. Consulter les logs: `docker logs energie-40eur-dashboard`
2. Vérifier la section Dépannage ci-dessus
3. Rollback au commit précédent si nécessaire

---

## 🎯 Prochaines Étapes

### Phase 2 - Enrichissement données

- [ ] Scraper flux transfrontaliers (exports/imports)
- [ ] Scraper production par type (nucléaire, renouvelables)
- [ ] Enrichir dashboard avec nouvelles analyses
- [ ] Répondre aux 3 questions métier en MWh réels

### Améliorations infrastructure

- [ ] Mettre en place CI/CD (GitHub Actions)
- [ ] Monitoring automatique (Uptime Robot / Healthchecks.io)
- [ ] Backups automatiques des données
- [ ] Logging centralisé
