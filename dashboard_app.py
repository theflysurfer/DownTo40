"""
Dashboard Interactif - Energie Disponible <=40EUR/MWh
Visualisation des analyses avec Streamlit
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
    layout="wide"
)

# Titre
st.title("⚡ Analyse Energie Disponible à <=40€/MWh")
st.markdown("**Période**: 2022-2024 | **Sources**: ODRE, RTE")

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
    st.error("Données non trouvées. Lancez d'abord: python scripts/9_analyze_with_odre_rte.py")
    st.stop()

# === SECTION 1: VUE D'ENSEMBLE ===
st.header("📊 Vue d'ensemble")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_twh = summary_df[summary_df['categorie'] == 'TOTAL']['gwh'].values[0] / 1000
    st.metric("Total Énergie", f"{total_twh:.1f} TWh")

with col2:
    valorisation = total_twh * 1000 * 40  # GWh * 40EUR
    st.metric("Valorisation (40€/MWh)", f"{valorisation:,.0f} M€")

with col3:
    exports_twh = summary_df[summary_df['categorie'] == 'Exports']['gwh'].values[0] / 1000
    st.metric("Exports", f"{exports_twh:.1f} TWh")

with col4:
    nuclear_twh = summary_df[summary_df['categorie'] == 'Nucleaire non produit']['gwh'].values[0] / 1000
    st.metric("Nucléaire non produit", f"{nuclear_twh:.1f} TWh")

# === SECTION 2: GRAPHIQUES ===
st.header("📈 Répartition de l'énergie")

col1, col2 = st.columns(2)

with col1:
    # Pie chart
    fig_pie = px.pie(
        summary_df[summary_df['categorie'] != 'TOTAL'],
        values='gwh',
        names='categorie',
        title="Répartition par catégorie (GWh)",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Bar chart
    fig_bar = px.bar(
        summary_df[summary_df['categorie'] != 'TOTAL'],
        x='categorie',
        y='gwh',
        title="Énergie par catégorie (GWh)",
        color='categorie',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

# === SECTION 3: EXPORTS PAR PAYS ===
st.header("🌍 Exports par pays")

if exports_df is not None and not exports_df.empty:
    col1, col2 = st.columns(2)

    with col1:
        fig_exports = px.bar(
            exports_df.sort_values('total_mwh_exported', ascending=False),
            x='pays',
            y='total_mwh_exported',
            title="Exports pendant périodes prix bas (MWh)",
            labels={'total_mwh_exported': 'MWh', 'pays': 'Pays'},
            color='pays',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_exports, use_container_width=True)

    with col2:
        # Table détails
        st.subheader("Détails par pays")
        exports_display = exports_df.copy()
        exports_display['MWh'] = exports_display['total_mwh_exported'].apply(lambda x: f"{x:,.0f}")
        exports_display['GWh'] = (exports_display['total_mwh_exported'] / 1000).apply(lambda x: f"{x:,.1f}")
        exports_display['Heures'] = exports_display['heures'].apply(lambda x: f"{x:,}")
        st.dataframe(
            exports_display[['pays', 'MWh', 'GWh', 'Heures']],
            use_container_width=True,
            hide_index=True
        )

# === SECTION 4: PRODUCTION PAR TYPE ===
st.header("⚡ Production électrique 2022-2024")

if odre_df is not None:
    # Agréger par mois
    odre_df['month'] = pd.to_datetime(odre_df['date_heure']).dt.to_period('M')
    monthly = odre_df.groupby('month')[['nucleaire', 'eolien', 'solaire', 'hydraulique', 'gaz']].mean().reset_index()
    monthly['month'] = monthly['month'].astype(str)

    fig_production = go.Figure()

    fig_production.add_trace(go.Scatter(
        x=monthly['month'], y=monthly['nucleaire'],
        name='Nucléaire', mode='lines', line=dict(width=2)
    ))
    fig_production.add_trace(go.Scatter(
        x=monthly['month'], y=monthly['eolien'],
        name='Éolien', mode='lines', line=dict(width=2)
    ))
    fig_production.add_trace(go.Scatter(
        x=monthly['month'], y=monthly['solaire'],
        name='Solaire', mode='lines', line=dict(width=2)
    ))
    fig_production.add_trace(go.Scatter(
        x=monthly['month'], y=monthly['hydraulique'],
        name='Hydraulique', mode='lines', line=dict(width=2)
    ))

    fig_production.update_layout(
        title="Production moyenne mensuelle (MW)",
        xaxis_title="Mois",
        yaxis_title="MW",
        hovermode='x unified'
    )

    st.plotly_chart(fig_production, use_container_width=True)

# === SECTION 5: STATISTIQUES ===
st.header("📋 Statistiques détaillées")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Mix énergétique moyen")
    if odre_df is not None:
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
        st.dataframe(
            mix_df.style.format({'MW': '{:,.0f}'}),
            use_container_width=True,
            hide_index=True
        )

with col2:
    st.subheader("Échanges commerciaux moyens")
    if odre_df is not None:
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
        exchanges_df['MW'] = exchanges_df['MW'].abs()
        st.dataframe(
            exchanges_df.style.format({'MW': '{:,.0f}'}),
            use_container_width=True,
            hide_index=True
        )

# === FOOTER ===
st.markdown("---")
st.markdown("""
**Notes méthodologiques:**
- Analyse préliminaire basée sur estimations de périodes à prix bas (nuit, week-end, été)
- Données ODRE 2022-2024 (105k lignes)
- Valorisation calculée à 40€/MWh
- Pour analyse complète avec prix horaires réels: obtenir token ENTSO-E

**Sources:**
- ODRE (Open Data Réseaux Énergies)
- RTE (Réseau de Transport d'Électricité)
""")
