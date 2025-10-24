# ENTSO-E Transparency Platform - Sources de Données Disponibles

## Données Actuellement Récupérées

### 1. Energy Prices - Day-Ahead Market
**Status**: ✅ En cours de scraping (2024, puis 2023, 2022)
- **Source**: Market > Energy Prices
- **Données**: Prix horaires EUR/MWh pour la France (BZN|FR)
- **Format**: 24h par jour, prix Day-Ahead
- **Utilité**: Identifier les heures à ≤40€/MWh pour optimisation énergétique

## Autres Données Intéressantes Disponibles

### 2. Load - Actual Total Load
**Catégorie**: Load
- **Description**: Consommation électrique réelle totale de la France
- **Données**: MW par période (15min ou 1h)
- **Utilité**: Comprendre la demande réelle vs prix bas
- **Corrélation potentielle**: Prix bas = surproduction vs demande

### 3. Generation - Actual Generation per Production Type
**Catégorie**: Generation
- **Description**: Production réelle par type de source
  - Nuclear
  - Wind Onshore
  - Wind Offshore
  - Solar
  - Hydro
  - Gas
  - Coal
  - Biomass
  - Other
- **Utilité**: Identifier les sources de surproduction (éolien/solaire) pendant prix bas
- **Insight clé**: Corrélation prix bas avec pics de renouvelables

### 4. Generation - Wind and Solar Forecast
**Catégorie**: Generation
- **Description**: Prévisions de production éolienne et solaire
- **Données**: Prévisions J-1 et intraday
- **Utilité**: Anticiper les périodes de prix bas liées aux renouvelables

### 5. Transmission - Cross-Border Physical Flow
**Catégorie**: Transmission
- **Description**: Flux physiques d'électricité aux frontières
- **Pays voisins**: Allemagne, Belgique, Espagne, Italie, Suisse, UK
- **Utilité**: Comprendre import/export pendant prix bas
- **Insight**: France exporte-t-elle l'excédent quand prix ≤40€?

### 6. Balancing - Imbalance Prices
**Catégorie**: Balancing
- **Description**: Prix d'équilibrage en temps réel
- **Utilité**: Identifier opportunités arbitrage
- **Comparaison**: Prix Day-Ahead vs Prix Balancing

### 7. Load - Day-Ahead Forecast
**Catégorie**: Load
- **Description**: Prévisions de consommation J-1
- **Utilité**: Comprendre si prix bas = erreur de prévision de demande

### 8. Congestion Management - Redispatching
**Catégorie**: Operations
- **Description**: Actions de redispatching (réduction/augmentation production)
- **Utilité**: Identifier contraintes réseau pendant surproduction

## Priorités de Scraping

### Phase 1: Prix (EN COURS)
✅ 2024 Energy Prices Day-Ahead
⏳ 2023 Energy Prices Day-Ahead
⏳ 2022 Energy Prices Day-Ahead

### Phase 2: Production (RECOMMANDÉ)
- Actual Generation per Production Type (2022-2024)
- Focus: Wind + Solar pour corréler avec prix bas

### Phase 3: Consommation
- Actual Total Load (2022-2024)
- Comprendre demande vs surproduction

### Phase 4: Flux Transfrontaliers
- Cross-Border Physical Flow (principaux voisins)
- Identifier export d'excédent

### Phase 5: Prévisions (Optionnel)
- Wind and Solar Forecast
- Day-Ahead Load Forecast

## Analyses Possibles avec ces Données

### 1. Corrélation Prix-Production Renouvelable
**Question**: Les prix ≤40€ sont-ils liés aux pics éolien/solaire?
**Données**: Energy Prices + Generation by Type

### 2. Pattern Saisonnier
**Question**: Quels mois ont le plus d'heures ≤40€?
**Découverte actuelle**: Mars-Mai 2024 = période d'or!
**Données**: Energy Prices (déjà en cours)

### 3. Profil Horaire
**Question**: Quelles heures de la journée ont les prix les plus bas?
**Hypothèse**: Nuit (surproduction éolienne) + midi (pic solaire)
**Données**: Energy Prices (déjà en cours)

### 4. Opportunités d'Export
**Question**: La France exporte-t-elle quand prix ≤40€?
**Utilité commerciale**: Revendre l'excédent aux voisins
**Données**: Energy Prices + Cross-Border Flow

### 5. Capacité de Stockage Nécessaire
**Question**: Quelle capacité de stockage pour capter toute l'énergie ≤40€?
**Données**: Energy Prices + Total Load
**Calcul**: (Load moyenne pendant heures ≤40€) × (nombre d'heures)

## Implémentation Technique

### Scraping Priority
1. ✅ Energy Prices: Script existant `14_scrape_any_year.js`
2. 🔜 Generation by Type: Nouveau script à créer
3. 🔜 Total Load: Nouveau script à créer
4. 🔜 Cross-Border Flow: Nouveau script à créer

### Format de Stockage Recommandé
- **JSONL** pour chaque type de données
- **CSV consolidé** pour analyses
- **Base de données** (SQLite/PostgreSQL) pour dashboard interactif

## Sources de Documentation
- ENTSO-E Transparency Platform: https://transparency.entsoe.eu
- API Documentation: https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html
- RESTful API: Requiert token (déjà demandé)
