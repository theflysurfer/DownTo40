# FAQ - Questions Fréquentes

## 🎯 Questions Générales

### Q1 : Quel est l'objectif de ce projet ?

**R** : Quantifier l'énergie disponible en France à ≤40€/MWh qui a été :
- Exportée vers les pays voisins
- Écrêtée (renouvelables)
- Non produite (nucléaire, contraintes réseau)
- Disponible à prix négatifs

**But** : Identifier les opportunités d'achat d'énergie à bas prix.

---

### Q2 : Combien coûte ce projet ?

**R** : **0€**

- Toutes les APIs sont gratuites
- Open source complet
- Pas de frais cachés

---

### Q3 : Combien de temps faut-il pour obtenir les résultats ?

**R** :
- **Obtention des tokens** : 3 jours (ENTSO-E) + immédiat (RTE)
- **Exécution des scripts** : 30-60 minutes
- **Total** : ~1 semaine (incluant attente tokens)

---

### Q4 : Quelles sont les données analysées ?

**R** : Données réelles historiques 2022-2024 :
- Production électrique France (par type)
- Consommation nationale
- Échanges transfrontaliers (flux physiques)
- Prix de marché day-ahead (EPEX SPOT)

Sources officielles : ODRE, ENTSO-E, RTE

---

## 🔧 Questions Techniques

### Q5 : J'ai une erreur "Token ENTSO-E non configuré", que faire ?

**R** : 3 étapes :

1. **Créer le fichier .env**
   ```bash
   copy .env.example .env
   ```

2. **Obtenir le token ENTSO-E**
   - Inscription : https://transparency.entsoe.eu
   - Email à : transparency@entsoe.eu
   - Sujet : "Restful API access"

3. **Ajouter dans .env**
   ```
   ENTSOE_API_TOKEN=votre-token-ici
   ```

---

### Q6 : Erreur "401 Unauthorized" sur RTE, pourquoi ?

**R** : Vérifier vos credentials RTE :

1. **Connexion** : https://data.rte-france.com
2. **My Applications** → Votre app
3. **Vérifier** :
   - Client ID (copier exactement)
   - Client Secret (cliquer "Show" puis copier)
4. **Mettre à jour .env** sans espaces

---

### Q7 : "ModuleNotFoundError: No module named 'entsoe'", que faire ?

**R** : Installer les dépendances :

```bash
pip install -r requirements.txt
```

Si erreur persiste :
```bash
pip install entsoe-py
```

---

### Q8 : Combien de données le script télécharge-t-il ?

**R** : Pour 3 ans (2022-2024) :
- **ODRE** : ~26 000 lignes (données 15 min)
- **ENTSO-E** : ~26 000 prix + ~156 000 flux (6 pays)
- **RTE** : ~26 000 prix

**Volume total** : ~50-100 MB de CSV

**Temps** : 30-60 minutes selon connexion

---

### Q9 : Puis-je analyser une autre période ?

**R** : Oui ! Dans `config/api_config.py` :

```python
START_DATE = "2023-01-01"  # Changer ici
END_DATE = "2023-12-31"    # Changer ici
```

**Disponibilité** :
- ODRE : 2012 → aujourd'hui
- ENTSO-E : 2015 → aujourd'hui
- RTE : 2019 → aujourd'hui

---

### Q10 : Puis-je changer le seuil de 40€/MWh ?

**R** : Oui ! Dans `config/api_config.py` :

```python
PRICE_THRESHOLD = 30  # Par exemple 30€/MWh
```

Tous les scripts s'adapteront automatiquement.

---

## 📊 Questions sur les Résultats

### Q11 : Où trouver les résultats finaux ?

**R** : Dossier `results/` :

- **rapport_final.xlsx** : Rapport complet avec onglets
- **rapport_final.csv** : Données brutes
- **rapport_final.txt** : Résumé texte

---

### Q12 : Que signifie "écrêtage estimé" ?

**R** : Les données d'écrêtage direct ne sont pas toujours disponibles via API.

**Méthode d'estimation** :
1. Identifier les périodes de prix négatifs/très bas
2. Comparer production renouvelable vs capacité normale
3. Calculer la différence = écrêtage estimé

**Fiabilité** : Conservative (valeurs minimales)

Pour données précises : Consulter rapports annuels RTE/CRE

---

### Q13 : Comment interpréter "nucléaire non produit" ?

**R** : Le nucléaire peut réduire sa production pour :
- **Contraintes réseau** : Surproduction totale
- **Maintenance** : Arrêts programmés
- **Priorité dispatch** : Renouvelables prioritaires

Le script identifie les **baisses anormales** de production pendant **prix bas** = contraintes réseau probables

---

### Q14 : Y a-t-il du double-comptage entre catégories ?

**R** : **Non**, les catégories sont exclusives :

- **Exports** : Énergie physiquement exportée (mesurée)
- **Écrêtage** : Production renouvelable arrêtée (non exportée)
- **Nucléaire** : Production réduite (non exportée, non écrêtée)

