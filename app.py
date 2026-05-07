import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="COFICAB · Ventes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── THEME CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

  /* Background */
  .stApp { background-color: #0b0f1a; color: #e8edf5; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1f2d47;
  }
  [data-testid="stSidebar"] * { color: #e8edf5 !important; }

  /* Metric cards */
  [data-testid="stMetric"] {
    background: #111827;
    border: 1px solid #1f2d47;
    border-radius: 14px;
    padding: 20px 24px;
  }
  [data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #5a6a84 !important;
  }
  [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    color: #e8edf5 !important;
  }
  [data-testid="stMetricDelta"] { font-family: 'DM Mono', monospace !important; }

  /* Dataframe */
  [data-testid="stDataFrame"] { border: 1px solid #1f2d47; border-radius: 10px; }

  /* Selectbox / multiselect */
  .stSelectbox > div, .stMultiSelect > div {
    background-color: #1a2235 !important;
    border-color: #1f2d47 !important;
    border-radius: 8px !important;
  }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] {
    background: #111827;
    border: 1px solid #1f2d47;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 7px;
    color: #5a6a84;
    font-weight: 500;
    font-size: 0.85rem;
  }
  .stTabs [aria-selected="true"] {
    background: #00e5a0 !important;
    color: #000 !important;
    font-weight: 700 !important;
  }

  /* Divider */
  hr { border-color: #1f2d47; }

  /* Header */
  .logo-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #e8edf5;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 4px;
  }
  .logo-badge {
    background: #00e5a0;
    color: #000;
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 1rem;
    font-weight: 700;
  }
  .subtitle {
    color: #5a6a84;
    font-size: 0.82rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.05em;
  }
  .section-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: #e8edf5;
    margin-bottom: 2px;
  }
  .section-sub {
    font-size: 0.75rem;
    color: #5a6a84;
    margin-bottom: 14px;
  }
  .kpi-accent { color: #00e5a0; font-family: 'DM Mono', monospace; }
</style>
""", unsafe_allow_html=True)

ACCENT   = "#00e5a0"
ACCENT2  = "#0073ff"
ACCENT3  = "#ff4d6d"
ACCENT4  = "#f5a623"
BG       = "#0b0f1a"
SURFACE  = "#111827"
SURFACE2 = "#1a2235"
BORDER   = "#1f2d47"
MUTED    = "#5a6a84"
TEXT     = "#e8edf5"

PLOTLY_LAYOUT = dict(
    paper_bgcolor=SURFACE,
    plot_bgcolor=SURFACE,
    font=dict(family="DM Sans", color=TEXT),
    xaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, tickfont=dict(color=MUTED, size=11)),
    yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, tickfont=dict(color=MUTED, size=11)),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=MUTED, size=11)),
    margin=dict(l=12, r=12, t=32, b=12),
)

# ─── LOAD DATA ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("ventes.xlsx")
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"].astype(str), format="%Y%m%d")
    df["Month"]  = df["Date"].dt.to_period("M").astype(str)
    df["Week"]   = df["Date"].dt.isocalendar().week.astype(int)
    df["YearWeek"] = df["Date"].dt.strftime("%Y-W%V")
    df["Cross Section Num"] = pd.to_numeric(df["Cross Section"], errors="coerce")
    return df

df = load_data()

# ─── SIDEBAR FILTERS ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="logo-header"><span class="logo-badge">$</span> COFICAB</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Tableau de bord · Ventes</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 🎛 Filtres")

    entity_opts = ["Tous"] + sorted(df["Entities"].dropna().unique().tolist())
    entity = st.selectbox("Entité", entity_opts)

    customer_opts = ["Tous"] + sorted(df["Customer"].dropna().unique().tolist())
    customer = st.selectbox("Client", customer_opts)

    family_opts = ["Tous"] + sorted(df["Family"].dropna().unique().tolist())
    family = st.selectbox("Famille produit", family_opts)

    date_min = df["Date"].min().date()
    date_max = df["Date"].max().date()
    date_range = st.date_input("Période", value=(date_min, date_max), min_value=date_min, max_value=date_max)

    st.markdown("---")
    st.markdown(f'<div class="subtitle">📅 Données : {date_min.strftime("%d %b")} → {date_max.strftime("%d %b %Y")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">📦 {len(df):,} lignes · {df["Customer"].nunique()} clients</div>', unsafe_allow_html=True)

# ─── APPLY FILTERS ────────────────────────────────────────────────────────────
fdf = df.copy()
if entity != "Tous":
    fdf = fdf[fdf["Entities"] == entity]
if customer != "Tous":
    fdf = fdf[fdf["Customer"] == customer]
if family != "Tous":
    fdf = fdf[fdf["Family"] == family]
if len(date_range) == 2:
    fdf = fdf[(fdf["Date"].dt.date >= date_range[0]) & (fdf["Date"].dt.date <= date_range[1])]

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="logo-header">📊 Vue d\'ensemble · Ventes</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">Données filtrées · {len(fdf):,} lignes affichées</div>', unsafe_allow_html=True)
st.markdown("")

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["  KPI & Tendances  ", "  Clients  ", "  Produits  ", "  Données brutes  "])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — KPI & TENDANCES
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    total_amount  = fdf["Amount"].sum()
    total_qty_m   = fdf["QTY M"].sum()
    total_qty_km  = fdf["QTY KM"].sum()
    avg_lme       = fdf["LME"].mean()
    n_invoices    = fdf["Invoice"].nunique()
    n_customers   = fdf["Customer"].nunique()

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Chiffre d'affaires", f"{total_amount:,.0f} MAD", delta=None)
    c2.metric("Quantité (m)", f"{total_qty_m:,.0f} m")
    c3.metric("Quantité (km)", f"{total_qty_km:,.1f} km")
    c4.metric("LME moyen", f"{avg_lme:.3f}")
    c5.metric("Factures", f"{n_invoices:,}")
    c6.metric("Clients actifs", f"{n_customers}")

    st.markdown("")

    # ── Revenus par mois ──────────────────────────────────────────────────────
    col_l, col_r = st.columns([2, 1])

    with col_l:
        st.markdown('<div class="section-title">Chiffre d\'affaires mensuel</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Montant total par mois · en MAD</div>', unsafe_allow_html=True)

        monthly = fdf.groupby("Month").agg(Amount=("Amount", "sum"), QTY_M=("QTY M", "sum")).reset_index()

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=monthly["Month"], y=monthly["Amount"],
            name="Montant (MAD)", marker_color=ACCENT,
            opacity=0.85, hovertemplate="%{x}<br>%{y:,.0f} MAD<extra></extra>"
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=monthly["Month"], y=monthly["QTY_M"],
            name="Quantité (m)", line=dict(color=ACCENT2, width=2.5),
            mode="lines+markers", marker=dict(size=6),
            hovertemplate="%{x}<br>%{y:,.0f} m<extra></extra>"
        ), secondary_y=True)
        fig.update_layout(**PLOTLY_LAYOUT, height=300, barmode="overlay")
        fig.update_yaxes(title_text="Montant MAD", secondary_y=False, title_font=dict(color=ACCENT))
        fig.update_yaxes(title_text="Quantité m", secondary_y=True, title_font=dict(color=ACCENT2))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title">Répartition par entité</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Part du CA par entité</div>', unsafe_allow_html=True)

        by_entity = fdf.groupby("Entities")["Amount"].sum().reset_index()
        fig2 = px.pie(
            by_entity, values="Amount", names="Entities",
            color_discrete_sequence=[ACCENT, ACCENT2, ACCENT3, ACCENT4],
            hole=0.65,
        )
        fig2.update_traces(textinfo="percent+label", textfont_color=TEXT)
        fig2.update_layout(**PLOTLY_LAYOUT, height=300, showlegend=True)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("")

    # ── Évolution hebdomadaire ─────────────────────────────────────────────────
    st.markdown('<div class="section-title">Évolution hebdomadaire</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Cumul du montant par semaine et par entité</div>', unsafe_allow_html=True)

    weekly = fdf.groupby(["YearWeek", "Entities"])["Amount"].sum().reset_index()
    fig3 = px.line(
        weekly, x="YearWeek", y="Amount", color="Entities",
        color_discrete_sequence=[ACCENT, ACCENT2, ACCENT3],
        markers=True, line_shape="spline",
        labels={"Amount": "Montant (MAD)", "YearWeek": "Semaine"},
    )
    fig3.update_traces(line_width=2.5, marker_size=5)
    fig3.update_layout(**PLOTLY_LAYOUT, height=280)
    st.plotly_chart(fig3, use_container_width=True)

    # ── LME dans le temps ─────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Indice LME dans le temps</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Valeur LME moyenne par semaine</div>', unsafe_allow_html=True)

    lme_weekly = fdf.groupby("YearWeek")["LME"].mean().reset_index()
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=lme_weekly["YearWeek"], y=lme_weekly["LME"],
        fill="tozeroy", fillcolor="rgba(0,115,255,0.12)",
        line=dict(color=ACCENT2, width=2.5), mode="lines",
        hovertemplate="%{x}<br>LME: %{y:.3f}<extra></extra>"
    ))
    fig4.update_layout(**PLOTLY_LAYOUT, height=240)
    st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CLIENTS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Performance par client</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Montant total · quantité · nombre de lignes</div>', unsafe_allow_html=True)

    by_customer = fdf.groupby("Customer").agg(
        Montant=("Amount", "sum"),
        QTY_M=("QTY M", "sum"),
        QTY_KM=("QTY KM", "sum"),
        Lignes=("Amount", "count"),
        Factures=("Invoice", "nunique"),
    ).reset_index().sort_values("Montant", ascending=False)

    # Bar chart
    fig5 = px.bar(
        by_customer, x="Montant", y="Customer",
        orientation="h", color="Montant",
        color_continuous_scale=[[0, SURFACE2], [1, ACCENT]],
        labels={"Montant": "CA (MAD)", "Customer": ""},
        text=by_customer["Montant"].apply(lambda x: f"{x:,.0f}"),
    )
    fig5.update_traces(textposition="outside", textfont_color=MUTED)
    fig5.update_layout(**PLOTLY_LAYOUT, height=400, coloraxis_showscale=False)
    fig5.update_yaxes(categoryorder="total ascending", gridcolor=BORDER)
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-title">Quantité (m) par client</div>', unsafe_allow_html=True)
        fig6 = px.pie(
            by_customer, values="QTY_M", names="Customer",
            color_discrete_sequence=[ACCENT, ACCENT2, ACCENT3, ACCENT4, "#a78bfa", "#34d399"],
            hole=0.55,
        )
        fig6.update_traces(textinfo="percent", textfont_color=TEXT)
        fig6.update_layout(**PLOTLY_LAYOUT, height=340, showlegend=True)
        st.plotly_chart(fig6, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title">Évolution mensuelle par client</div>', unsafe_allow_html=True)
        cust_monthly = fdf.groupby(["Month", "Customer"])["Amount"].sum().reset_index()
        fig7 = px.line(
            cust_monthly, x="Month", y="Amount", color="Customer",
            markers=True, line_shape="spline",
            labels={"Amount": "CA (MAD)", "Month": "Mois"},
            color_discrete_sequence=[ACCENT, ACCENT2, ACCENT3, ACCENT4, "#a78bfa", "#34d399",
                                     "#fb923c", "#e879f9", "#94a3b8", "#22d3ee"],
        )
        fig7.update_layout(**PLOTLY_LAYOUT, height=340)
        st.plotly_chart(fig7, use_container_width=True)

    # Table récapitulative
    st.markdown('<div class="section-title">Tableau récapitulatif clients</div>', unsafe_allow_html=True)
    by_customer["Montant"] = by_customer["Montant"].map("{:,.0f}".format)
    by_customer["QTY_M"]   = by_customer["QTY_M"].map("{:,.0f}".format)
    by_customer["QTY_KM"]  = by_customer["QTY_KM"].map("{:,.1f}".format)
    st.dataframe(
        by_customer.rename(columns={"Customer": "Client", "QTY_M": "Qté (m)",
                                    "QTY_KM": "Qté (km)", "Lignes": "Nb lignes", "Factures": "Nb factures"}),
        use_container_width=True, hide_index=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PRODUITS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown('<div class="section-title">Top 20 familles produits</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Par chiffre d\'affaires</div>', unsafe_allow_html=True)
        by_family = fdf.groupby("Family")["Amount"].sum().nlargest(20).reset_index()
        fig8 = px.bar(
            by_family, x="Amount", y="Family", orientation="h",
            color="Amount", color_continuous_scale=[[0, SURFACE2], [1, ACCENT4]],
            labels={"Amount": "CA (MAD)", "Family": ""},
            text=by_family["Amount"].apply(lambda x: f"{x:,.0f}"),
        )
        fig8.update_traces(textposition="outside", textfont_color=MUTED)
        fig8.update_layout(**PLOTLY_LAYOUT, height=500, coloraxis_showscale=False)
        fig8.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig8, use_container_width=True)

    with col_p2:
        st.markdown('<div class="section-title">Sections transversales</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Distribution par section (mm²)</div>', unsafe_allow_html=True)
        by_section = fdf.groupby("Cross Section").agg(
            Amount=("Amount", "sum"), QTY_M=("QTY M", "sum")
        ).reset_index().sort_values("Amount", ascending=False).head(20)
        fig9 = px.bar(
            by_section, x="Cross Section", y="Amount",
            color="QTY_M", color_continuous_scale=[[0, SURFACE2], [1, ACCENT2]],
            labels={"Amount": "CA (MAD)", "Cross Section": "Section (mm²)", "QTY_M": "Qté (m)"},
        )
        fig9.update_layout(**PLOTLY_LAYOUT, height=500, coloraxis_colorbar=dict(title="Qté (m)"))
        st.plotly_chart(fig9, use_container_width=True)

    st.markdown("")
    st.markdown('<div class="section-title">Famille & Section — Heatmap CA</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Top 15 familles · Top 10 sections</div>', unsafe_allow_html=True)

    top_fam  = fdf.groupby("Family")["Amount"].sum().nlargest(15).index.tolist()
    top_sec  = fdf.groupby("Cross Section")["Amount"].sum().nlargest(10).index.tolist()
    heat_df  = fdf[fdf["Family"].isin(top_fam) & fdf["Cross Section"].isin(top_sec)]
    pivot    = heat_df.pivot_table(values="Amount", index="Family", columns="Cross Section",
                                   aggfunc="sum", fill_value=0)

    fig10 = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale=[[0, SURFACE2], [0.5, ACCENT2], [1, ACCENT]],
        hoverongaps=False,
        hovertemplate="Section: %{x}<br>Famille: %{y}<br>CA: %{z:,.0f} MAD<extra></extra>",
    ))
    fig10.update_layout(**PLOTLY_LAYOUT, height=420, xaxis_title="Section (mm²)", yaxis_title="Famille")
    st.plotly_chart(fig10, use_container_width=True)

    # CU vs AV scatter
    st.markdown('<div class="section-title">Prix unitaire CU vs AV</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Comparaison par client · taille = quantité</div>', unsafe_allow_html=True)
    sample = fdf.sample(min(3000, len(fdf)), random_state=42)
    fig11 = px.scatter(
        sample, x="CU", y="AV", color="Customer", size="QTY M",
        size_max=18, opacity=0.7,
        color_discrete_sequence=[ACCENT, ACCENT2, ACCENT3, ACCENT4, "#a78bfa", "#34d399",
                                  "#fb923c", "#e879f9", "#94a3b8", "#22d3ee"],
        labels={"CU": "Prix CU", "AV": "Prix AV", "Customer": "Client"},
        hover_data=["Family", "Cross Section"],
    )
    fig11.update_layout(**PLOTLY_LAYOUT, height=380)
    st.plotly_chart(fig11, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — DONNÉES BRUTES
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">Données brutes filtrées</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{len(fdf):,} lignes · {len(fdf.columns)} colonnes</div>', unsafe_allow_html=True)

    search = st.text_input("🔍 Rechercher dans les données", placeholder="Famille, client, DN…")
    if search:
        mask = fdf.apply(lambda col: col.astype(str).str.contains(search, case=False, na=False)).any(axis=1)
        display_df = fdf[mask]
    else:
        display_df = fdf

    st.dataframe(
        display_df.drop(columns=["Month", "Week", "YearWeek", "Cross Section Num"], errors="ignore"),
        use_container_width=True, height=520,
    )

    col_dl1, col_dl2 = st.columns([1, 5])
    with col_dl1:
        csv = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Exporter CSV",
            data=csv, file_name="ventes_filtrees.csv", mime="text/csv",)

