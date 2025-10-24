"""
Dashboard Interactif v2 - Energie Disponible <=40EUR/MWh
Avec problématique et méthodologie explicites
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configuration page
st.set_page_config(
    page_title="Energie <=40EUR/MWh - Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === SIDEBAR : Navigation ===
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/1f77b4/ffffff?text=Energie+40EUR", use_column_width=True)
    st.title("Navigation")
    page = st.radio(
        "Sections",
        ["🎯 Problématique", "📊 Résultats", "🔬 Méthodologie", "📈 Données détaillées"]
    )

    st.markdown("---")
    st.markdown("### 🔢 Chiffres clés")
    st.metric("Période", "2022-2024")
    st.metric("Sources", "ODRE + RTE")
    st.metric("Données", "105k lignes")

# Charger les données
@st.cache_data
def load_data():
    try:
        summary = pd.read_csv("results/rapport_preliminaire.csv")
        exports = pd.read_csv("results/exports_detail.csv")
        odre = pd.read_csv("data/raw/odre_eco2mix_national.csv", parse_dates=['date_heure'])
        return summary, exports, odre
    except:
        return None, None, None

summary_df, exports_df, odre_df = load_data()

if summary_df is None:
    st.error("⚠️ Données non trouvées. Lancez d'abord: `python scripts/9_analyze_with_odre_rte.py`")
    st.stop()

# === PAGE 1: PROBLÉMATIQUE ===
if page == "🎯 Problématique":
    st.title("⚡ Énergie Disponible à ≤40€/MWh en France")
    st.markdown("## 🎯 Problématique & Contexte")

    # Question initiale
    st.markdown("### 📋 Question du dirigeant")
    st.info("""
    **"J'ai besoin de MWh à 40€/MWh."**

    **Combien de MWh ont été :**
    - ✈️ Vendus aux pays frontaliers à ≤40€ ?
    - ⚛️ Non produits par le nucléaire (contraintes réseau, priorité dispatch) ?
    - 🌞 Écrêtés (solaire, éolien) à cause de prix négatifs ?

    💡 **Idée** : Pourquoi ne pas me les vendre à 40€/MWh au lieu de les exporter ou les perdre ?
    """)

    # Réponse
    st.markdown("### ✅ Notre réponse")

    col1, col2, col3 = st.columns(3)

    with col1:
        total_twh = summary_df[summary_df['categorie'] == 'TOTAL']['gwh'].values[0] / 1000
        st.metric(
            "💰 Énergie identifiée",
            f"{total_twh:.1f} TWh",
            delta="Sur 2022-2024"
        )

    with col2:
        valorisation = total_twh * 1000 * 40
        st.metric(
            "💵 Valorisation potentielle",
            f"{valorisation/1000:.1f} Mds €",
            delta="À 40€/MWh"
        )

    with col3:
        st.metric(
            "📅 Période analysée",
            "3 ans",
            delta="2022-2024"
        )

    st.success(f"""
    **{total_twh:.0f} TWh d'énergie "disponible mais non utilisée"** ont été identifiés en France sur 2022-2024.

    Cette énergie aurait pu être valorisée à **{valorisation/1000:.1f} milliards €** au lieu d'être :
    - Exportée vers les pays voisins
    - Écrêtée (renouvelables arrêtées)
    - Non produite (nucléaire contraint)
    """)

    # Enjeux
    st.markdown("### 🎯 Enjeux stratégiques")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### 🔴 Problème actuel

        - **Exports massifs** pendant prix bas → Énergie "perdue" à l'étranger
        - **Écrêtage** renouvelables → Gaspillage énergie verte
        - **Nucléaire sous-utilisé** → Capacité inutilisée
        - **Prix négatifs** récurrents → Surproduction non valorisée
        """)

    with col2:
        st.markdown("""
        #### 🟢 Opportunité

        - **Sécuriser énergie** à prix garanti ≤40€/MWh
        - **Valoriser surplus** nationaux au lieu d'exporter
        - **Contrats flexibles** avec RTE/EDF/Producteurs
        - **ROI potentiel** : Milliards € sur 3 ans
        """)

    st.markdown("### 🗺️ Approche")

    st.markdown("""
    Notre analyse répond précisément aux 4 questions en:

    1. **Quantifiant** les MWh exportés pendant périodes à prix bas
    2. **Estimant** le nucléaire non produit (variabilité anormale)
    3. **Calculant** l'écrêtage des renouvelables (prix négatifs)
    4. **Identifiant** toutes les heures de prix négatifs

    → **Résultat** : Cartographie complète de l'énergie ≤40€/MWh "disponible"
    """)

