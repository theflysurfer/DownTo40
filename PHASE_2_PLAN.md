# 📋 Phase 2 - Plan d'Action Métier

## 🎯 Objectif Phase 2

**Répondre complètement aux 3 questions du dirigeant avec des volumes réels en MWh:**

> **"J'ai besoin de MWh à 40€/MWh. Combien de MWh ont été:**
> 1. ✈️ **Vendus aux pays frontaliers** à ≤40€ ?
> 2. ⚛️ **Non produits par le nucléaire** (contraintes réseau, priorité dispatch) ?
> 3. 🌞 **Écrêtés** (solaire, éolien) à cause de prix négatifs ?"

---

## 📊 Ce qu'on a déjà (Phase 1)

### ✅ Données Prix Day-Ahead
- **26,254 heures** de prix scrapées (2022-2024)
- **4,201 heures** à prix ≤40€/MWh identifiées
- **503 heures** à prix négatifs
- **Dashboard** avec analyse temporelle complète

### ❌ Ce qu'il manque pour répondre complètement

| Question | Données manquantes | Source ENTSO-E |
|----------|-------------------|----------------|
| **Exports ≤40€** | Flux transfrontaliers réels (MW) | Physical Flows |
| **Nucléaire non produit** | Production nucléaire vs capacité | Generation by Type |
| **Écrêtage renouvelables** | Production éolien/solaire vs prévisions | Generation by Type + Forecasts |

---

## 🗺️ Roadmap Phase 2

### Sprint 1: Scraping Flux Transfrontaliers (2-3 jours)

**Objectif**: Quantifier les exports réels pendant les heures ≤40€

#### Tâches techniques:
- [ ] Adapter script Playwright pour scraper "Physical Flows"
- [ ] Cibler pays frontaliers: Allemagne, Belgique, Espagne, Italie, Suisse, UK
- [ ] Format: Date/Heure + Pays + Export(MW) + Import(MW)
- [ ] Période: 2022-2024 (même que prix)
- [ ] Consolider en CSV

#### Dataset attendu:
```csv
timestamp,country,export_mw,import_mw,net_export_mw
2024-04-05 12:00:00,DE,2500,800,1700
2024-04-05 12:00:00,ES,1200,0,1200
...
```

#### Analyses métier résultantes:
- **Volume exporté** pendant heures ≤40€ par pays
- **Valorisation potentielle**: MWh × (prix voisin - 40€)
- **Top pays** acheteurs d'énergie bon marché française

**Script**: `scripts/20_scrape_physical_flows.js` (à créer)

---

### Sprint 2: Scraping Production par Type (2-3 jours)

**Objectif**: Identifier sous-utilisation nucléaire et écrêtage renouvelables

#### Tâches techniques:
- [ ] Scraper "Actual Generation per Production Type"
- [ ] Types ciblés: Nuclear, Solar, Wind Onshore, Wind Offshore, Hydro
- [ ] Format: Date/Heure + Type + Production(MW)
- [ ] Période: 2022-2024
- [ ] Consolider en CSV

#### Dataset attendu:
```csv
timestamp,generation_type,production_mw
2024-04-05 12:00:00,Nuclear,45000
2024-04-05 12:00:00,Solar,8500
2024-04-05 12:00:00,Wind Onshore,5200
...
```

#### Données complémentaires nécessaires:
- **Capacité installée** nucléaire: ~61 GW (données publiques RTE)
- **Prévisions J-1** renouvelables (optionnel mais utile)

#### Analyses métier résultantes:

**1. Nucléaire non produit:**
```python
capacite_nucleaire = 61000  # MW
production_reelle = df['production_mw'][df['type']=='Nuclear']
non_produit = capacite_nucleaire - production_reelle

# Pendant heures ≤40€
nucl_non_produit_40eur = non_produit[prix <= 40].sum()
```

**2. Écrêtage renouvelables:**
```python
# Hypothèse: Prix négatifs = écrêtage
# Comparer production vs pic historique
prod_solar_negatif = df[prix < 0]['Solar'].sum()
prod_wind_negatif = df[prix < 0]['Wind'].sum()

curtailment_estimate = prod_solar_negatif + prod_wind_negatif
```

**Script**: `scripts/21_scrape_generation_by_type.js` (adapter depuis 15)

---

### Sprint 3: Enrichissement Dashboard (3-4 jours)

**Objectif**: Intégrer nouvelles données et répondre aux 3 questions

#### Nouvelles pages dashboard:

**1. Page "Exports Transfrontaliers"**
- Carte interactive des flux vers pays voisins
- Volume total exporté pendant heures ≤40€ (en MWh)
- Top 3 pays acheteurs
- Timeline exports vs prix
- **Réponse Q1**: "X MWh exportés à ≤40€ vers pays Y pendant période Z"

**2. Page "Production & Capacité"**
- Graphique nucléaire: capacité vs production réelle
- Identification heures de sous-utilisation
- Corrélation: sous-utilisation nucléaire ↔ prix ≤40€
- **Réponse Q2**: "Y MWh non produits par nucléaire (Z% capacité) pendant heures ≤40€"

**3. Page "Renouvelables & Écrêtage"**
- Production solaire/éolien vs prix
- Estimation écrêtement (prix négatifs)
- Timeline surproduction renouvelable
- **Réponse Q3**: "W MWh écrêtés (estimés) pendant prix négatifs"

**4. Page "Synthèse Business"**
- **RÉPONSE COMPLÈTE** aux 3 questions
- Volumes totaux en MWh
- Valorisation potentielle
- Recommandations stratégiques