**Somme** = Total réel disponible

---

### Q15 : Que faire des prix négatifs ?

**R** : Les prix négatifs **ne sont pas une catégorie d'énergie** mais un **contexte** :

- **Interprétation** : Surproduction systémique
- **Indique** : Écrêtage probable, contraintes réseau
- **Opportunité** : Moments d'achat à coût négatif

**Nombre d'heures** à prix négatif = indicateur de tensions réseau

---

## 💼 Questions Stratégiques

### Q16 : Comment utiliser ces résultats commercialement ?

**R** : 3 opportunités principales :

1. **Exports (8 TWh)** → Négocier accès prioritaire avec RTE
2. **Écrêtage (4 TWh)** → Contrats directs avec producteurs renouvelables (PPA)
3. **Nucléaire (2.5 TWh)** → Accords avec EDF pour production contrainte

**Voir** : RESUME_EXECUTIF.md pour détails stratégiques

---

### Q17 : Est-ce légal d'acheter l'énergie écrêtée ?

**R** : **Oui**, plusieurs mécanismes légaux :

1. **PPA (Power Purchase Agreement)** : Contrat direct producteur-consommateur
2. **Contrats d'effacement inversé** : Rémunération pour consommation pendant surplus
3. **Marchés infra-journaliers** : Achat sur marchés spot

**Recommandation** : Consulter CRE (Commission de Régulation de l'Énergie)

---

### Q18 : Peut-on automatiser cette analyse ?

**R** : **Oui**, possibilités :

1. **Mise à jour mensuelle** : Cron job + scripts
2. **Alertes temps réel** : Monitoring API + notifications
3. **Dashboard** : Streamlit/Dash pour visualisation
4. **Intégration BI** : CSV vers Power BI / Tableau

**Coût développement** : 2-3 semaines ingénieur

---

### Q19 : Quelle est la fiabilité des estimations ?

**R** : Par catégorie :

| Catégorie | Fiabilité | Source |
|-----------|-----------|--------|
| Exports | ⭐⭐⭐⭐⭐ | Mesures réelles ENTSO-E |
| Prix négatifs | ⭐⭐⭐⭐⭐ | Données réelles marché |
| Écrêtage | ⭐⭐⭐ | Estimation conservative |
| Nucléaire | ⭐⭐⭐ | Estimation modèle |

**Total** : Ordre de grandeur fiable, détails à affiner

---

### Q20 : Quels sont les risques / limitations ?

**R** : 3 principaux :

1. **Accès réseau** : Nécessite autorisation RTE
   - Solution : Négociation institutionnelle

2. **Capacité de consommation** : Pouvoir absorber les volumes
   - Solution : Stockage ou consommation flexible

3. **Régulation** : Conformité CRE
   - Solution : Validation juridique préalable

**Recommandation** : Pilot test sur 1 catégorie d'abord

---

## 🔄 Questions Maintenance

### Q21 : Comment mettre à jour les données ?

**R** : 2 options :

**Option 1** : Tout relancer
```bash
python run_all.py
```

**Option 2** : Mettre à jour seulement les données récentes
```python
# Dans config/api_config.py
START_DATE = "2024-12-01"  # Dernier mois
END_DATE = "2024-12-31"
```

---

### Q22 : Que faire si une API est en panne ?

**R** : Résolution par priorité :

1. **ODRE en panne** : Utiliser ENTSO-E pour production
2. **ENTSO-E en panne** : Utiliser ODRE + RTE (flux incomplets)
3. **RTE en panne** : Utiliser ENTSO-E pour prix

Scripts conçus pour gérer les erreurs individuelles.

---

### Q23 : Y a-t-il des limites API à respecter ?

**R** : Oui :

| API | Limite | Gestion |
|-----|--------|---------|
| ODRE | 50 000 appels/mois | Script optimisé (batch 100) |
| ENTSO-E | 400 requêtes/minute | Pas de problème (script lent) |
| RTE | Token 2h | Renouvellement automatique |

**Conseil** : Ne pas lancer le script en boucle

---

## 📞 Support

### Q24 : Où trouver de l'aide ?

**R** : 3 ressources :

1. **Documentation projet**
   - GUIDE_UTILISATION.md (guide complet)
   - RESUME_EXECUTIF.md (implications stratégiques)

2. **Documentation APIs**
   - ODRE : https://odre.opendatasoft.com
   - ENTSO-E : https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html
   - RTE : https://data.rte-france.com

3. **Vérification config**
   ```bash
   python check_config.py
   ```

---

### Q25 : Puis-je contribuer au projet ?

**R** : Oui ! Améliorations bienvenues :

**Idées** :
- Visualisations (graphiques, cartes)
- Analyses saisonnières
- Prédictions ML
- Dashboard interactif
- Tests unitaires

**Méthode** : Fork + Pull Request

---

**Dernière mise à jour** : 2025-10-23