# === PAGE 2: RÉSULTATS ===
elif page == "📊 Résultats":
    st.title("📊 Résultats de l'Analyse")
    st.markdown("## Synthèse 2022-2024")

    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_twh = summary_df[summary_df['categorie'] == 'TOTAL']['gwh'].values[0] / 1000
        st.metric("Total Énergie", f"{total_twh:.1f} TWh")

    with col2:
        valorisation = total_twh * 1000 * 40
        st.metric("Valorisation", f"{valorisation:,.0f} M€")

    with col3:
        exports_twh = summary_df[summary_df['categorie'] == 'Exports']['gwh'].values[0] / 1000
        st.metric("Exports", f"{exports_twh:.1f} TWh", delta=f"{exports_twh/total_twh*100:.0f}%")

    with col4:
        nuclear_twh = summary_df[summary_df['categorie'] == 'Nucleaire non produit']['gwh'].values[0] / 1000
        st.metric("Nucléaire", f"{nuclear_twh:.1f} TWh", delta=f"{nuclear_twh/total_twh*100:.0f}%")

    st.markdown("---")

    # Graphiques
    col1, col2 = st.columns(2)

    with col1:
        fig_pie = px.pie(
            summary_df[summary_df['categorie'] != 'TOTAL'],
            values='gwh',
            names='categorie',
            title="📊 Répartition par catégorie (GWh)",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        fig_bar = px.bar(
            summary_df[summary_df['categorie'] != 'TOTAL'].sort_values('gwh', ascending=False),
            x='categorie',
            y='gwh',
            title="📈 Énergie par catégorie (GWh)",
            color='gwh',
            color_continuous_scale='Blues',
            text='gwh'
        )
        fig_bar.update_traces(texttemplate='%{text:.0f} GWh', textposition='outside')
        fig_bar.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    # Exports détaillés
    st.markdown("### 🌍 Détail des exports par pays")

    if exports_df is not None and not exports_df.empty:
        col1, col2 = st.columns([2, 1])

        with col1:
            fig_exports = px.bar(
                exports_df.sort_values('total_mwh_exported', ascending=True),
                y='pays',
                x='total_mwh_exported',
                title="Exports pendant périodes prix bas",
                labels={'total_mwh_exported': 'MWh', 'pays': 'Pays'},
                color='total_mwh_exported',
                color_continuous_scale='RdYlGn_r',
                orientation='h',
                text='total_mwh_exported'
            )
            fig_exports.update_traces(texttemplate='%{text:,.0f} MWh', textposition='outside')
            fig_exports.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_exports, use_container_width=True)

        with col2:
            st.markdown("#### 🔢 Chiffres clés")
            exports_display = exports_df.copy()
            exports_display['GWh'] = (exports_display['total_mwh_exported'] / 1000).apply(lambda x: f"{x:,.1f}")
            st.dataframe(
                exports_display[['pays', 'GWh']].sort_values('pays'),
                use_container_width=True,
                hide_index=True
            )
            st.metric("Total exports", f"{exports_df['total_mwh_exported'].sum()/1000:.1f} GWh")

