# ⚡ Quick Start - Démarrage Rapide (5 minutes)

## 🎯 Objectif
Analyser l'énergie disponible à ≤40€/MWh en France (2022-2024)

---

## ⚙️ 1. Installation (2 min)

```bash
pip install -r requirements.txt
```

---

## 🔑 2. Configuration APIs (2 min)

### Créer fichier .env
```bash
copy .env.example .env
```

### Obtenir les tokens

**ENTSO-E** (⏳ 3 jours d'attente)
1. Inscription : https://transparency.entsoe.eu
2. Email à : transparency@entsoe.eu
   - Sujet : "Restful API access"
3. Copier le token reçu dans `.env`

**RTE** (✅ Immédiat)
1. Inscription : https://data.rte-france.com
2. Créer application → Souscrire "Wholesale Market"
3. Copier Client ID + Secret dans `.env`

**ODRE** : ✅ Aucun token nécessaire

---

## ✅ 3. Vérification (1 min)

```bash
python check_config.py
```

**Attendu** : 6/6 ✅

---

## 🚀 4. Exécution (30-60 min automatique)

```bash
python run_all.py
```

---

## 📊 5. Résultats

```bash
start results\rapport_final.xlsx
```

**Onglets** :
- Synthèse : Total MWh à ≤40€/MWh
- Exports : Par pays (DE, BE, CH, IT, ES, GB)
- Écrêtage : Solaire, éolien
- Nucléaire : Contraintes réseau
- Prix négatifs : Statistiques annuelles

---

## 📚 Documentation Complète

- **README.md** : Vue d'ensemble
- **GUIDE_UTILISATION.md** : Guide détaillé
- **RESUME_EXECUTIF.md** : Business case
- **FAQ.md** : 25 questions/réponses
- **COMPTE_RENDU_FINAL.md** : Compte rendu complet

---

## 🆘 Problème ?

```bash
python check_config.py  # Diagnostic
```

Consulter **FAQ.md** ou **GUIDE_UTILISATION.md**

---

## 💡 Résultat Attendu

**≈580 millions €** d'opportunités identifiées sur 3 ans :
- 8 TWh exports (320 M€)
- 4 TWh écrêtage (160 M€)
- 2.5 TWh nucléaire (100 M€)

---

**Coût : 0€** | **APIs gratuites** | **Prêt à l'emploi** ✅