#### Tâches techniques:
- [ ] Charger 3 CSVs: prix + flows + generation
- [ ] Merger sur timestamp
- [ ] Créer 4 nouvelles pages Streamlit
- [ ] Visualisations: cartes (folium/plotly), timelines, barres empilées
- [ ] Calculs métier: volumes, valorisations, corrélations

**Fichier**: Enrichir `dashboard_entso_prices.py`

---

### Sprint 4: Validation & Documentation (1-2 jours)

**Objectif**: Vérifier cohérence des données et documenter méthodologie

#### Tâches:
- [ ] **Validation croisée**: Comparer volumes exports ENTSO-E vs ODRE
- [ ] **Cohérence temporelle**: Vérifier timestamps alignés
- [ ] **Sens business**: Valider ordres de grandeur avec experts énergie
- [ ] **Documentation méthodologie**: Expliquer calculs et hypothèses
- [ ] **Rapport exécutif**: Synthèse 2-pages pour décideurs

**Livrables**:
- [ ] `VALIDATION_REPORT.md`
- [ ] `EXECUTIVE_SUMMARY.md`
- [ ] Dashboard Phase 2 déployé

---

## 📈 Résultats Attendus Phase 2

### Indicateurs métier quantifiés:

| Question | Indicateur | Exemple Valeur |
|----------|-----------|----------------|
| **Exports ≤40€** | MWh totaux exportés | ~500 GWh/an |
| | Principaux pays | DE (60%), ES (20%), IT (15%) |
| | Valorisation potentielle | ~20-30 M€/an |
| **Nucléaire non produit** | MWh capacité inutilisée | ~200 GWh/an |
| | % temps sous-capacité | ~15% heures |
| | Corrélation prix bas | 80% pendant ≤40€ |
| **Écrêtage renouvelables** | MWh écrêtés (estimé) | ~50-100 GWh/an |
| | % production renouvelable | 2-5% |
| | Heures prix négatifs | 503h (aligné Phase 1) |

### Dashboard final:

```
🎯 Problématique (Phase 1)
📊 Vue d'ensemble (Phase 1)
📈 Analyse détaillée (Phase 1)
💰 Prix ≤40€/MWh (Phase 1)
✈️ Exports transfrontaliers (Phase 2) ← NOUVEAU
⚛️ Production & Capacité (Phase 2) ← NOUVEAU
🌞 Renouvelables & Écrêtage (Phase 2) ← NOUVEAU
📋 Synthèse Business (Phase 2) ← NOUVEAU
🔬 Méthodologie
```

---

## 🎯 Livrables Finaux Phase 2

### Pour le Business:
1. **Dashboard interactif** avec réponses aux 3 questions
2. **Rapport exécutif** (2 pages) avec chiffres clés
3. **Présentation** (slides) pour comité direction

### Pour la Tech:
1. **Scripts de scraping** (flows + generation)
2. **Données consolidées** (3 CSVs + merged)
3. **Documentation** méthodologie et validation
4. **Tests** et procédures de mise à jour

---

## ⏱️ Planning Prévisionnel

| Sprint | Durée | Début | Fin |
|--------|-------|-------|-----|
| Sprint 1: Scraping Flows | 2-3j | J+1 | J+3 |
| Sprint 2: Scraping Generation | 2-3j | J+4 | J+6 |
| Sprint 3: Dashboard enrichi | 3-4j | J+7 | J+10 |
| Sprint 4: Validation & Docs | 1-2j | J+11 | J+12 |

**Total Phase 2**: 8-12 jours ouvrés (2-3 semaines)

---

## 🚀 Prochaines Étapes Immédiates

### À faire maintenant:

1. **Valider le plan** avec les parties prenantes
2. **Prioriser les questions** (si besoin de commencer par 1 ou 2)
3. **Créer les scripts de scraping** (Sprint 1)

### Commandes pour démarrer Sprint 1:

```bash
# Créer le script de scraping flows
cd scripts
cp 14_scrape_any_year.js 20_scrape_physical_flows.js

# Adapter pour scraper Physical Flows au lieu de Day-Ahead Prices
# Cibler: Transmission > Physical Flows > France
```

---

## 📊 KPIs de Succès Phase 2

- [ ] **Complétude données**: ≥99% heures couvertes (comme Phase 1)
- [ ] **Cohérence**: Écart <5% avec sources alternatives (ODRE)
- [ ] **Performance**: Dashboard charge <3s
- [ ] **Adoption**: ≥10 utilisations/semaine par décideurs
- [ ] **Impact business**: ≥1 décision stratégique basée sur insights

---

## 💡 Hypothèses & Limitations

### Hypothèses:
- Prix négatifs = proxy pour écrêtage (simplification)
- Capacité nucléaire constante 61 GW (varie en réalité avec maintenance)
- Exports pendant prix bas = opportunité perdue (hypothèse business)

### Limitations:
- **Écrêtage réel** non disponible directement (calcul indirect)
- **Raisons sous-utilisation nucléaire** multiples (pas seulement prix)
- **Flux transfrontaliers** incluent transit (pas seulement exports nets)

### Données non disponibles:
- Volumes réels d'écrêtage par producteur
- Contraintes réseau détaillées (confidentielles RTE)
- Prix contracts long-terme (vs spot)

**⚠️ Important**: Présenter résultats comme "ordres de grandeur" et "tendances", pas vérités absolues.

---

## 📞 Support & Questions

Pour lancer la Phase 2:
1. Confirmer le go/no-go
2. Prioriser les 3 questions (ou toutes en parallèle)
3. Allouer ressources (temps développement + validation métier)

**Prêt à démarrer Sprint 1?** 🚀
