# Plan de Déploiement Dashboard Énergie

## Statut Actuel (24 octobre 2025, 14:41)

### ✅ TERMINÉ - Phase 1: Scraping & Consolidation

**Scraping ENTSO-E (Playwright):**
- ✅ 2024: 365/366 dates (99.7%) - 8,782 heures - 0 erreurs
- ✅ 2023: 365/365 dates (100%) - 8,760 heures - 0 erreurs
- ✅ 2022: 363/365 dates (99.5%) - 8,712 heures - 2 erreurs

**Total scraped:** 26,254 heures de prix Day-Ahead France (2022-2024)

**Consolidation CSV:**
- ✅ `data/processed/entsoe_2022_2024_prices_full.csv` (26,242 records)
- ✅ `data/processed/entsoe_2022_2024_summary.csv` (résumé annuel)
- ✅ `data/processed/entsoe_2022_2024_monthly.csv` (breakdown mensuel)
- ✅ `data/processed/entsoe_2022_2024_below_40.csv` (4,201 heures ≤40€)

**Insights Clés:**
```
2022 (Crise énergétique):
- Prix moyen: 275.92 EUR/MWh
- Heures ≤40€: 82 (0.9%) - CATASTROPHIQUE
- Prix max: 2,987€/MWh

2023 (Récupération):
- Prix moyen: 96.84 EUR/MWh
- Heures ≤40€: 1,033 (11.8%) - MOYEN
- 147 heures à prix négatifs

2024 (Abondance):
- Prix moyen: 57.88 EUR/MWh
- Heures ≤40€: 3,090 (35.2%) - EXCELLENT
- 352 heures à prix négatifs
- Mars-Avril: période d'or (plusieurs jours à 100% ≤40€)
```

### ⚠️ EN ATTENTE - Phase 2: Déploiement Dashboard

**Problème identifié:**
- URL cible: `https://energie.srv759970.hstgr.cloud/`
- Status: 401 Unauthorized (même avec credentials `julien:DevAccess2025`)
- Cause probable: Dashboard jamais déployé sur ce domaine
- Aucune config Nginx "energie" trouvée dans les configs serveur

**Dashboard local prêt:**
- ✅ `dashboard_entso_prices.py` (Streamlit 4 pages)
- ✅ Dockerfile existant
- ✅ docker-compose.yml existant
- ✅ Données consolidées prêtes

---

## Options de Déploiement

### Option 1: Déploiement SSH Manuel (RECOMMANDÉ)

**Prérequis:**
- Accès SSH: `ssh root@69.62.108.82`
- Documentation: `C:\Users\JulienFernandez\OneDrive\Coding\_référentiels de code\Hostinger\scripts\deploy.bat`

**Étapes:**

1. **Transférer les fichiers au VPS:**
```bash
# Depuis Windows
scp -r "C:\Users\JulienFernandez\OneDrive\Coding\_Projets de code\2025.10 40 euros du MWh" root@69.62.108.82:/opt/energie-dashboard/
```

2. **SSH vers le serveur:**
```bash
ssh root@69.62.108.82
cd /opt/energie-dashboard
```

3. **Build Docker:**
```bash
docker-compose build
docker-compose up -d
```

4. **Configurer Nginx:**
```bash
# Créer config Nginx
nano /etc/nginx/sites-available/energie

# Contenu suggéré:
server {
    listen 443 ssl http2;
    server_name energie.srv759970.hstgr.cloud;

    ssl_certificate /etc/letsencrypt/live/srv759970.hstgr.cloud/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/srv759970.hstgr.cloud/privkey.pem;

    include snippets/basic-auth.conf;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Activer le site
ln -s /etc/nginx/sites-available/energie /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

5. **Vérifier:**
```bash
docker ps | grep energie
curl -I -u julien:DevAccess2025 https://energie.srv759970.hstgr.cloud/
```

### Option 2: Script Automatique `deploy.bat`

**Usage:**
```bash
cd "C:\Users\JulienFernandez\OneDrive\Coding\_référentiels de code\Hostinger\scripts"
deploy.bat
# Choisir:
# Type: 1 (Streamlit)
# Nom: energie-dashboard
# Projet: C:\Users\...\2025.10 40 euros du MWh
```

**Limites:**
- Ne configure pas automatiquement Nginx
- Nécessite configuration manuelle du domaine après

### Option 3: Déploiement Local pour Tests

**Usage immédiat (local):**
```bash
cd "C:\Users\JulienFernandez\OneDrive\Coding\_Projets de code\2025.10 40 euros du MWh"
streamlit run dashboard_entso_prices.py
```

Accessible sur: `http://localhost:8501`

---

## Checklist Déploiement

- [ ] Transférer fichiers vers VPS (`scp` ou `rsync`)
- [ ] Build image Docker sur le serveur
- [ ] Lancer conteneur Docker
- [ ] Créer config Nginx `/etc/nginx/sites-available/energie`
- [ ] Activer site (symlink)
- [ ] Recharger Nginx
- [ ] Tester avec credentials Basic Auth
- [ ] Vérifier logs: `docker logs energie-dashboard`

---

## Commandes Utiles Post-Déploiement

```bash
# Voir logs dashboard
docker logs -f energie-dashboard

# Redémarrer dashboard
docker restart energie-dashboard

# Voir tous les containers
docker ps

# Update données (re-run scraping)
cd /opt/energie-dashboard
node scripts/14_scrape_any_year.js 2024
python scripts/16_consolidate_entsoe_prices.py
docker restart energie-dashboard

# Logs Nginx
tail -f /var/log/nginx/energie-access.log
tail -f /var/log/nginx/energie-error.log
```

---

## Phase 3 (Optionnel): Données Complémentaires

### Sources Identifiées ENTSO-E:

1. **Generation by Production Type** (PRIORITÉ)
   - Script prêt: `scripts/15_scrape_generation_by_type.js`
   - Données: Nuclear, Wind, Solar, Hydro, Gas, etc.
   - But: Corréler prix bas ↔ surproduction renouvelables

2. **Actual Total Load**
   - Données: Demande électrique réelle
   - But: Identifier heures creuses vs heures pleines

3. **Cross-Border Physical Flow**
   - Données: Imports/Exports France
   - But: Comprendre prix négatifs (surplus exporté)

**Commandes scraping Phase 3:**
```bash
node scripts/15_scrape_generation_by_type.js 2024
node scripts/15_scrape_generation_by_type.js 2023
node scripts/15_scrape_generation_by_type.js 2022
```

---

## Contact & Support

**Serveur VPS:**
- Host: `69.62.108.82`
- Domaine: `srv759970.hstgr.cloud`
- SSH: `root@69.62.108.82`

**Documentation complète:**
- Hostinger: `C:\Users\JulienFernandez\OneDrive\Coding\_référentiels de code\Hostinger\`
- Basic Auth Guide: `docs/guides/infrastructure/basic-auth.md`
- Deploy Script: `scripts/deploy.bat`

**Credentials Basic Auth:**
- Username: `julien`
- Password: `DevAccess2025`

---

**Dernière mise à jour:** 24 octobre 2025, 14:41 CEST
**Status:** Scraping & Consolidation ✅ | Déploiement ⏳ | Phase 3 Optionnelle ⏳
