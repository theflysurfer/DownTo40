# Données de Référence pour Validation des Ordres de Grandeur

**Date**: 24 octobre 2025
**Sources**: RTE, ENTSO-E, CRE, Montel News

---

## 1. Exports Transfrontaliers France (Q1)

### Données Officielles RTE

| Année | Solde Net Exports | Évolution | Détails par Pays |
|-------|-------------------|-----------|------------------|
| **2022** | **-16.5 TWh** (importateur net) | Première fois depuis 1980 | - Exports: IT (17.9 TWh), CH (13.7 TWh)<br>- Imports: BE+DE (29.3 TWh), ES (12.9 TWh), UK (12.6 TWh) |
| **2023** | **+50.1 TWh** (exportateur net) | +66.6 TWh vs 2022 | - IT (+20 TWh solde), CH (+16.3 TWh), UK (+13.2 TWh)<br>- UK: +23 TWh vs 2022<br>- Core (DE+BE): +30 TWh vs 2022 |
| **2024** | **+89 TWh** (RECORD historique) | +38.9 TWh vs 2023 | - DE+BE: 27.2 TWh<br>- IT: 22.3 TWh<br>- UK: 20.1 TWh<br>- CH: 16.7 TWh<br>- ES: 2.8 TWh |

**Source**: [RTE Bilan Électrique 2024](https://analysesetdonnees.rte-france.com/bilan-electrique-2024/europe)

### Comportement Pendant Prix Négatifs (2024)

**CRE - Note Prix Négatifs (Nov 2024)**:
- **359 heures** à prix négatifs en 2024 (vs 147h en 2023)
- France **exportatrice 83-85% du temps** même pendant prix négatifs
- Volume exports réduit de moitié pendant prix négatifs (-4 GW en moyenne)
- **Imports depuis DE+BE** pendant 71% des heures à prix négatifs
- France "exporte" ses prix négatifs vers voisins ~15% du temps
- France "importe" prix négatifs depuis DE+BE ~40% du temps

**Pertes économiques**: 80 M€ pour producteurs français non soutenus en 2024

**Source**: [CRE Analyse Prix Négatifs](https://www.cre.fr/fileadmin/Documents/Rapports_et_etudes/2024/241126_Note_Prix_negatifs.pdf)

### Allemagne (Perspective Voisin)

- **2024**: 29 TWh imports nets (6% de la consommation)
- **2023**: 11 TWh imports nets
- **Doublement imports** en 1 an, grâce à production française bas-carbone abondante

---

## 2. Production Nucléaire & Capacité Disponible (Q2)

### Données Officielles RTE

| Année | Production Nucléaire | Capacité Installée | Disponibilité | % Mix Électrique |
|-------|---------------------|-------------------|---------------|------------------|
| **2022** | ~280 TWh (estimé) | ~61 GW | ~55-60% | ~63% |
| **2023** | **320.4 TWh** | ~61 GW | ~60-65% | ~66% |
| **2024** | **361.7 TWh** | ~61 GW | **71.5%** | **65%** |

**Observations**:
- **2024**: Plus haute production depuis fermeture Fessenheim (2020)
- **+13% vs 2023** (+41.3 TWh)
- **+29% vs 2022** (+81.7 TWh estimé)
- Récupération après crises corrosion sous contrainte 2022

**Capacité non utilisée 2024**:
```
Capacité théorique max: 61 GW × 8760h = 534.4 TWh
Production réelle: 361.7 TWh
Gap théorique: 172.7 TWh (32.3%)
```

**MAIS**:
- Maintenance planifiée obligatoire
- Taux de disponibilité 71.5% = **capacité effective 381.9 TWh**
- **Sous-utilisation réelle**: ~20.2 TWh (5.3%)

**Source**: [RTE Bilan Production 2024](https://analysesetdonnees.rte-france.com/bilan-electrique-2024/production)

### Corrélation Nucléaire ↔ Prix Bas

**Hypothèse métier à valider**:
- Périodes de sur-disponibilité nucléaire → surplus production → prix bas
- Besoin de croiser production nucléaire horaire vs prix spot
- **Sprint 2 Phase 2**: Scraper production par type (incluant nucléaire)

---

## 3. Écrêtage Renouvelables (Q3)

### Données Officielles RTE & Montel News

| Année | Écrêtage Total | Éolien | Solaire | % Production Renouvelable |
|-------|---------------|--------|---------|---------------------------|
| **2023** | **~0.6 TWh** (estimé) | ~0.3 TWh | ~0.3 TWh | ~0.8% |
| **2024** | **1.7 TWh** | **0.9 TWh** | **0.8 TWh** | **~2.4%** |

**Évolution**: ×2.8 en 1 an (presque **triplement**)

**Contexte Production 2024**:
- Éolien: ~50 TWh (37.5 GW installés onshore + 1.5 GW offshore)
- Solaire: 23.3 TWh (20.8 GW installés)
- **Total Renouvelable**: ~70 TWh
- **Écrêtage**: 1.7 / 70 = **2.4%**

**Heures à prix négatifs 2024**:
- S1 2024: 235 heures (5.4% du temps)
- Total 2024: 359 heures (4% du temps)

**Corrélation**:
- Prix négatifs ≈ surproduction renouvelable (surtout DE+NL) + basse demande
- France "subit" écrêtage même si ses voisins sont source

**Source**:
- [Montel News - French Curtailment Record](https://montelnews.com/news/93be1c1e-dbe8-4d7a-a4c8-a9c789d1e8e3/french-renewables-curtailment-hits-record-1-7-twh-in-2024)
- [RTE Bilan Production 2024](https://analysesetdonnees.rte-france.com/bilan-electrique-2024/production)

---

## 4. Ordres de Grandeur à Valider avec Nos Données

### Question 1: Exports pendant heures ≤40€

**Hypothèses à tester**:
- Si 89 TWh exports sur année 2024
- Et ~3,000 heures à prix ≤40€ (35% du temps)
- **Estimation grossière**: 89 × 0.35 = **~31 TWh exportés à ≤40€** ?

**MAIS**:
- CRE dit exports **réduits de moitié** pendant prix négatifs
- Besoin de croiser prix spot + physical flows horaire
- **Sprint 1 en cours**: Scraping Physical Flows 2022-2024

**Fourchette attendue**: 20-40 TWh/an à ≤40€

---

### Question 2: Nucléaire non produit pendant ≤40€

**Hypothèses à tester**:
- Capacité disponible 2024: 71.5% × 61 GW = 43.6 GW
- Production moyenne: 361.7 TWh / 8760h = 41.3 GW
- **Gap moyen**: ~2.3 GW (sous-utilisation ~5%)

**Pendant heures ≤40€** (3,000h en 2024):
- Si sous-utilisation similaire: 2.3 GW × 3,000h = **~7 TWh**
- Si sous-utilisation accrue (dispatch prioritaire renouvelables): jusqu'à **10-15 TWh**

**À valider avec données Sprint 2**

---

### Question 3: Écrêtage pendant heures ≤40€

**Données confirmées 2024**:
- Total écrêtage: **1.7 TWh**
- Prix négatifs: 359h (4% du temps)
- Prix ≤40€: ~3,000h (35% du temps)

**Hypothèses**:
- La majorité de l'écrêtage se produit pendant prix négatifs
- **Fourchette**: 1.5-1.7 TWh écrêtés pendant prix ≤40€
- Écrêtage = indicateur indirect (pas données directes RTE/ENTSO-E)

---

## 5. Récapitulatif des Volumes Annuels Attendus

| Question | Volume Attendu (TWh/an) | Confiance | Source Validation |
|----------|------------------------|-----------|-------------------|
| **Exports ≤40€** | 20-40 TWh | Moyenne | Physical Flows (scraping Sprint 1) + Prix spot |
| **Nucléaire non produit** | 7-15 TWh | Faible | Production par type (Sprint 2) + Capacité |
| **Écrêtage renouvelables** | 1.5-1.7 TWh | Haute | Montel News, RTE (confirmé 2024) |

**Total MWh "disponibles" à ≤40€**: **30-55 TWh/an** (2024)

---

## 6. Valorisation Potentielle Révisée

### Scénario Conservateur (10% accessibles)

```
Volume accessible: 35 TWh × 10% = 3,500 GWh = 3.5 TWh
Prix spot moyen ≤40€: 25€/MWh
Prix garanti client: 40€/MWh
Marge: 15€/MWh

Valorisation: 3.5 TWh × 15€/MWh = 52.5 M€/an
```

### Scénario Optimiste (20% accessibles)

```
Volume accessible: 35 TWh × 20% = 7 TWh
Marge: 15€/MWh

Valorisation: 7 TWh × 15€/MWh = 105 M€/an
```

**ROI Phase 2**: Si investissement total = 50k€ → **ROI < 1 semaine** (!!)

---

## 7. Limitations et Biais

### Données manquantes:
- **Écrêtage réel horaire**: Pas de transparence RTE/ENTSO-E
- **Raisons sous-utilisation nucléaire**: Maintenance vs dispatch économique
- **Flux transit**: Physical Flows incluent transit (pas seulement FR exports directs)

### Hypothèses fortes:
- Prix négatifs ≈ écrêtage (simplification)
- Sous-utilisation nucléaire uniforme (en réalité variable)
- Exports valorisables à 40€ (dépend contrats long-terme)

---

## 8. Prochaines Étapes

- [x] Scraping Physical Flows 2024 (Sprint 1 - en cours, 25.7% complété)
- [ ] Scraping Physical Flows 2023, 2022
- [ ] Consolidation CSV flows
- [ ] **Analyse croisée**: Flows × Prix spot → Exports pendant ≤40€
- [ ] Scraping Production par type (Sprint 2)
- [ ] **Analyse croisée**: Production nucléaire × Prix spot → Gap pendant ≤40€

---

**Document vivant** - À mettre à jour avec résultats scraping Phase 2
