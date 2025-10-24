# Guide d'Utilisation Complet

## Vue d'ensemble du projet

Ce projet analyse **l'énergie non utilisée en France sur 2022-2024** disponible à **≤40€/MWh**, en répondant à la question :

> "J'ai besoin de MWh à 40€/MWh, combien de MWh ont été :
> - Vendus aux pays frontaliers à ≤40€ ?
> - Non produits par le nucléaire (contraintes réseau) ?
> - Écrêtés (solaire, éolien) ?
> - Disponibles à prix négatifs ?"

## Étape 1 : Installation

### 1.1 Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### 1.2 Installation des dépendances

```bash
pip install -r requirements.txt
```

Packages installés :
- `requests` : requêtes HTTP vers les APIs
- `pandas` : manipulation des données
- `python-dotenv` : gestion des tokens
- `entsoe-py` : client Python pour ENTSO-E
- `openpyxl` : export Excel
- `matplotlib`, `seaborn` : visualisations (optionnel)

## Étape 2 : Configuration des APIs

### 2.1 ODRE (Open Data Réseaux Énergies) - GRATUIT, SANS TOKEN

**Aucune configuration nécessaire** pour ODRE.

L'API est publique et accessible sans authentification.

### 2.2 ENTSO-E Transparency Platform - GRATUIT avec inscription

**Temps d'obtention : 3 jours ouvrés**

#### Instructions :

1. **S'inscrire** sur https://transparency.entsoe.eu
   - Créer un compte avec email professionnel ou personnel

2. **Demander l'accès API**
   - Envoyer un email à : **transparency@entsoe.eu**
   - Sujet : **"Restful API access"**
   - Corps du message : Indiquer l'email utilisé pour l'inscription

3. **Recevoir l'autorisation** (sous 3 jours)
   - Vous recevrez un email de confirmation

