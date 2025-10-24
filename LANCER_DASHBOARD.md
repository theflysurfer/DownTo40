# 🚀 Lancer le Dashboard Interactif

## Installation des dépendances

```bash
pip install streamlit plotly
```

## Lancement du dashboard

```bash
streamlit run dashboard_app.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à l'adresse : **http://localhost:8501**

---

## 📊 Fonctionnalités du Dashboard

### 1. Vue d'ensemble
- Total énergie disponible (TWh)
- Valorisation à 40€/MWh
- Métriques clés par catégorie

### 2. Visualisations interactives
- **Pie chart** : Répartition par catégorie
- **Bar charts** : Énergie par catégorie et par pays
- **Séries temporelles** : Production mensuelle par type

### 3. Exports par pays
- Graphique des exports pendant périodes prix bas
- Table détaillée avec MWh, GWh, heures

### 4. Production électrique
- Évolution mensuelle du mix énergétique
- Nucléaire, éolien, solaire, hydraulique, gaz

### 5. Statistiques
- Mix énergétique moyen
- Échanges commerciaux moyens par pays

---

## 🌐 Déploiement en ligne (Streamlit Cloud)

### Étape 1 : Préparer le projet

1. Créer un repository GitHub
2. Pusher le code (avec les données dans `results/` et `data/`)

### Étape 2 : Déployer

1. Aller sur https://streamlit.io/cloud
2. Se connecter avec GitHub
3. Cliquer **"New app"**
4. Sélectionner votre repository
5. Main file: `dashboard_app.py`
6. Cliquer **"Deploy"**

**URL publique** générée automatiquement !
Exemple : `https://votre-app.streamlit.app`

---

## 🎨 Personnalisation

### Modifier les couleurs

Dans `dashboard_app.py`, ligne 64 :
```python
color_discrete_sequence=px.colors.qualitative.Set3
```

Palettes disponibles :
- `Set1`, `Set2`, `Set3`
- `Pastel`, `Dark2`
- `Plotly`, `Safe`

### Ajouter des filtres

Exemple : Filtre par année
```python
year = st.selectbox("Année", [2022, 2023, 2024])
odre_filtered = odre_df[odre_df['date_heure'].dt.year == year]
```

### Ajouter une page

```python
# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Vue d'ensemble", "Analyse détaillée", "Export"])

if page == "Vue d'ensemble":
    # Code vue d'ensemble
elif page == "Analyse détaillée":
    # Code analyse
```

---

## 🔧 Dépannage

### Erreur "Données non trouvées"

Lancez d'abord l'analyse :
```bash
python scripts/9_analyze_with_odre_rte.py
```

### Port 8501 déjà utilisé

Changez le port :
```bash
streamlit run dashboard_app.py --server.port 8502
```

### Performances lentes

Réduisez la période ou agrégez les données :
```python
# Agréger par jour au lieu de 15 min
daily = odre_df.resample('D', on='date_heure').mean()
```

---

## 📱 Options avancées

### Mode sombre

```bash
streamlit run dashboard_app.py --theme.base dark
```

### Configuration

Créer `.streamlit/config.toml` :
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"

[server]
port = 8501
headless = true
```

---

## 🚀 Alternatives de déploiement

### 1. Heroku
- Gratuit
- `heroku create`
- `git push heroku main`

### 2. Google Cloud Run
- Scalable
- Pay-as-you-go

### 3. AWS EC2
- Contrôle total
- Plus technique

### 4. Streamlit Cloud (Recommandé)
- ✅ Gratuit
- ✅ Simple
- ✅ Intégration GitHub
- ✅ HTTPS automatique

---

**Besoin d'aide ?** Consultez : https://docs.streamlit.io/
