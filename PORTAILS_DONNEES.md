# 🌐 Portails de Données Énergétiques - Guide Complet

## 📊 Résumé des Portails

| Portail | Inscription | Token API | Téléchargement Direct CSV | Gratuit |
|---------|-------------|-----------|---------------------------|---------|
| **ODRE** | ❌ Non | ❌ Non | ✅ Oui | ✅ Oui |
| **data.gouv.fr** | ❌ Non | ❌ Non | ✅ Oui | ✅ Oui |
| **ENTSO-E** | ✅ Oui | ✅ Oui | ❌ Non | ✅ Oui |
| **RTE Data Portal** | ✅ Oui | ✅ Oui | ❌ Non | ✅ Oui |

---

## 1️⃣ ODRE (Open Data Réseaux Énergies)

### 🔗 URLs du Portail

**Portail principal** : https://opendata.reseaux-energies.fr/

**Interface de données** : https://odre.opendatasoft.com/

**Exploration datasets** : https://odre.opendatasoft.com/explore/

### 📥 Téléchargement Direct (SANS API)

#### Méthode 1 : Via l'interface web

1. Aller sur https://odre.opendatasoft.com/explore/
2. Rechercher "eco2mix national"
3. Cliquer sur le dataset
4. Bouton **"Export"** en haut à droite
5. Choisir format **CSV**
6. Téléchargement immédiat

#### Méthode 2 : URLs directes de téléchargement

**Données nationales éCO2mix 2022** :
```
https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-cons-def/exports/csv?where=date_heure%20%3E%3D%20%272022-01-01%27%20and%20date_heure%20%3C%20%272023-01-01%27&limit=-1&timezone=UTC
```

**Données nationales éCO2mix 2023** :
```
https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-cons-def/exports/csv?where=date_heure%20%3E%3D%20%272023-01-01%27%20and%20date_heure%20%3C%20%272024-01-01%27&limit=-1&timezone=UTC
```

**Données nationales éCO2mix 2024** :
```
https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-cons-def/exports/csv?where=date_heure%20%3E%3D%20%272024-01-01%27%20and%20date_heure%20%3C%20%272025-01-01%27&limit=-1&timezone=UTC
```

### 📋 Datasets Disponibles

**éCO2mix National Consolidé** :
- ID: `eco2mix-national-cons-def`
- URL: https://odre.opendatasoft.com/explore/dataset/eco2mix-national-cons-def/
- Contenu : Production, consommation, échanges (données 15 min)
- Période : 2012 → aujourd'hui

**éCO2mix Régional** :
- ID: `eco2mix-regional-cons-def`
- URL: https://odre.opendatasoft.com/explore/dataset/eco2mix-regional-cons-def/
- Contenu : Données par région

**Parc de production par filière** :
- ID: `parc-prod-par-filiere`
- URL: https://odre.opendatasoft.com/explore/dataset/parc-prod-par-filiere/
- Contenu : Capacité installée par type

### ✅ Avantages

- ✅ **AUCUNE inscription** nécessaire
- ✅ **AUCUN token** requis
- ✅ Téléchargement **immédiat**
- ✅ Export CSV, JSON, Excel, etc.
- ✅ **Pas de limite** de téléchargement

### 📝 Script Fourni

➡️ Utilisez : `scripts/1_fetch_odre_direct.py`

---

## 2️⃣ data.gouv.fr (Plateforme Nationale)

### 🔗 URL du Portail

**Portail principal** : https://www.data.gouv.fr/

**Recherche énergie** : https://www.data.gouv.fr/fr/search/?q=%C3%A9lectricit%C3%A9

### 📥 Datasets Principaux

#### Dataset RTE : Électricité (consommation, production, CO2, échanges)

**URL** : https://www.data.gouv.fr/fr/datasets/electricite-consommation-production-co2-et-echanges/

**Contenu** :
- Consommation en MW
- Production par filière
- Émissions CO2 associées
- Échanges commerciaux aux frontières

**Granularité** : Demi-horaire (30 min)

**Période** : Historique complet + temps réel

**Format** : CSV téléchargeable directement

#### Téléchargement Direct

1. Aller sur la page du dataset
2. Section **"Fichiers"**
3. Cliquer sur le fichier CSV souhaité
4. Téléchargement immédiat

**Exemple de fichiers disponibles** :
- `2022-eco2mix-national.csv`
- `2023-eco2mix-national.csv`
- `2024-eco2mix-national.csv`

### 🔍 Autres Datasets Utiles

**Registre national des installations de production** :
- URL: https://www.data.gouv.fr/fr/datasets/registre-national-des-installations-de-production-et-de-stockage-delectricite-au-31-12-2024/
- Contenu : Liste complète des centrales (nom, type, capacité, localisation)

