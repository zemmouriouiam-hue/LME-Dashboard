import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── CONFIG ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="COFICAB · Analyse des Ventes (EUR)",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DESIGN SYSTEM ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --navy:    #050d1a;
  --navy2:   #0a1628;
  --navy3:   #0f2040;
  --border:  #1a3560;
  --gold:    #f0b429;
  --golddim: rgba(240,180,41,0.15);
  --cyan:    #00d4ff;
  --text:    #dce8f5;
  --muted:   #4d6b8a;
}

html, body, [class*="css"] { font-family: 'Barlow', sans-serif; }

.stApp {
  background-color: var(--navy);
  background-image:
    linear-gradient(rgba(26,53,96,0.22) 1px, transparent 1px),
    linear-gradient(90deg, rgba(26,53,96,0.22) 1px, transparent 1px);
  background-size: 44px 44px;
  color: var(--text);
}

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0a1628 0%, #050d1a 100%) !important;
  border-right: 1px solid var(--border) !important;
}

[data-testid="stMetric"] {
  background: linear-gradient(135deg, #0f2040 0%, #0a1628 100%);
  border: 1px solid var(--border);
  border-bottom: 3px solid var(--gold);
  border-radius: 10px;
  padding: 20px 22px 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.45);
}

[data-testid="stMetricValue"] {
  font-family: 'Bebas Neue', sans-serif !important;
  font-size: 2rem !important;
  color: #f0f6ff !important;
}

.brand-logo {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.55rem;
  letter-spacing: 3px;
  color: #f0f6ff;
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-logo .pill {
  background: linear-gradient(135deg, #f0b429, #f5c842);
  color: #050d1a;
  border-radius: 6px;
  padding: 3px 12px;
}

.section-hdr {
  font-family: 'Barlow', sans-serif;
  font-weight: 700;
  font-size: 0.75rem;
  color: #7a9cbd;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 9px;
}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTES COULEURS ────────────────────────────────────────────────────────
GOLD, CYAN, GREEN, CORAL = "#f0b429", "#00d4ff", "#00e87a", "#ff5757"
NAVY2, BORDER, MUTED, TEXT = "#0a1628", "#1a3560", "#4d6b8a", "#dce8f5"
VIVID = [CYAN, GOLD, GREEN, CORAL, "#a855f7", "#fb923c"]

PLOTLY = dict(
    paper_bgcolor=NAVY2,
    plot_bgcolor=NAVY2,
    font=dict(family="Barlow", color=TEXT, size=12),
    xaxis=dict(gridcolor="#0e1f38", linecolor=BORDER, tickfont=dict(color=MUTED)),
    yaxis=dict(gridcolor="#0e1f38", linecolor=BORDER, tickfont=dict(color=MUTED)),
    margin=dict(l=16, r=16, t=40, b=16),
)

# ── CHARGEMENT DES DONNÉES ─────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("ventes.xlsx")
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"].astype(str), format="%Y%m%d")
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["YearWeek"] = df["Date"].dt.strftime("%Y-W%V")
    # Conversion de la section en string pour un filtrage propre
    df["Cross Section"] = df["Cross Section"].astype(str).replace('nan', 'N/A')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Erreur lors du chargement du fichier 'ventes.xlsx': {e}")
    st.stop()

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="brand-logo"><span class="pill">C</span> COFICAB</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    entity = st.selectbox("Entité", ["Tous"] + sorted(df["Entities"].dropna().unique().tolist()))
    customer = st.selectbox("Client", ["Tous"] + sorted(df["Customer"].dropna().unique().tolist()))
    family = st.selectbox("Famille produit", ["Tous"] + sorted(df["Family"].dropna().unique().tolist()))
    
    # NOUVEAU FILTRE : Cross Section
    sections = sorted(df["Cross Section"].unique().tolist())
    section_filter = st.selectbox("Cross Section (mm²)", ["Tous"] + sections)

    date_range = st.date_input("Période", value=(df["Date"].min().date(), df["Date"].max().date()))

# ── FILTRAGE ───────────────────────────────────────────────────────────────────
fdf = df.copy()
if entity != "Tous": fdf = fdf[fdf["Entities"] == entity]
if customer != "Tous": fdf = fdf[fdf["Customer"] == customer]
if family != "Tous": fdf = fdf[fdf["Family"] == family]
if section_filter != "Tous": fdf = fdf[fdf["Cross Section"] == section_filter]
if len(date_range) == 2:
    fdf = fdf[(fdf["Date"].dt.date >= date_range[0]) & (fdf["Date"].dt.date <= date_range[1])]

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown('<div style="font-family:Bebas Neue; font-size:2.4rem; color:white;">Analyse des Ventes</div>', unsafe_allow_html=True)
st.markdown(f'<div style="font-family:JetBrains Mono; color:{MUTED}; font-size:0.75rem;">COFICAB GROUP · DEVISE : EUR</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["⚡ KPI & Tendances", "👥 Clients", "📦 Produits", "🗃 Données brutes"])

# --- TAB 1: KPI ---
with tab1:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("CA Total", f"{fdf['Amount'].sum()/1e6:.2f}M €")
    c2.metric("Volume (m)", f"{fdf['QTY M'].sum()/1e3:.1f}K m")
    # QUANTITÉ MOYENNE PAR LIGNE
    c3.metric("Qté Moyenne", f"{fdf['QTY M'].mean():.1f} m") 
    c4.metric("LME Moyen", f"{fdf['LME'].mean():.3f}")
    c5.metric("Nb Factures", f"{fdf['Invoice'].nunique():,}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-hdr">CA MENSUEL & VOLUME</div>', unsafe_allow_html=True)
    
    monthly = fdf.groupby("Month").agg(Amount=("Amount","sum"), Qty=("QTY M","sum")).reset_index()
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(go.Bar(x=monthly["Month"], y=monthly["Amount"], name="CA (€)", marker_color=GOLD), secondary_y=False)
    fig1.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Qty"], name="Volume (m)", line=dict(color=CYAN, width=3)), secondary_y=True)
    fig1.update_layout(**PLOTLY, height=350)
    st.plotly_chart(fig1, use_container_width=True)

# --- TAB 2: CLIENTS ---
with tab2:
    st.markdown('<div class="section-hdr">TOP 10 CLIENTS (EUR)</div>', unsafe_allow_html=True)
    top_cust = fdf.groupby("Customer")["Amount"].sum().nlargest(10).reset_index()
    fig2 = px.bar(top_cust, x="Amount", y="Customer", orientation='h', color="Amount", color_continuous_scale="Blues")
    fig2.update_layout(**PLOTLY, height=400, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# --- TAB 3: PRODUITS ---
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-hdr">RÉPARTITION PAR FAMILLE (€)</div>', unsafe_allow_html=True)
        fam_data = fdf.groupby("Family")["Amount"].sum().reset_index()
        fig3 = px.pie(fam_data, values="Amount", names="Family", hole=0.5, color_discrete_sequence=VIVID)
        fig3.update_layout(**PLOTLY, height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-hdr">TOP CROSS SECTIONS (€)</div>', unsafe_allow_html=True)
        sec_data = fdf.groupby("Cross Section")["Amount"].sum().nlargest(10).reset_index()
        fig4 = px.bar(sec_data, x="Cross Section", y="Amount", marker_color=CYAN)
        fig4.update_layout(**PLOTLY, height=400)
        st.plotly_chart(fig4, use_container_width=True)

# --- TAB 4: DONNÉES ---
with tab4:
    st.markdown('<div class="section-hdr">DONNÉES FILTRÉES</div>', unsafe_allow_html=True)
    st.dataframe(fdf, use_container_width=True)
