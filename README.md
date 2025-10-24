# Analyse Énergie Non Utilisée France (2022-2024)

## Objectif
Quantifier l'énergie disponible à ≤40€/MWh non utilisée en France :
1. Exports vers pays frontaliers à ≤40€/MWh
2. Nucléaire non produit (contraintes réseau)
3. Écrêtage solaire/éolien
4. Périodes à prix négatifs

## Sources de données

### 1. ODRE (Open Data Réseaux Énergies) - GRATUIT ✅
- **URL**: https://odre.opendatasoft.com
- **Token**: ❌ Non nécessaire
- **Téléchargement direct CSV**: ✅ Oui
- **Données**: Production, consommation, échanges transfrontaliers (2012-2024)
- **Avantage**: Démarrage immédiat sans inscription

### 2. ENTSO-E Transparency Platform - GRATUIT
- **URL**: https://transparency.entsoe.eu
- **Token**: Nécessaire (inscription + email à transparency@entsoe.eu)
- **Données**: Flux physiques transfrontaliers, prix day-ahead, écrêtage
- **Documentation**: https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html

### 3. RTE Data Portal (Wholesale Market) - GRATUIT
- **URL**: https://data.rte-france.com
- **Token**: OAuth2 nécessaire (inscription gratuite)
- **Données**: Prix EPEX SPOT France
- **Token validité**: 2 heures (renouvelable)

## Structure du projet

```
.
├── README.md
├── requirements.txt
├── .env.example              # Template pour vos tokens API
├── config/
│   └── api_config.py         # Configuration centralisée
├── data/                     # Données téléchargées (gitignored)
│   ├── raw/                  # Données brutes
│   └── processed/            # Données traitées
├── scripts/
│   ├── 1_fetch_odre.py       # Extraction ODRE
│   ├── 2_fetch_entsoe.py     # Extraction ENTSO-E
│   ├── 3_fetch_rte_prices.py # Extraction prix RTE
│   ├── 4_analyze_exports.py  # Analyse exports ≤40€
│   ├── 5_analyze_curtailment.py  # Analyse écrêtage
│   ├── 6_analyze_nuclear.py  # Analyse nucléaire non produit
│   ├── 7_analyze_negative_prices.py  # Analyse prix négatifs
│   └── 8_consolidate.py      # Rapport final consolidé
└── results/                  # Résultats d'analyse
    └── rapport_final.csv
```

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

1. Copier `.env.example` vers `.env`
2. Remplir vos tokens API :
   - **ENTSO-E**: Inscription sur https://transparency.entsoe.eu + email
   - **RTE**: Inscription sur https://data.rte-france.com
3. Vérifier la configuration :
   ```bash
   python check_config.py
   ```

## Utilisation

### Option 1 : Exécution automatique (recommandé)

```bash
python run_all.py
```

### Option 2 : Exécution manuelle

Exécuter les scripts dans l'ordre :

```bash
# 1. Télécharger données ODRE (pas de token requis)
python scripts/1_fetch_odre.py

# 2. Télécharger données ENTSO-E (token requis)
python scripts/2_fetch_entsoe.py

# 3. Télécharger prix RTE (token requis)
python scripts/3_fetch_rte_prices.py

# 4-7. Analyses spécifiques
python scripts/4_analyze_exports.py
python scripts/5_analyze_curtailment.py
python scripts/6_analyze_nuclear.py
python scripts/7_analyze_negative_prices.py

# 8. Rapport consolidé final
python scripts/8_consolidate.py
```

## Période d'analyse

**2022-01-01 à 2024-12-31** (3 années complètes)

## Documentation

- **QUICKSTART.md** : Démarrage en 5 minutes ⚡
- **README.md** (ce fichier) : Vue d'ensemble rapide
- **PORTAILS_DONNEES.md** : 🌐 Guide complet des portails (inscriptions, URLs téléchargement)
- **GUIDE_UTILISATION.md** : Guide détaillé pas-à-pas
- **RESUME_EXECUTIF.md** : Résumé pour dirigeants avec implications stratégiques
- **FAQ.md** : 25 questions/réponses

## Prochaines étapes

1. Lire **GUIDE_UTILISATION.md** pour instructions complètes
2. Obtenir les tokens API (ENTSO-E et RTE)
3. Exécuter `python check_config.py` pour vérifier la configuration
4. Exécuter `python run_all.py` pour lancer l'analyse complète
5. Consulter les résultats dans `results/rapport_final.xlsx`