**Consommation par commune** :
- URL: https://www.data.gouv.fr/fr/datasets/consommation-annuelle-delectricite-et-gaz-par-commune/
- Contenu : Consommation annuelle par commune

### ✅ Avantages

- ✅ **AUCUNE inscription** nécessaire
- ✅ Plateforme **gouvernementale officielle**
- ✅ Données **validées et certifiées**
- ✅ Téléchargement **direct**
- ✅ Historiques complets

---

## 3️⃣ ENTSO-E Transparency Platform

### 🔗 URLs du Portail

**Portail principal** : https://transparency.entsoe.eu/

**Inscription** : https://transparency.entsoe.eu/usrm/user/createPublicUser

**Documentation API** : https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html

### 🔑 Inscription et Obtention du Token

#### Étape 1 : Créer un compte (2 minutes)

1. Aller sur : https://transparency.entsoe.eu/
2. Cliquer sur **"Login"** (coin supérieur droit)
3. Cliquer sur **"Register"**
4. Remplir le formulaire :
   - Email (professionnel ou personnel)
   - Nom, prénom
   - Organisation (optionnel)
   - Pays
5. Valider l'inscription via email reçu

#### Étape 2 : Demander l'accès API (5 minutes)

**Email à envoyer** :

```
À : transparency@entsoe.eu
Sujet : Restful API access

Bonjour,

Je souhaite obtenir un accès à l'API Restful de la plateforme ENTSO-E Transparency.

Email d'inscription : [votre_email@exemple.com]

Merci,
Cordialement
```

#### Étape 3 : Attente (3 jours ouvrés)

ENTSO-E Helpdesk répond sous 3 jours ouvrés pour accorder l'accès.

#### Étape 4 : Générer le token (1 minute)

