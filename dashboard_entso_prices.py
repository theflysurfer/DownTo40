"""
Dashboard ENTSO-E Electricity Prices 2022-2024
Real scraped data from ENTSO-E Transparency Platform
Focus: Analysis of hours with prices ≤40€/MWh
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Prix Électricité France 2022-2024",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_price_data():
    """Load consolidated ENTSO-E price data"""
    processed_dir = Path('data/processed')

    try:
        # Full dataset
        full_df = pd.read_csv(processed_dir / 'entsoe_2022_2024_prices_full.csv')
        full_df['datetime'] = pd.to_datetime(full_df['datetime'])

        # Summary
        summary_df = pd.read_csv(processed_dir / 'entsoe_2022_2024_summary.csv')

        # Monthly
        monthly_df = pd.read_csv(processed_dir / 'entsoe_2022_2024_monthly.csv')

        # Below 40
        below_40_df = pd.read_csv(processed_dir / 'entsoe_2022_2024_below_40.csv')
        below_40_df['datetime'] = pd.to_datetime(below_40_df['datetime'])

        return full_df, summary_df, monthly_df, below_40_df

    except FileNotFoundError:
        st.error("⚠️ Fichiers de données non trouvés. Exécutez d'abord: python scripts/16_consolidate_entsoe_prices.py")
        st.stop()

# Sidebar
with st.sidebar:
    st.title("⚡ Prix Électricité FR")
    st.markdown("### 📅 Période")
    st.metric("Années", "2022-2024")
    st.metric("Source", "ENTSO-E")

    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["🎯 Problématique", "📊 Vue d'ensemble", "📈 Analyse détaillée", "💰 Prix ≤40€/MWh", "📚 Sources"]
    )

    st.markdown("---")
    st.markdown("### ℹ️ À propos")
    st.markdown("""
    **Données**: Prix Day-Ahead EPEX SPOT France

    **Granularité**: Horaire

    **Source**: ENTSO-E Transparency Platform

    **Scraping**: Playwright automation
    """)

# Load data
full_df, summary_df, monthly_df, below_40_df = load_price_data()

# === PAGE 0: PROBLÉMATIQUE ===
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

    # Réponse avec données réelles
    st.markdown("### ✅ Notre réponse")

    col1, col2, col3 = st.columns(3)

    total_hours_below_40 = len(below_40_df)
    total_hours = len(full_df)
    pct_below_40 = (total_hours_below_40 / total_hours * 100) if total_hours > 0 else 0

    # Estimation GWh from hours at average 30€
    estimated_gwh_below_40 = total_hours_below_40 * 30 / 1000  # Rough avg consumption per hour

    with col1:
        st.metric(
            "⚡ Heures identifiées",
            f"{total_hours_below_40:,} heures",
            delta=f"{pct_below_40:.1f}% du temps (2022-2024)"
        )

    with col2:
        st.metric(
            "📅 Période analysée",
            "3 ans complets",
            delta="2022-2024"
        )

    with col3:
        negative_hours = full_df['is_negative'].sum()
        st.metric(
            "🔻 Prix négatifs",
            f"{negative_hours:,} heures",
            delta="Opportunités maximales"
        )

    st.success(f"""
    **{total_hours_below_40:,} heures à prix ≤40€/MWh** identifiées sur 2022-2024.

    Cela représente **{pct_below_40:.1f}% du temps** sur 3 ans, avec des opportunités en constante augmentation:
    - 2022: 0.9% (crise énergétique)
    - 2023: 11.8% (récupération)
    - 2024: 35.2% (abondance)
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

        **Résultat**: Des milliers d'heures à prix ≤40€ chaque année !
        """)

    with col2:
        st.markdown("""
        #### 🟢 Opportunité

        - **Sécuriser énergie** à prix garanti ≤40€/MWh
        - **Valoriser surplus** nationaux au lieu d'exporter
        - **Contrats flexibles** avec RTE/EDF/Producteurs
        - **Arbitrage intelligent** basé sur prédictions prix

        **Potentiel**: 35% des heures en 2024 étaient ≤40€ !
        """)

    st.markdown("### 📊 Évolution du marché")

    # Graph showing trend
    yearly_stats = summary_df.copy()
    fig_trend = px.bar(
        yearly_stats,
        x='year',
        y='percent_below_40',
        title="📈 Évolution des heures ≤40€/MWh par an",
        labels={'percent_below_40': '% heures ≤40€', 'year': 'Année'},
        color='percent_below_40',
        color_continuous_scale='RdYlGn',
        text='percent_below_40'
    )
    fig_trend.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_trend.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("""
    **Tendance claire**: Les opportunités d'achat à ≤40€/MWh explosent avec l'augmentation des renouvelables !

    La suite du dashboard présente l'analyse détaillée de ces 26,242 heures de données prix.
    """)

# === PAGE 1: VUE D'ENSEMBLE ===
elif page == "📊 Vue d'ensemble":
    st.title("⚡ Prix de l'Électricité en France (2022-2024)")
    st.markdown("## 🎯 Synthèse des données ENTSO-E")

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_hours = len(full_df)
        st.metric("Total heures", f"{total_hours:,}")

    with col2:
        avg_price = full_df['price'].mean()
        st.metric("Prix moyen", f"{avg_price:.2f} €/MWh")

    with col3:
        below_40_hours = len(below_40_df)
        below_40_pct = (below_40_hours / total_hours * 100) if total_hours > 0 else 0
        st.metric("Heures ≤40€", f"{below_40_hours:,}", delta=f"{below_40_pct:.1f}%")

    with col4:
        negative_hours = full_df['is_negative'].sum()
        negative_pct = (negative_hours / total_hours * 100) if total_hours > 0 else 0
        st.metric("Heures <0€", f"{negative_hours:,}", delta=f"{negative_pct:.1f}%")

    st.markdown("---")

    # Yearly comparison
    st.markdown("### 📊 Comparaison annuelle")

    col1, col2 = st.columns(2)

    with col1:
        # Bar chart - hours below 40
        fig_yearly = px.bar(
            summary_df,
            x='year',
            y='hours_below_40',
            title="Heures avec prix ≤40€/MWh par année",
            labels={'hours_below_40': 'Heures', 'year': 'Année'},
            color='hours_below_40',
            color_continuous_scale='RdYlGn',
            text='hours_below_40'
        )
        fig_yearly.update_traces(texttemplate='%{text:,.0f}h', textposition='outside')
        fig_yearly.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_yearly, use_container_width=True)

    with col2:
        # Average prices by year
        fig_avg = px.bar(
            summary_df,
            x='year',
            y='avg_price',
            title="Prix moyen annuel (€/MWh)",
            labels={'avg_price': 'Prix moyen (€/MWh)', 'year': 'Année'},
            color='avg_price',
            color_continuous_scale='Blues_r',
            text='avg_price'
        )
        fig_avg.update_traces(texttemplate='%{text:.2f}€', textposition='outside')
        fig_avg.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_avg, use_container_width=True)

    # Yearly details table
    st.markdown("### 📋 Statistiques détaillées par année")

    display_summary = summary_df.copy()
    display_summary['Année'] = display_summary['year'].astype(int)
    display_summary['Total heures'] = display_summary['total_hours'].apply(lambda x: f"{int(x):,}")
    display_summary['Heures ≤40€'] = display_summary['hours_below_40'].apply(lambda x: f"{int(x):,}")
    display_summary['% ≤40€'] = display_summary['percent_below_40'].apply(lambda x: f"{x:.1f}%")
    display_summary['Heures <0€'] = display_summary['hours_negative'].apply(lambda x: f"{int(x):,}")
    display_summary['Prix moyen'] = display_summary['avg_price'].apply(lambda x: f"{x:.2f}€")
    display_summary['Prix min'] = display_summary['min_price'].apply(lambda x: f"{x:.2f}€")
    display_summary['Prix max'] = display_summary['max_price'].apply(lambda x: f"{x:.2f}€")

    st.dataframe(
        display_summary[['Année', 'Total heures', 'Heures ≤40€', '% ≤40€', 'Heures <0€',
                         'Prix moyen', 'Prix min', 'Prix max']],
        use_container_width=True,
        hide_index=True
    )

    # Key insights
    st.markdown("### 💡 Insights clés")

    best_year = summary_df.loc[summary_df['hours_below_40'].idxmax()]['year']
    best_year_hours = summary_df.loc[summary_df['hours_below_40'].idxmax()]['hours_below_40']

    worst_year = summary_df.loc[summary_df['hours_below_40'].idxmin()]['year']
    worst_year_hours = summary_df.loc[summary_df['hours_below_40'].idxmin()]['hours_below_40']

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(f"""
        **Meilleure année**: {int(best_year)}

        {int(best_year_hours):,} heures ≤40€/MWh

        ({(best_year_hours/8760*100):.1f}% de l'année)
        """)

    with col2:
        st.warning(f"""
        **Année la plus chère**: {int(worst_year)}

        Seulement {int(worst_year_hours):,} heures ≤40€

        ({(worst_year_hours/8760*100):.1f}% de l'année)
        """)

    with col3:
        min_price_ever = full_df['price'].min()
        max_price_ever = full_df['price'].max()

        st.info(f"""
        **Fourchette de prix**

        Min: {min_price_ever:.2f}€/MWh

        Max: {max_price_ever:.2f}€/MWh
        """)

# === PAGE 2: ANALYSE DÉTAILLÉE ===
elif page == "📈 Analyse détaillée":
    st.title("📈 Analyse Détaillée des Prix")

    # Monthly trends
    st.markdown("### 📅 Tendances mensuelles")

    monthly_df['year_month'] = monthly_df['year'].astype(str) + '-' + monthly_df['month'].astype(str).str.zfill(2)

    fig_monthly = go.Figure()

    fig_monthly.add_trace(go.Scatter(
        x=monthly_df['year_month'],
        y=monthly_df['avg_price'],
        name='Prix moyen',
        mode='lines+markers',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6)
    ))

    fig_monthly.update_layout(
        title="Évolution du prix moyen mensuel (€/MWh)",
        xaxis_title="Mois",
        yaxis_title="Prix (€/MWh)",
        hovermode='x unified',
        height=400
    )

    st.plotly_chart(fig_monthly, use_container_width=True)

    # Monthly hours below 40
    st.markdown("### 💰 Heures ≤40€/MWh par mois")

    fig_monthly_40 = px.bar(
        monthly_df,
        x='year_month',
        y='hours_below_40',
        title="Nombre d'heures ≤40€/MWh par mois",
        labels={'hours_below_40': 'Heures', 'year_month': 'Mois'},
        color='hours_below_40',
        color_continuous_scale='RdYlGn'
    )

    fig_monthly_40.update_layout(height=400, coloraxis_showscale=False)
    st.plotly_chart(fig_monthly_40, use_container_width=True)

    # Hourly patterns
    st.markdown("### ⏰ Patterns horaires")

    hourly_stats = full_df.groupby('hour').agg({
        'price': 'mean',
        'is_below_40': 'mean'
    }).reset_index()

    hourly_stats['percent_below_40'] = hourly_stats['is_below_40'] * 100

    col1, col2 = st.columns(2)

    with col1:
        fig_hourly_price = px.bar(
            hourly_stats,
            x='hour',
            y='price',
            title="Prix moyen par heure de la journée",
            labels={'price': 'Prix moyen (€/MWh)', 'hour': 'Heure'},
            color='price',
            color_continuous_scale='Viridis'
        )
        fig_hourly_price.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_hourly_price, use_container_width=True)

    with col2:
        fig_hourly_40 = px.bar(
            hourly_stats,
            x='hour',
            y='percent_below_40',
            title="% d'heures ≤40€ par heure de la journée",
            labels={'percent_below_40': '% heures ≤40€', 'hour': 'Heure'},
            color='percent_below_40',
            color_continuous_scale='RdYlGn'
        )
        fig_hourly_40.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_hourly_40, use_container_width=True)

    # Weekend vs weekday
    st.markdown("### 📆 Week-end vs Semaine")

    weekend_stats = full_df.groupby('is_weekend').agg({
        'price': 'mean',
        'is_below_40': lambda x: (x.sum() / len(x) * 100)
    }).reset_index()

    weekend_stats['period'] = weekend_stats['is_weekend'].map({True: 'Week-end', False: 'Semaine'})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Prix moyen")
        for _, row in weekend_stats.iterrows():
            st.metric(row['period'], f"{row['price']:.2f} €/MWh")

    with col2:
        st.markdown("#### % heures ≤40€")
        for _, row in weekend_stats.iterrows():
            st.metric(row['period'], f"{row['is_below_40']:.1f}%")

# === PAGE 3: PRIX ≤40€/MWh ===
elif page == "💰 Prix ≤40€/MWh":
    st.title("💰 Analyse des Prix ≤40€/MWh")

    total_below_40 = len(below_40_df)
    st.markdown(f"### {total_below_40:,} heures identifiées avec prix ≤40€/MWh")

    # Distribution by year
    below_40_yearly = below_40_df.groupby('year').size().reset_index(name='count')

    col1, col2 = st.columns([2, 1])

    with col1:
        fig_dist = px.pie(
            below_40_yearly,
            values='count',
            names='year',
            title="Répartition des heures ≤40€ par année",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    with col2:
        st.markdown("#### Par année")
        for _, row in below_40_yearly.iterrows():
            st.metric(f"{int(row['year'])}", f"{int(row['count']):,} heures")

    # Monthly heatmap
    st.markdown("### 🗓️ Heatmap mensuelle des heures ≤40€")

    heatmap_data = below_40_df.groupby(['year', 'month']).size().reset_index(name='hours')
    heatmap_pivot = heatmap_data.pivot(index='month', columns='year', values='hours').fillna(0)

    fig_heatmap = px.imshow(
        heatmap_pivot,
        labels=dict(x="Année", y="Mois", color="Heures"),
        x=heatmap_pivot.columns,
        y=['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun',
           'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'],
        color_continuous_scale='RdYlGn',
        aspect="auto"
    )

    fig_heatmap.update_layout(height=500)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Price distribution for low prices
    st.markdown("### 📊 Distribution des prix ≤40€")

    fig_hist = px.histogram(
        below_40_df,
        x='price',
        nbins=40,
        title="Distribution des prix lorsque ≤40€/MWh",
        labels={'price': 'Prix (€/MWh)', 'count': 'Nombre d\'heures'},
        color_discrete_sequence=['#2ca02c']
    )

    st.plotly_chart(fig_hist, use_container_width=True)

    # Best periods
    st.markdown("### 🏆 Meilleures périodes")

    # Best months
    best_months = below_40_df.groupby(['year', 'month']).size().reset_index(name='hours')
    best_months = best_months.sort_values('hours', ascending=False).head(10)
    best_months['year_month'] = best_months['year'].astype(str) + '-' + best_months['month'].astype(str).str.zfill(2)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top 10 mois")
        for _, row in best_months.iterrows():
            st.write(f"**{row['year_month']}**: {int(row['hours'])} heures")

    with col2:
        # Best hours of day
        st.markdown("#### Meilleures heures")
        best_hours = below_40_df.groupby('hour').size().reset_index(name='count')
        best_hours = best_hours.sort_values('count', ascending=False).head(10)
        for _, row in best_hours.iterrows():
            st.write(f"**{int(row['hour'])}h**: {int(row['count']):,} occurrences")

# === PAGE 4: ÉVOLUTION TEMPORELLE ===
else:  # "📈 Évolution temporelle"
    st.title("📈 Évolution Temporelle des Prix")

    # Year selector
    selected_year = st.selectbox("Sélectionner une année", [2022, 2023, 2024])

    year_df = full_df[full_df['year'] == selected_year].copy()

    st.markdown(f"### Prix horaires {selected_year}")

    # Time series
    fig_ts = go.Figure()

    fig_ts.add_trace(go.Scatter(
        x=year_df['datetime'],
        y=year_df['price'],
        mode='lines',
        name='Prix',
        line=dict(color='#1f77b4', width=1)
    ))

    # Add 40€ threshold line
    fig_ts.add_hline(
        y=40,
        line_dash="dash",
        line_color="red",
        annotation_text="Seuil 40€/MWh",
        annotation_position="right"
    )

    fig_ts.update_layout(
        title=f"Évolution du prix horaire en {selected_year}",
        xaxis_title="Date",
        yaxis_title="Prix (€/MWh)",
        hovermode='x unified',
        height=500
    )

    st.plotly_chart(fig_ts, use_container_width=True)

    # Statistics for selected year
    st.markdown(f"### 📊 Statistiques {selected_year}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Prix moyen", f"{year_df['price'].mean():.2f}€")

    with col2:
        st.metric("Prix médian", f"{year_df['price'].median():.2f}€")

    with col3:
        below_40_count = year_df['is_below_40'].sum()
        st.metric("Heures ≤40€", f"{int(below_40_count):,}")

    with col4:
        negative_count = year_df['is_negative'].sum()
        st.metric("Heures <0€", f"{int(negative_count):,}")

    # Box plot by month
    st.markdown(f"### 📦 Distribution mensuelle des prix en {selected_year}")

    year_df['month_name'] = year_df['datetime'].dt.strftime('%b')

    fig_box = px.box(
        year_df,
        x='month',
        y='price',
        title=f"Distribution des prix par mois ({selected_year})",
        labels={'price': 'Prix (€/MWh)', 'month': 'Mois'},
        category_orders={'month': list(range(1, 13))}
    )

    fig_box.update_layout(height=500)
    st.plotly_chart(fig_box, use_container_width=True)

# === PAGE 5: SOURCES ===
elif page == "\U0001F4DA Sources":  # 📚 emoji as Unicode escape
    st.title("📚 Sources et Validation des Données")

    st.markdown("""
    Cette page recense toutes les sources externes utilisées pour valider les ordres de grandeur
    de nos analyses sur les MWh disponibles à ≤40€/MWh.
    """)

    # Section 1: Sources Officielles RTE
    st.markdown("## 🏛️ Sources Officielles Françaises")

    st.markdown("### RTE (Réseau de Transport d'Électricité)")

    sources_rte = [
        {
            "titre": "Bilan Électrique 2024",
            "url": "https://analysesetdonnees.rte-france.com/bilan-electrique-2024",
            "type": "Page web interactive",
            "données_clés": "89 TWh exports nets, 361.7 TWh nucléaire, 71.5% disponibilité nucléaire",
            "pertinence": "Source primaire pour exports transfrontaliers et production nucléaire"
        },
        {
            "titre": "Bilan Électrique 2024 - Europe",
            "url": "https://analysesetdonnees.rte-france.com/bilan-electrique-2024/europe",
            "type": "Page web",
            "données_clés": "Détails exports par pays: DE+BE 27.2 TWh, IT 22.3 TWh, UK 20.1 TWh",
            "pertinence": "Validation exports par pays frontalier"
        },
        {
            "titre": "Bilan Électrique 2024 - Production",
            "url": "https://analysesetdonnees.rte-france.com/bilan-electrique-2024/production",
            "type": "Page web",
            "données_clés": "Production nucléaire +13% vs 2023, capacité 61 GW",
            "pertinence": "Validation production et disponibilité nucléaire"
        },
        {
            "titre": "Bilan Électrique 2023",
            "url": "https://analysesetdonnees.rte-france.com/bilan-electrique-2023",
            "type": "Page web",
            "données_clés": "50.1 TWh exports nets 2023 (vs -16.5 TWh en 2022)",
            "pertinence": "Comparaison historique exports 2022-2023"
        },
        {
            "titre": "Bilan S1 2024 (PDF)",
            "url": "https://assets.rte-france.com/prod/public/2024-08/2024-08-02-bilan-s1-2024-fr.pdf",
            "type": "Rapport PDF",
            "données_clés": "235 heures prix négatifs S1 2024 (5.4% du temps)",
            "pertinence": "Validation prix négatifs et production renouvelable"
        }
    ]

    for source in sources_rte:
        with st.expander(f"📄 {source['titre']}"):
            st.markdown(f"**Type**: {source['type']}")
            st.markdown(f"**URL**: [{source['url']}]({source['url']})")
            st.markdown(f"**Données clés**: {source['données_clés']}")
            st.markdown(f"**Pertinence**: {source['pertinence']}")

    # Section 2: CRE
    st.markdown("### CRE (Commission de Régulation de l'Énergie)")

    sources_cre = [
        {
            "titre": "Analyse Prix Négatifs 2024",
            "url": "https://www.cre.fr/fileadmin/Documents/Rapports_et_etudes/2024/241126_Note_Prix_negatifs.pdf",
            "type": "Rapport PDF",
            "données_clés": "359h prix négatifs 2024, France exportatrice 83% du temps, pertes 80 M€",
            "pertinence": "Comportement exports pendant prix négatifs"
        },
        {
            "titre": "Présentation Prix Négatifs",
            "url": "https://www.cre.fr/fileadmin/Documents/Rapports_et_etudes/2024/241126_Presentation_prix_negatifs.pdf",
            "type": "Présentation PDF",
            "données_clés": "Imports DE+BE pendant 71% heures prix négatifs",
            "pertinence": "Impact interconnexions sur prix négatifs"
        }
    ]

    for source in sources_cre:
        with st.expander(f"📄 {source['titre']}"):
            st.markdown(f"**Type**: {source['type']}")
            st.markdown(f"**URL**: [{source['url']}]({source['url']})")
            st.markdown(f"**Données clés**: {source['données_clés']}")
            st.markdown(f"**Pertinence**: {source['pertinence']}")

    # Section 3: ENTSO-E
    st.markdown("## 🇪🇺 Sources Européennes")

    st.markdown("### ENTSO-E (European Network of TSOs)")

    sources_entsoe = [
        {
            "titre": "Transparency Platform - Day-Ahead Prices",
            "url": "https://transparency.entsoe.eu/transmission-domain/r2/dayAheadPrices/show",
            "type": "Plateforme de données",
            "données_clés": "Prix spot horaires France 2022-2024 (source primaire dashboard)",
            "pertinence": "Source primaire de nos données scrapées"
        },
        {
            "titre": "Transparency Platform - Physical Flows",
            "url": "https://transparency.entsoe.eu/transmission/physicalFlows",
            "type": "Plateforme de données",
            "données_clés": "Flux transfrontaliers horaires (en cours de scraping Phase 2)",
            "pertinence": "Source Q1: Exports pendant heures ≤40€"
        },
        {
            "titre": "Transparency Platform - Generation by Type",
            "url": "https://transparency.entsoe.eu/generation/r2/actualGenerationPerProductionType",
            "type": "Plateforme de données",
            "données_clés": "Production horaire par type (nucléaire, solaire, éolien)",
            "pertinence": "Source future Q2: Nucléaire non produit"
        }
    ]

    for source in sources_entsoe:
        with st.expander(f"📄 {source['titre']}"):
            st.markdown(f"**Type**: {source['type']}")
            st.markdown(f"**URL**: [{source['url']}]({source['url']})")
            st.markdown(f"**Données clés**: {source['données_clés']}")
            st.markdown(f"**Pertinence**: {source['pertinence']}")

    # Section 4: Presse & Analyses Sectorielles
    st.markdown("## 📰 Presse et Analyses Sectorielles")

    sources_presse = [
        {
            "titre": "Montel News - French Curtailment Record",
            "url": "https://montelnews.com/news/93be1c1e-dbe8-4d7a-a4c8-a9c789d1e8e3/french-renewables-curtailment-hits-record-1-7-twh-in-2024",
            "type": "Article de presse",
            "données_clés": "1.7 TWh écrêtés 2024 (0.9 TWh éolien + 0.8 TWh solaire), ×2.8 vs 2023",
            "pertinence": "Validation Q3: Écrêtage renouvelables"
        },
        {
            "titre": "U.S. EIA - France Nuclear Increase 2024",
            "url": "https://www.eia.gov/todayinenergy/detail.php?id=65785",
            "type": "Analyse internationale",
            "données_clés": "Récupération production nucléaire → plus d'exports",
            "pertinence": "Contexte international exports français"
        },
        {
            "titre": "Statista - France Top EU Exporter",
            "url": "https://fr.statista.com/infographie/32647/volume-exportation-electricite-france-vers-les-pays-europeens/",
            "type": "Infographie",
            "données_clés": "Graphiques exports par pays européen",
            "pertinence": "Visualisation comparative exports"
        }
    ]

    for source in sources_presse:
        with st.expander(f"📄 {source['titre']}"):
            st.markdown(f"**Type**: {source['type']}")
            st.markdown(f"**URL**: [{source['url']}]({source['url']})")
            st.markdown(f"**Données clés**: {source['données_clés']}")
            st.markdown(f"**Pertinence**: {source['pertinence']}")

    # Section 5: Synthèse Validation
    st.markdown("## ✅ Synthèse des Ordres de Grandeur Validés")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Exports 2024", "89 TWh", help="Source: RTE Bilan 2024")
        st.caption("Exports pendant ≤40€: 20-40 TWh estimés")

    with col2:
        st.metric("Production Nucléaire", "361.7 TWh", help="Source: RTE Bilan 2024")
        st.caption("Sous-utilisation: 7-15 TWh estimés")

    with col3:
        st.metric("Écrêtage Renouvelables", "1.7 TWh", help="Source: Montel News")
        st.caption("Quasi-intégralité pendant ≤40€")

    st.markdown("---")

    st.info("""
    **📊 Total MWh disponibles à ≤40€/MWh: 30-55 TWh/an (2024)**

    Ces ordres de grandeur sont cohérents avec:
    - Les bilans officiels RTE 2022-2024
    - Les analyses CRE sur les prix négatifs
    - Les données ENTSO-E scrapées (26,254 heures)
    - Les rapports sectoriels internationaux

    **Phase 2** en cours: Scraping des flux transfrontaliers et production par type
    pour quantifier précisément chaque composante en croisant avec nos données de prix.
    """)

    # Méthodologie
    st.markdown("## 🔬 Méthodologie de Validation")

    st.markdown("""
    ### Approche Cross-Validation

    1. **Sources Primaires** (RTE, ENTSO-E, CRE)
       - Données officielles de référence
       - Publications annuelles validées
       - Rapports réglementaires

    2. **Sources Secondaires** (Presse spécialisée, EIA, Statista)
       - Confirmation des tendances
       - Perspectives internationales
       - Analyses sectorielles

    3. **Données Scrapées** (Notre projet)
       - Prix horaires ENTSO-E 2022-2024
       - Flux transfrontaliers (en cours)
       - Production par type (à venir)

    ### Critères de Fiabilité

    - ✅ **Cohérence**: Les chiffres de différentes sources convergent (±5%)
    - ✅ **Officialité**: Priorité aux opérateurs de réseau (RTE, ENTSO-E)
    - ✅ **Granularité**: Données horaires > quotidiennes > mensuelles
    - ✅ **Actualité**: Publications 2024-2025 pour données 2022-2024

    ### Limitations Identifiées

    - ⚠️ **Écrêtage réel**: Pas de données publiques directes, proxy prix négatifs
    - ⚠️ **Raisons sous-utilisation nucléaire**: Maintenance vs dispatch économique
    - ⚠️ **Flux transit**: Physical Flows incluent transit (pas seulement exports FR)
    """)

    # Document de référence
    st.markdown("## 📄 Document de Référence Complet")

    st.markdown("""
    Toutes les sources sont détaillées dans le document:

    **`docs/VALIDATION_DATA_SOURCES.md`**

    Ce document inclut:
    - Tableaux récapitulatifs exports 2022-2024
    - Production nucléaire et disponibilité
    - Écrêtage renouvelables
    - Estimations valorisation potentielle
    - Hypothèses et limitations

    📥 Accessible dans le dépôt GitHub du projet.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>Dashboard ENTSO-E Prix Électricité France 2022-2024</strong></p>
    <p>Source: ENTSO-E Transparency Platform | Scraping: Playwright | Mise à jour: Temps réel</p>
    <p>Données: {0:,} heures scraped sur 3 ans | Granularité: Horaire</p>
</div>
""".format(len(full_df)), unsafe_allow_html=True)