4. **Générer le token**
   - Se connecter sur https://transparency.entsoe.eu
   - Aller dans : **Account Settings** → **Web API Security Token**
   - Cliquer sur **"Generate a new token"**
   - Copier le token (format : `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

5. **Ajouter le token au projet**
   - Copier `.env.example` vers `.env`
   - Remplacer `your_entsoe_token_here` par votre token

```bash
# Dans le fichier .env
ENTSOE_API_TOKEN=12345678-1234-1234-1234-123456789abc
```

### 2.3 RTE Data Portal (OAuth2) - GRATUIT avec inscription

**Temps d'obtention : Immédiat**

#### Instructions :

1. **S'inscrire** sur https://data.rte-france.com
   - Créer un compte

2. **Créer une application**
   - Se connecter
   - Aller dans : **My Applications**
   - Cliquer sur **"Create a new application"**
   - Nom de l'application : "Analyse Energie 40€"
   - Description : "Analyse énergie disponible"

3. **Souscrire aux APIs**
   - Dans votre application, cliquer sur **"Subscribe to APIs"**
   - Souscrire à : **"Wholesale Market v2.0"** (prix EPEX SPOT)
   - Validation automatique

4. **Récupérer les credentials**
   - Dans votre application, vous verrez :
     - **Client ID** (commence par des lettres/chiffres)
     - **Client Secret** (cliquer sur "Show" pour voir)
   - Copier les deux

5. **Ajouter au projet**

```bash
# Dans le fichier .env
RTE_CLIENT_ID=votre_client_id_ici
RTE_CLIENT_SECRET=votre_client_secret_ici
```

### 2.4 Vérifier la configuration

Votre fichier `.env` final doit ressembler à :

```
ENTSOE_API_TOKEN=12345678-1234-1234-1234-123456789abc
RTE_CLIENT_ID=abc123def456
RTE_CLIENT_SECRET=secret_key_here
```

## Étape 3 : Exécution des analyses

### Option A : Exécution automatique complète (recommandé)

```bash
python run_all.py
```

Ce script exécute toutes les étapes automatiquement :
1. Télécharge les données ODRE
2. Télécharge les données ENTSO-E
3. Télécharge les prix RTE
4. Analyse les exports
5. Analyse l'écrêtage
6. Analyse le nucléaire
7. Analyse les prix négatifs
8. Génère le rapport final

**Durée estimée : 30-60 minutes** (selon la quantité de données)

### Option B : Exécution manuelle étape par étape

#### 1. Extraction des données brutes

```bash
# Données ODRE (production, consommation, échanges)
python scripts/1_fetch_odre.py

# Données ENTSO-E (flux transfrontaliers, prix)
python scripts/2_fetch_entsoe.py

# Prix EPEX SPOT via RTE
python scripts/3_fetch_rte_prices.py
```

**Résultats** : Fichiers CSV dans `data/raw/`

#### 2. Analyses spécifiques

```bash
# Exports vers pays frontaliers à ≤40€/MWh
python scripts/4_analyze_exports.py

# Écrêtage des renouvelables
python scripts/5_analyze_curtailment.py

# Nucléaire non produit
python scripts/6_analyze_nuclear.py

# Prix négatifs
python scripts/7_analyze_negative_prices.py
```

**Résultats** : Fichiers CSV dans `data/processed/`

#### 3. Rapport final consolidé

```bash
python scripts/8_consolidate.py
```

**Résultats** :
- `results/rapport_final.csv`
- `results/rapport_final.xlsx` (avec onglets détaillés)
- `results/rapport_final.txt`

## Étape 4 : Interpréter les résultats

### 4.1 Structure du rapport final

Le fichier `results/rapport_final.xlsx` contient plusieurs onglets :

#### Onglet "Synthèse"
| Colonne | Description |
|---------|-------------|
| `categorie` | Type d'énergie non utilisée |
| `mwh` | Total en MégaWatt-heures |
| `gwh` | Total en GigaWatt-heures |
| `heures` | Nombre d'heures concernées |
| `prix_moyen` | Prix moyen pendant ces périodes (€/MWh) |

#### Onglet "Exports"
Détail des exports par pays frontalier :
- Allemagne (DE)
- Belgique (BE)
- Suisse (CH)
- Italie (IT)
- Espagne (ES)
- Grande-Bretagne (GB)

#### Onglet "Écrêtage"
Énergie renouvelable écrêtée par technologie :
- Solaire
- Éolien

#### Onglet "Nucléaire"
Production nucléaire non réalisée (contraintes réseau)

#### Onglet "Prix négatifs"
Statistiques par année sur les périodes de prix négatifs

### 4.2 Exemple d'interprétation

```
TOTAL: 15 000 GWh (15 TWh)

Répartition:
- Exports: 8 000 GWh (53%)
- Écrêtage: 4 000 GWh (27%)
- Nucléaire: 2 500 GWh (17%)
- Prix négatifs: 500 heures identifiées
```

**Interprétation** :
> Sur 2022-2024, **15 TWh d'énergie** auraient pu être disponibles à ≤40€/MWh
> au lieu d'être exportée (8 TWh), écrêtée (4 TWh) ou non produite (2.5 TWh).

**Valorisation potentielle** :
- À 40€/MWh : 15 000 GWh × 40€ = **600 millions €**

## Étape 5 : Limitations et notes méthodologiques

### 5.1 Exports
**Source** : Données réelles ENTSO-E
**Fiabilité** : ⭐⭐⭐⭐⭐ (Très élevée)
**Note** : Flux physiques mesurés, prix day-ahead réels

### 5.2 Écrêtage
**Source** : Estimation basée sur prix négatifs et variations de production
**Fiabilité** : ⭐⭐⭐ (Estimation conservative)
**Note** : Les données d'écrêtage direct ne sont pas toujours disponibles via API.
Valeurs réelles peuvent être supérieures.

Pour données précises : consulter rapports RTE/CRE

### 5.3 Nucléaire non produit
**Source** : Estimation basée sur variations de production
**Fiabilité** : ⭐⭐⭐ (Estimation conservative)
**Note** : Compare production réelle vs capacité normale (P95)

### 5.4 Prix négatifs
**Source** : Données réelles ENTSO-E/RTE
**Fiabilité** : ⭐⭐⭐⭐⭐ (Très élevée)
**Note** : Indicateur de surproduction et d'écrêtage probable

### 5.5 Pas de double-comptage
Les catégories sont exclusives :
- Exports ≠ écrêtage
- Nucléaire non produit ≠ exports
- Prix négatifs = contexte informatif

## Étape 6 : Dépannage

### Problème : "Token ENTSO-E non configuré"

**Solution** :
1. Vérifier que le fichier `.env` existe (pas `.env.example`)
2. Vérifier que le token est bien copié sans espaces
3. Format attendu : `ENTSOE_API_TOKEN=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

### Problème : "Erreur 401 - Token expiré (RTE)"

**Solution** :
Le token OAuth2 RTE expire après 2 heures. Le script le regénère automatiquement.
Si le problème persiste :
1. Vérifier que Client ID et Secret sont corrects
2. Réessayer quelques minutes plus tard

### Problème : "Aucune donnée récupérée"

**Solutions possibles** :
1. Vérifier la connexion internet
2. Vérifier que les dates dans `config/api_config.py` sont valides
3. Certaines données peuvent ne pas être disponibles pour toute la période
4. ENTSO-E : limite de 400 requêtes/minute, attendre si dépassement

### Problème : "Quota API dépassé (ODRE)"

**Solution** :
ODRE limite à 50 000 appels/mois. Si dépassé :
- Attendre le mois prochain
- Ou utiliser les données déjà téléchargées dans `data/raw/`

## Étape 7 : Personnalisation

### Modifier le seuil de prix

Dans `config/api_config.py` :

```python
PRICE_THRESHOLD = 40  # Changer ici (€/MWh)
```

### Modifier la période d'analyse

Dans `config/api_config.py` :

```python
START_DATE = "2023-01-01"  # Date de début
END_DATE = "2023-12-31"    # Date de fin
```

### Ajouter d'autres pays

Dans `config/api_config.py`, ajouter dans `EIC_CODES` :

```python
EIC_CODES = {
    "FR": "10YFR-RTE------C",
    "DE": "10Y1001A1001A83F",
    # Ajouter ici...
}
```

Codes EIC disponibles : https://www.entsoe.eu/data/energy-identification-codes-eic/

## Support et contribution

### Questions ?
Consulter la documentation des APIs :
- ODRE : https://odre.opendatasoft.com
- ENTSO-E : https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html
- RTE : https://data.rte-france.com

### Améliorations futures possibles
1. Ajout de visualisations (graphiques)
2. Analyses mensuelles/saisonnières
3. Corrélation avec météo
4. API automatique de mise à jour
5. Dashboard interactif

---

**Dernière mise à jour** : 2025-10-23