1. Se connecter sur https://transparency.entsoe.eu/
2. Aller dans **"Account Settings"**
3. Section **"Web API Security Token"**
4. Cliquer sur **"Generate a new token"**
5. **Copier le token** (format : `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

#### Étape 5 : Configurer le projet

```bash
# Dans le fichier .env
ENTSOE_API_TOKEN=12345678-1234-1234-1234-123456789abc
```

### 📊 Données Disponibles via API

- ✅ Prix day-ahead par pays
- ✅ Flux physiques transfrontaliers
- ✅ Production par type d'énergie
- ✅ Consommation réalisée
- ✅ Capacité installée
- ✅ Disponibilité des centrales
- ✅ Écrêtage des renouvelables (partiel)

### ⚠️ Limites

- **400 requêtes/minute** maximum
- Token nécessaire (pas de téléchargement direct)

### 📝 Script Fourni

➡️ Utilisez : `scripts/2_fetch_entsoe.py`

---

## 4️⃣ RTE Data Portal (Digital Services)

### 🔗 URLs du Portail

**Portail principal** : https://data.rte-france.com/

**Inscription** : https://data.rte-france.com/web/guest/profile

**Catalogue API** : https://data.rte-france.com/catalog

### 🔑 Inscription et Obtention des Credentials

#### Étape 1 : Créer un compte (2 minutes)

1. Aller sur : https://data.rte-france.com/
2. Cliquer sur **"Sign in"** (coin supérieur droit)
3. Cliquer sur **"Create an account"**
4. Remplir le formulaire :
   - Email
   - Mot de passe
   - Nom, prénom
   - Organisation
   - Accepter CGU
5. Valider l'inscription via email

#### Étape 2 : Créer une application (3 minutes)

1. Se connecter
2. Aller dans **"My applications"** (menu en haut)
3. Cliquer sur **"Create a new application"**
4. Remplir :
   - Nom : "Analyse Energie 40EUR"
   - Description : "Analyse énergie disponible à prix bas"
5. Cliquer sur **"Create"**

#### Étape 3 : Souscrire aux APIs (2 minutes)

1. Dans votre application, cliquer sur **"Subscribe to APIs"**
2. Rechercher : **"Wholesale Market v2.0"**
3. Cliquer sur **"Subscribe"**
4. Validation **automatique et immédiate**

#### Étape 4 : Récupérer les credentials (1 minute)

1. Retourner dans **"My applications"**
2. Cliquer sur votre application
3. Section **"Credentials"** :
   - **Client ID** : Copier (commence par des lettres/chiffres)
   - **Client Secret** : Cliquer sur "Show" puis copier
4. **IMPORTANT** : Garder le Client Secret confidentiel

#### Étape 5 : Configurer le projet

```bash
# Dans le fichier .env
RTE_CLIENT_ID=abc123def456
RTE_CLIENT_SECRET=votre_secret_ici
```

### 📊 APIs Disponibles

**Wholesale Market** (Prix EPEX SPOT) :
- Prix day-ahead horaires France
- Prix intraday
- Volumes échangés

**Actual Generation** (Production réalisée) :
- Production par filière en temps réel
- Historiques

**Physical Flows** (Flux physiques) :
- Échanges aux interconnexions
- Programmes commerciaux

### ⚠️ Limites

- Token OAuth2 valide **2 heures**
- Renouvellement automatique dans les scripts
- Quotas généreux (pas de souci pour usage normal)

### 📝 Script Fourni

➡️ Utilisez : `scripts/3_fetch_rte_prices.py`

---

## 5️⃣ Autres Portails Utiles

### CRE (Commission de Régulation de l'Énergie)

**URL** : https://www.cre.fr/

**Données** :
- Rapports annuels
- Statistiques marché
- Données d'écrêtage (rapports PDF)

**Téléchargement** : Documents PDF/Excel sur les pages de rapports

### Bilan Électrique RTE

**URL** : https://bilan-electrique.rte-france.com/

**Contenu** :
- Bilan annuel complet
- Analyses détaillées
- Chiffres clés

**Format** : Rapports interactifs + PDF téléchargeables

---

## 📋 Tableau Récapitulatif des Données

| Donnée | ODRE | data.gouv.fr | ENTSO-E | RTE |
|--------|------|--------------|---------|-----|
| **Production par type** | ✅ | ✅ | ✅ | ✅ |
| **Consommation** | ✅ | ✅ | ✅ | ✅ |
| **Échanges frontaliers** | ✅ | ✅ | ✅ | ✅ |
| **Prix day-ahead** | ❌ | ❌ | ✅ | ✅ |
| **Flux physiques détaillés** | ❌ | ❌ | ✅ | ✅ |
| **Écrêtage direct** | ❌ | ❌ | ⚠️ Partiel | ❌ |
| **Téléchargement direct** | ✅ | ✅ | ❌ | ❌ |
| **API** | ⚠️ Optionnel | ❌ | ✅ | ✅ |
| **Inscription** | ❌ | ❌ | ✅ | ✅ |

---

## 🚀 Stratégie de Téléchargement Recommandée

### Option 1 : SANS inscription (Démarrage immédiat)

**Sources** : ODRE + data.gouv.fr uniquement

**Avantages** :
- ✅ Démarrage **immédiat**
- ✅ Aucune inscription
- ✅ Téléchargement direct CSV

**Limitations** :
- ❌ Pas de prix horaires détaillés
- ❌ Pas de flux physiques par pays
- ⚠️ Analyses partielles possibles

**Scripts à utiliser** :
```bash
python scripts/1_fetch_odre_direct.py  # Données ODRE
# Télécharger manuellement depuis data.gouv.fr si besoin
```

### Option 2 : AVEC inscriptions (Analyse complète)

**Sources** : ODRE + data.gouv.fr + ENTSO-E + RTE

**Avantages** :
- ✅ **Analyse complète**
- ✅ Prix horaires précis
- ✅ Flux par pays détaillés
- ✅ Toutes les 4 questions répondues

**Délai** :
- RTE : ✅ Immédiat
- ENTSO-E : ⏳ 3 jours

**Scripts à utiliser** :
```bash
python run_all.py  # Tout automatique
```

---

## 🎯 Actions Immédiates Recommandées

### Aujourd'hui (10 minutes) :

1. **Téléchargement direct ODRE/data.gouv.fr**
   ```bash
   python scripts/1_fetch_odre_direct.py
   ```

2. **Inscriptions APIs** (pour analyses futures)
   - ✅ RTE : https://data.rte-france.com/ (immédiat)
   - ✅ ENTSO-E : https://transparency.entsoe.eu/ + email

### Dans 3 jours :

3. **Token ENTSO-E reçu**
   - Configurer `.env`
   - Lancer analyse complète : `python run_all.py`

---

## 📞 Support des Portails

| Portail | Email Support | Documentation |
|---------|---------------|---------------|
| **ODRE** | - | https://odre.opendatasoft.com/ |
| **data.gouv.fr** | support@data.gouv.fr | https://doc.data.gouv.fr/ |
| **ENTSO-E** | transparency@entsoe.eu | https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html |
| **RTE** | rte-opendata@rte-france.com | https://data.rte-france.com/catalog |

---

## ✅ Checklist d'Inscription

- [ ] ODRE : Aucune inscription nécessaire ✅
- [ ] data.gouv.fr : Aucune inscription nécessaire ✅
- [ ] ENTSO-E :
  - [ ] Créer compte
  - [ ] Envoyer email à transparency@entsoe.eu
  - [ ] Attendre réponse (3 jours)
  - [ ] Générer token
  - [ ] Copier dans .env
- [ ] RTE :
  - [ ] Créer compte
  - [ ] Créer application
  - [ ] Souscrire "Wholesale Market"
  - [ ] Copier Client ID et Secret dans .env

---

**Dernière mise à jour** : 2025-10-23