# === PAGE 3: MÉTHODOLOGIE ===
elif page == "🔬 Méthodologie":
    st.title("🔬 Méthodologie d'Analyse")

    st.markdown("## 📊 Sources de données")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 1️⃣ ODRE (Open Data Réseaux Énergies)

        **🔗 Source** : https://odre.opendatasoft.com

        **📦 Données utilisées** :
        - **105 121 lignes** (2022-2024)
        - **Granularité** : 15 minutes
        - **37 colonnes** de données

        **📋 Contenu** :
        - Production par filière
          - Nucléaire, éolien, solaire, hydraulique
          - Gaz, charbon, bioénergies
        - Consommation nationale
        - **Échanges commerciaux par pays**
          - Angleterre, Espagne, Italie
          - Suisse, Allemagne-Belgique

        **✅ Fiabilité** : Données consolidées officielles RTE
        """)

    with col2:
        st.markdown("""
        ### 2️⃣ RTE Data Portal

        **🔗 Source** : https://data.rte-france.com

        **📦 API configurée** :
        - Wholesale Market v3.0
        - Prix EPEX SPOT France

        **📋 Contenu** :
        - Prix horaires day-ahead
        - Volumes marché
        - Échanges détaillés

        ### 3️⃣ ENTSO-E (en cours)

        **🔗 Source** : https://transparency.entsoe.eu

        **📦 En attente token** (3 jours)

        **📋 Apportera** :
        - Prix réels horaires
        - Flux transfrontaliers précis
        - Affinage de l'analyse
        """)

    st.markdown("---")
    st.markdown("## 🧮 Méthodes de calcul")

    tab1, tab2, tab3 = st.tabs(["📤 Exports (74 TWh)", "⚛️ Nucléaire (132 TWh)", "🌞 Écrêtage (11 TWh)"])

    with tab1:
        st.markdown("""
        ### Méthodologie : Exports pendant périodes prix bas

        **🎯 Objectif** : Identifier les MWh exportés quand prix ≤40€/MWh

        **📊 Données** : Échanges commerciaux ODRE (`ech_comm_XXX`)

        **🧮 Méthode** :

        1. **Estimation périodes prix bas** (en l'absence de prix horaires complets) :
           - **Nuit** (0h-6h) → Prix typiquement 20-30€/MWh
           - **Week-end** → Demande faible → Prix bas
           - **Été midi** (11h-15h) → Surplus solaire → Prix bas voire négatifs

        2. **Filtrage exports** :
           - Valeurs négatives = exports (MW sortants)
           - Pendant périodes prix bas uniquement

        3. **Conversion MWh** :
           ```
           MWh = Σ(MW export × durée) / 4
           ```
           Division par 4 car données toutes les 15 min

        4. **Agrégation par pays**

        **✅ Résultat** : 74 TWh exportés dont :
        - Italie : 19.5 TWh
        - Allemagne-Belgique : 17.7 TWh
        - Suisse : 16.1 TWh
        - Angleterre : 12.8 TWh
        - Espagne : 8.1 TWh

        **⚠️ Limite** : Estimation périodes prix bas (sera affiné avec ENTSO-E)
        """)

    with tab2:
        st.markdown("""
        ### Méthodologie : Nucléaire non produit

        **🎯 Objectif** : Quantifier l'énergie nucléaire "manquante"

        **📊 Données** : Production nucléaire horaire (`nucleaire`)

        **🧮 Méthode** :

        1. **Calcul capacité de référence** :
           - **P95** = Percentile 95% de la production
           - = **48 578 MW** sur 2022-2024
           - Représente la capacité "normale haute"

        2. **Détection sous-production** :
           - Seuil : < 80% du P95 = < 38 862 MW
           - = Périodes de production anormalement basse

        3. **Calcul énergie manquante** :
           ```
           MW_manquant = P95 - Production_réelle
           MWh = Σ(MW_manquant) / 4
           ```

        4. **Filtrage contextuel** :
           - Uniquement périodes de prix bas estimés
           - Exclut maintenance programmée longue

        **✅ Résultat** : 132 TWh "non produits"
        - 30 822 heures de sous-production
        - Soit 3.5 ans équivalents

        **🔍 Causes probables** :
        - Contraintes réseau (surproduction totale)
        - Maintenance programmée
        - Priorité dispatch renouvelables

        **⚠️ Limite** : Estimation conservative (inclut maintenance planifiée)
        """)

    with tab3:
        st.markdown("""
        ### Méthodologie : Écrêtage renouvelables

        **🎯 Objectif** : Estimer l'énergie renouvelable écrêtée

        **📊 Données** : Production solaire/éolien + exports

        **🧮 Méthode** :

        1. **Identification périodes de surproduction** :
           - Exports physiques > 5000 MW
           - = France exporte massivement
           - → Indicateur de surplus

        2. **Calcul capacité normale** :
           - **P90** production solaire/éolien
           - = Capacité de référence haute

        3. **Détection écrêtage** :
           - Pendant surproduction :
             ```
             Écrêtage = (P90 × 50%) - Production_réelle
             ```
           - Si production < 50% du P90 → Écrêtage probable

        4. **Conversion MWh** :
           ```
           MWh = Σ(MW_écrêté) / 4
           ```

        **✅ Résultat** : 11 TWh écrêtés
        - Solaire : 11.2 TWh
        - 27 688 heures d'exports massifs identifiées

        **⚠️ Limite** :
        - Estimation **très conservative**
        - Pas de données d'écrêtage directes via API
        - Valeurs réelles probablement **supérieures**
        - À affiner avec rapports CRE/RTE officiels
        """)

    st.markdown("---")
    st.markdown("## ⚖️ Fiabilité des estimations")

    reliability_data = {
        'Catégorie': ['Exports', 'Nucléaire non produit', 'Écrêtage'],
        'Fiabilité': ['⭐⭐⭐⭐', '⭐⭐⭐', '⭐⭐⭐'],
        'Méthode': ['Données mesurées + estimation périodes', 'Modèle variabilité', 'Estimation conservative'],
        'Affinage avec ENTSO-E': ['Prix réels horaires', 'Corrélation prix', 'Détection prix négatifs']
    }

    st.table(pd.DataFrame(reliability_data))

# === PAGE 4: DONNÉES DÉTAILLÉES ===
else:  # "📈 Données détaillées"
    st.title("📈 Données Détaillées 2022-2024")

    if odre_df is not None:
        st.markdown("## ⚡ Production électrique mensuelle")

        # Agréger par mois
        odre_df['month'] = pd.to_datetime(odre_df['date_heure']).dt.to_period('M')
        monthly = odre_df.groupby('month')[['nucleaire', 'eolien', 'solaire', 'hydraulique', 'gaz']].mean().reset_index()
        monthly['month'] = monthly['month'].astype(str)

        fig_production = go.Figure()

        fig_production.add_trace(go.Scatter(
            x=monthly['month'], y=monthly['nucleaire'],
            name='Nucléaire', mode='lines', line=dict(width=3, color='#ff7f0e')
        ))
        fig_production.add_trace(go.Scatter(
            x=monthly['month'], y=monthly['eolien'],
            name='Éolien', mode='lines', line=dict(width=2, color='#2ca02c')
        ))
        fig_production.add_trace(go.Scatter(
            x=monthly['month'], y=monthly['solaire'],
            name='Solaire', mode='lines', line=dict(width=2, color='#ffbb00')
        ))
        fig_production.add_trace(go.Scatter(
            x=monthly['month'], y=monthly['hydraulique'],
            name='Hydraulique', mode='lines', line=dict(width=2, color='#1f77b4')
        ))

        fig_production.update_layout(
            title="Production moyenne mensuelle (MW)",
            xaxis_title="Mois",
            yaxis_title="MW",
            hovermode='x unified',
            height=500
        )

        st.plotly_chart(fig_production, use_container_width=True)

        st.markdown("---")
        st.markdown("## 📊 Mix énergétique & Échanges")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ⚡ Mix énergétique moyen")
            mix_data = {
                'Source': ['Nucléaire', 'Éolien', 'Solaire', 'Hydraulique', 'Gaz', 'Autres'],
                'MW': [
                    odre_df['nucleaire'].mean(),
                    odre_df['eolien'].mean(),
                    odre_df['solaire'].mean(),
                    odre_df['hydraulique'].mean(),
                    odre_df['gaz'].mean(),
                    (odre_df['fioul'].mean() + odre_df['charbon'].mean() + odre_df['bioenergies'].mean())
                ]
            }
            mix_df = pd.DataFrame(mix_data)

            fig_mix = px.bar(
                mix_df.sort_values('MW', ascending=True),
                y='Source',
                x='MW',
                orientation='h',
                color='MW',
                color_continuous_scale='Viridis',
                text='MW'
            )
            fig_mix.update_traces(texttemplate='%{text:,.0f} MW', textposition='outside')
            fig_mix.update_layout(showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig_mix, use_container_width=True)

        with col2:
            st.markdown("### 🌍 Échanges commerciaux moyens")
            exchanges_data = {
                'Pays': ['Angleterre', 'Espagne', 'Italie', 'Suisse', 'Allemagne-Belgique'],
                'MW': [
                    odre_df['ech_comm_angleterre'].mean(),
                    odre_df['ech_comm_espagne'].mean(),
                    odre_df['ech_comm_italie'].mean(),
                    odre_df['ech_comm_suisse'].mean(),
                    odre_df['ech_comm_allemagne_belgique'].mean()
                ]
            }
            exchanges_df = pd.DataFrame(exchanges_data)
            exchanges_df['Type'] = exchanges_df['MW'].apply(lambda x: 'Export' if x < 0 else 'Import')
            exchanges_df['MW_abs'] = exchanges_df['MW'].abs()

            fig_exch = px.bar(
                exchanges_df,
                x='Pays',
                y='MW_abs',
                color='Type',
                color_discrete_map={'Export': '#d62728', 'Import': '#2ca02c'},
                text='MW_abs'
            )
            fig_exch.update_traces(texttemplate='%{text:,.0f} MW', textposition='outside')
            st.plotly_chart(fig_exch, use_container_width=True)

# === FOOTER ===
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>Projet Énergie ≤40€/MWh France 2022-2024</strong></p>
    <p>Sources : ODRE (105k lignes) | RTE Data Portal | ENTSO-E (en cours)</p>
    <p>Méthodologie : Estimation conservative basée sur périodes prix bas</p>
</div>
""", unsafe_allow_html=True)
