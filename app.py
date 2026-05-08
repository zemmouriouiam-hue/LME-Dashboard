import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── CONFIG ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="COFICAB · Analyse des Ventes",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DESIGN SYSTEM ──────────────────────────────────────────────────────────────
# Aesthetic: Executive Intelligence
# Deep navy grid background + Electric gold accents + vivid data palette
# Fonts: Bebas Neue (display) + Barlow (body) + JetBrains Mono (data)
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
  --green:   #00e87a;
  --coral:   #ff5757;
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

/* SIDEBAR */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0a1628 0%, #050d1a 100%) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background: var(--navy3) !important;
  border-color: var(--border) !important;
  border-radius: 6px !important;
}
[data-testid="stSidebar"] label {
  font-size: 0.7rem !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
  color: var(--muted) !important;
}

/* KPI CARDS */
[data-testid="stMetric"] {
  background: linear-gradient(135deg, #0f2040 0%, #0a1628 100%);
  border: 1px solid var(--border);
  border-bottom: 3px solid var(--gold);
  border-radius: 10px;
  padding: 20px 22px 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.45);
  transition: all 0.25s ease;
  position: relative;
  overflow: hidden;
}
[data-testid="stMetric"]::after {
  content: '';
  position: absolute;
  top: -20px; right: -20px;
  width: 80px; height: 80px;
  background: radial-gradient(circle, rgba(240,180,41,0.12), transparent 70%);
  border-radius: 50%;
}
[data-testid="stMetric"]:hover {
  box-shadow: 0 8px 32px rgba(0,0,0,0.5), 0 0 24px rgba(240,180,41,0.15);
  transform: translateY(-3px);
  border-bottom-color: #f5c842;
}
[data-testid="stMetricLabel"] {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.60rem !important;
  font-weight: 500 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.13em !important;
  color: var(--muted) !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Bebas Neue', sans-serif !important;
  font-size: 2rem !important;
  font-weight: 400 !important;
  color: #f0f6ff !important;
  letter-spacing: 1.5px !important;
  line-height: 1.1 !important;
}
[data-testid="stMetricDelta"] {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.72rem !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
  background: var(--navy2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 5px;
  gap: 4px;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 6px;
  color: var(--muted);
  font-family: 'Barlow', sans-serif;
  font-weight: 600;
  font-size: 0.83rem;
  letter-spacing: 0.02em;
  padding: 9px 22px;
  transition: all 0.2s;
}
.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
  background: var(--navy3) !important;
  color: var(--text) !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, #f0b429 0%, #f5c842 100%) !important;
  color: #050d1a !important;
  font-weight: 700 !important;
  box-shadow: 0 2px 14px rgba(240,180,41,0.4) !important;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}

/* DOWNLOAD BUTTON */
.stDownloadButton > button {
  background: linear-gradient(135deg, #f0b429, #f5c842) !important;
  color: #050d1a !important;
  font-family: 'Barlow', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.83rem !important;
  border: none !important;
  border-radius: 6px !important;
  padding: 9px 22px !important;
  box-shadow: 0 4px 14px rgba(240,180,41,0.3) !important;
  transition: all 0.2s !important;
  letter-spacing: 0.03em !important;
}
.stDownloadButton > button:hover {
  box-shadow: 0 6px 22px rgba(240,180,41,0.5) !important;
  transform: translateY(-2px) !important;
}

/* TEXT INPUT */
.stTextInput > div > div {
  background: var(--navy3) !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
  border-radius: 6px !important;
}

/* SCROLLBAR */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

hr { border-color: var(--border); opacity: 0.5; }

/* CUSTOM TYPOGRAPHY */
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
  font-size: 0.9rem;
  box-shadow: 0 2px 10px rgba(240,180,41,0.4);
}
.page-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 2.4rem;
  letter-spacing: 3px;
  color: #f0f6ff;
  line-height: 1;
  text-shadow: 0 0 40px rgba(240,180,41,0.1);
}
.page-meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.71rem;
  color: var(--muted);
  letter-spacing: 0.04em;
  margin-top: 6px;
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
.section-hdr .dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--gold);
  box-shadow: 0 0 8px var(--gold);
  flex-shrink: 0;
}
.badge-gold {
  display: inline-block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.63rem;
  padding: 3px 9px;
  border-radius: 20px;
  background: rgba(240,180,41,0.15);
  color: #f0b429;
  border: 1px solid rgba(240,180,41,0.3);
  margin-right: 5px;
}
.badge-cyan {
  display: inline-block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.63rem;
  padding: 3px 9px;
  border-radius: 20px;
  background: rgba(0,212,255,0.12);
  color: #00d4ff;
  border: 1px solid rgba(0,212,255,0.25);
}
.sidebar-info {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  color: var(--muted);
  line-height: 2.1;
}
</style>
""", unsafe_allow_html=True)

# ── COLOR CONSTANTS ────────────────────────────────────────────────────────────
GOLD    = "#f0b429"
CYAN    = "#00d4ff"
GREEN   = "#00e87a"
CORAL   = "#ff5757"
VIOLET  = "#a855f7"
AMBER   = "#fb923c"
TEAL    = "#22d3ee"
LIME    = "#84cc16"
PINK    = "#e879f9"
SILVER  = "#94a3b8"

NAVY2   = "#0a1628"
NAVY3   = "#0f2040"
BORDER  = "#1a3560"
MUTED   = "#4d6b8a"
TEXT    = "#dce8f5"

VIVID = [CYAN, GOLD, GREEN, CORAL, VIOLET, AMBER, TEAL, LIME, PINK, SILVER]

PLOTLY = dict(
    paper_bgcolor=NAVY2,
    plot_bgcolor=NAVY2,
    font=dict(family="Barlow", color=TEXT, size=12),
    xaxis=dict(gridcolor="#0e1f38", zerolinecolor="#0e1f38",
               tickfont=dict(color=MUTED, size=11), linecolor=BORDER),
    yaxis=dict(gridcolor="#0e1f38", zerolinecolor="#0e1f38",
               tickfont=dict(color=MUTED, size=11), linecolor=BORDER),
    legend=dict(bgcolor="rgba(5,13,26,0.9)", bordercolor=BORDER, borderwidth=1,
                font=dict(color="#7a9cbd", size=11)),
    margin=dict(l=16, r=16, t=40, b=16),
    hoverlabel=dict(bgcolor="#0f2040", bordercolor=BORDER,
                    font=dict(color=TEXT, size=12, family="Barlow")),
)

# ── LOAD DATA ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("ventes.xlsx")
    df.columns = df.columns.str.strip()
    df["Date"]     = pd.to_datetime(df["Date"].astype(str), format="%Y%m%d")
    df["Month"]    = df["Date"].dt.to_period("M").astype(str)
    df["YearWeek"] = df["Date"].dt.strftime("%Y-W%V")
    df["Cross Section Num"] = pd.to_numeric(df["Cross Section"], errors="coerce")
    return df

df = load_data()

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("COFICAB.png", width=170)
    st.markdown(
        '<p style="font-family:JetBrains Mono,monospace;font-size:0.67rem;'
        'color:#4d6b8a;margin:4px 0 18px;letter-spacing:0.05em;">ANALYSE DES VENTES · 2025</p>',
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown(
        '<p style="font-family:Barlow,sans-serif;font-weight:700;font-size:0.68rem;'
        'color:#4d6b8a;text-transform:uppercase;letter-spacing:0.14em;margin-bottom:12px;">'
        '⚙ Filtres</p>', unsafe_allow_html=True
    )

    entity   = st.selectbox("Entité",          ["Tous"] + sorted(df["Entities"].dropna().unique().tolist()))
    customer = st.selectbox("Client",           ["Tous"] + sorted(df["Customer"].dropna().unique().tolist()))
    family   = st.selectbox("Famille produit",  ["Tous"] + sorted(df["Family"].dropna().unique().tolist()))

    date_min   = df["Date"].min().date()
    date_max   = df["Date"].max().date()
    date_range = st.date_input("Période", value=(date_min, date_max),
                               min_value=date_min, max_value=date_max)
    st.markdown("---")
    st.markdown(
        f'<div class="sidebar-info">'
        f'📅 {date_min.strftime("%d %b")} → {date_max.strftime("%d %b %Y")}<br>'
        f'📦 {len(df):,} lignes totales<br>'
        f'👥 {df["Customer"].nunique()} clients<br>'
        f'🏭 {df["Entities"].nunique()} entités'
        f'</div>', unsafe_allow_html=True
    )

# ── FILTERS ────────────────────────────────────────────────────────────────────
fdf = df.copy()
if entity   != "Tous": fdf = fdf[fdf["Entities"] == entity]
if customer != "Tous": fdf = fdf[fdf["Customer"] == customer]
if family   != "Tous": fdf = fdf[fdf["Family"] == family]
if len(date_range) == 2:
    fdf = fdf[(fdf["Date"].dt.date >= date_range[0]) &
              (fdf["Date"].dt.date <= date_range[1])]

# ── PAGE HEADER ────────────────────────────────────────────────────────────────
col_logo, col_t, col_b = st.columns([1, 3, 1])
with col_logo:
    st.image("COFICAB.png", width=160)
with col_t:
    st.markdown('<div class="page-title">Analyse des Ventes</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="page-meta">'
        f'<span style="color:{GOLD}">{len(fdf):,} lignes</span> &nbsp;·&nbsp; '
        f'{date_range[0].strftime("%d %b %Y") if len(date_range)==2 else "—"}'
        f' → {date_range[1].strftime("%d %b %Y") if len(date_range)==2 else "—"}'
        f'</div>', unsafe_allow_html=True
    )
with col_b:
    st.markdown(
        '<div style="text-align:right;padding-top:16px;">'
        '<span class="badge-gold">● LIVE</span>'
        '</div>', unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "  ⚡  KPI & Tendances  ",
    "  👥  Clients  ",
    "  📦  Produits  ",
    "  🗃  Données brutes  ",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    total_amount = fdf["Amount"].sum()
    total_qty_m  = fdf["QTY M"].sum()
    total_qty_km = fdf["QTY KM"].sum()
    avg_lme      = fdf["LME"].mean()
    n_invoices   = fdf["Invoice"].nunique()
    n_customers  = fdf["Customer"].nunique()

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Chiffre d'affaires", f"{total_amount/1e6:.2f}M EUR")
    c2.metric("Quantité (m)",       f"{total_qty_m/1e3:.1f}K m")
    c3.metric("Quantité (km)",      f"{total_qty_km:.1f} km")
    c4.metric("LME moyen",          f"{avg_lme:.3f}")
    c5.metric("Factures",           f"{n_invoices:,}")
    c6.metric("Clients actifs",     f"{n_customers}")

    st.markdown("<br>", unsafe_allow_html=True)

    # CA MENSUEL
    st.markdown('<div class="section-hdr"><span class="dot"></span>CA MENSUEL & QUANTITÉ</div>', unsafe_allow_html=True)
    monthly = fdf.groupby("Month").agg(Amount=("Amount","sum"), QTY_M=("QTY M","sum")).reset_index()

    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(go.Bar(
        x=monthly["Month"], y=monthly["Amount"],
        name="CA (EUR)",
        marker=dict(
            color=monthly["Amount"],
            colorscale=[[0,"#0e1f38"],[0.5,"#1a4a8a"],[1, GOLD]],
            line=dict(width=0),
        ),
        hovertemplate="<b>%{x}</b><br>CA: %{y:,.0f} EUR<extra></extra>",
        opacity=0.93,
    ), secondary_y=False)
    fig1.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["QTY_M"],
        name="Qté (m)", mode="lines+markers",
        line=dict(color=CYAN, width=3),
        marker=dict(size=9, color=CYAN, symbol="circle",
                    line=dict(color=NAVY2, width=2.5)),
        hovertemplate="<b>%{x}</b><br>Qté: %{y:,.0f} m<extra></extra>",
    ), secondary_y=True)
    fig1.update_layout(**PLOTLY, height=320, bargap=0.28)
    fig1.update_yaxes(title_text="Montant EUR",
                      title_font=dict(color=GOLD, size=11), secondary_y=False)
    fig1.update_yaxes(title_text="Quantité (m)",
                      title_font=dict(color=CYAN, size=11), secondary_y=True)
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown('<div class="section-hdr"><span class="dot"></span>ÉVOLUTION HEBDOEURAIRE PAR ENTITÉ</div>', unsafe_allow_html=True)
        weekly = fdf.groupby(["YearWeek","Entities"])["Amount"].sum().reset_index()
        fig3 = px.line(
            weekly, x="YearWeek", y="Amount", color="Entities",
            color_discrete_sequence=[CYAN, GOLD],
            markers=True, line_shape="spline",
            labels={"Amount":"Montant (EUR)","YearWeek":"Semaine"},
        )
        fig3.update_traces(line_width=3, marker_size=7,
                           marker=dict(line=dict(color=NAVY2, width=2)))
        fig3.update_layout(**PLOTLY, height=280)
        st.plotly_chart(fig3, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-hdr"><span class="dot"></span>PART PAR ENTITÉ</div>', unsafe_allow_html=True)
        by_entity = fdf.groupby("Entities")["Amount"].sum().reset_index()
        fig2 = px.pie(
            by_entity, values="Amount", names="Entities",
            color_discrete_sequence=[CYAN, GOLD],
            hole=0.65,
        )
        fig2.update_traces(
            textinfo="percent+label",
            textfont=dict(color=TEXT, size=13, family="Barlow"),
            marker=dict(line=dict(color=NAVY2, width=4)),
            pull=[0.04]*len(by_entity),
        )
        fig2.add_annotation(
            text="CA<br>TOTAL", x=0.5, y=0.5,
            font=dict(color=TEXT, size=12, family="Bebas Neue"),
            showarrow=False
        )
        fig2.update_layout(**PLOTLY, height=280, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # LME
    st.markdown('<div class="section-hdr"><span class="dot"></span>INDICE LME HEBDOEURAIRE</div>', unsafe_allow_html=True)
    lme_weekly = fdf.groupby("YearWeek")["LME"].mean().reset_index()
    mean_lme   = lme_weekly["LME"].mean()
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=lme_weekly["YearWeek"], y=lme_weekly["LME"],
        fill="tozeroy", fillcolor="rgba(0,212,255,0.07)",
        line=dict(color=CYAN, width=2.5), mode="lines",
        hovertemplate="<b>%{x}</b><br>LME: %{y:.3f}<extra></extra>",
    ))
    fig4.add_hline(y=mean_lme, line_dash="dot",
                   line_color=GOLD, line_width=1.5,
                   annotation_text=f"  Moyenne: {mean_lme:.3f}",
                   annotation_font_color=GOLD, annotation_font_size=11)
    fig4.update_layout(**PLOTLY, height=230)
    st.plotly_chart(fig4, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    by_customer = fdf.groupby("Customer").agg(
        Montant=("Amount","sum"),
        QTY_M=("QTY M","sum"),
        QTY_KM=("QTY KM","sum"),
        Lignes=("Amount","count"),
        Factures=("Invoice","nunique"),
    ).reset_index().sort_values("Montant", ascending=False)

    st.markdown('<div class="section-hdr"><span class="dot"></span>CLASSEMENT DES CLIENTS PAR CA</div>', unsafe_allow_html=True)
    fig5 = px.bar(
        by_customer, x="Montant", y="Customer",
        orientation="h",
        color="Montant",
        color_continuous_scale=[[0,"#0e1f38"],[0.35,"#1a4a8a"],[1, GOLD]],
        labels={"Montant":"CA (EUR)","Customer":""},
        text=by_customer["Montant"].apply(lambda x: f"{x/1e6:.2f}M"),
    )
    fig5.update_traces(
        textposition="outside",
        textfont=dict(color=GOLD, size=12, family="JetBrains Mono"),
        marker=dict(line=dict(width=0)),
    )
    fig5.update_layout(**PLOTLY, height=420, coloraxis_showscale=False)
    fig5.update_yaxes(categoryorder="total ascending", gridcolor=BORDER)
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-hdr"><span class="dot"></span>PART DE MARCHÉ — QUANTITÉ (m)</div>', unsafe_allow_html=True)
        fig6 = px.pie(
            by_customer, values="QTY_M", names="Customer",
            color_discrete_sequence=VIVID, hole=0.58,
        )
        fig6.update_traces(
            textinfo="percent",
            textfont=dict(color=TEXT, size=12, family="Barlow"),
            marker=dict(line=dict(color=NAVY2, width=3)),
        )
        fig6.update_layout(**PLOTLY, height=360, showlegend=True)
        st.plotly_chart(fig6, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-hdr"><span class="dot"></span>ÉVOLUTION MENSUELLE PAR CLIENT</div>', unsafe_allow_html=True)
        cust_monthly = fdf.groupby(["Month","Customer"])["Amount"].sum().reset_index()
        fig7 = px.line(
            cust_monthly, x="Month", y="Amount", color="Customer",
            markers=True, line_shape="spline",
            labels={"Amount":"CA (EUR)","Month":"Mois"},
            color_discrete_sequence=VIVID,
        )
        fig7.update_traces(line_width=2.5, marker_size=6,
                           marker=dict(line=dict(color=NAVY2, width=1.5)))
        fig7.update_layout(**PLOTLY, height=360)
        st.plotly_chart(fig7, use_container_width=True)

    st.markdown('<div class="section-hdr"><span class="dot"></span>TABLEAU RÉCAPITULATIF</div>', unsafe_allow_html=True)
    disp = by_customer.copy()
    disp["Montant"] = disp["Montant"].map("{:,.0f} EUR".format)
    disp["QTY_M"]   = disp["QTY_M"].map("{:,.0f} m".format)
    disp["QTY_KM"]  = disp["QTY_KM"].map("{:,.1f} km".format)
    st.dataframe(
        disp.rename(columns={"Customer":"Client","QTY_M":"Qté (m)",
                             "QTY_KM":"Qté (km)","Lignes":"Nb lignes","Factures":"Nb factures"}),
        use_container_width=True, hide_index=True,
    )

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown('<div class="section-hdr"><span class="dot"></span>TOP 20 FAMILLES PRODUITS</div>', unsafe_allow_html=True)
        by_family = fdf.groupby("Family")["Amount"].sum().nlargest(20).reset_index()
        fig8 = px.bar(
            by_family, x="Amount", y="Family", orientation="h",
            color="Amount",
            color_continuous_scale=[[0,"#0a1f18"],[0.5,"#0e5c4a"],[1, GREEN]],
            labels={"Amount":"CA (EUR)","Family":""},
            text=by_family["Amount"].apply(lambda x: f"{x/1e3:.0f}K"),
        )
        fig8.update_traces(
            textposition="outside",
            textfont=dict(color=GREEN, size=11, family="JetBrains Mono"),
            marker=dict(line=dict(width=0)),
        )
        fig8.update_layout(**PLOTLY, height=530, coloraxis_showscale=False)
        fig8.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig8, use_container_width=True)

    with col_p2:
        st.markdown('<div class="section-hdr"><span class="dot"></span>DISTRIBUTION PAR SECTION (mm²)</div>', unsafe_allow_html=True)
        by_section = fdf.groupby("Cross Section").agg(
            Amount=("Amount","sum"), QTY_M=("QTY M","sum")
        ).reset_index().sort_values("Amount", ascending=False).head(20)
        fig9 = px.bar(
            by_section, x="Cross Section", y="Amount",
            color="QTY_M",
            color_continuous_scale=[[0,"#0e1f38"],[0.5,"#0e3d6e"],[1, CYAN]],
            labels={"Amount":"CA (EUR)","Cross Section":"Section (mm²)","QTY_M":"Qté (m)"},
        )
        fig9.update_layout(
            **PLOTLY, height=530,
            coloraxis_colorbar=dict(title="Qté (m)",
                                    title_font=dict(color=MUTED, size=11),
                                    tickfont=dict(color=MUTED, size=10))
        )
        st.plotly_chart(fig9, use_container_width=True)

    st.markdown('<div class="section-hdr"><span class="dot"></span>HEATMAP — FAMILLE × SECTION</div>', unsafe_allow_html=True)
    top_fam = fdf.groupby("Family")["Amount"].sum().nlargest(15).index.tolist()
    top_sec = fdf.groupby("Cross Section")["Amount"].sum().nlargest(10).index.tolist()
    heat_df = fdf[fdf["Family"].isin(top_fam) & fdf["Cross Section"].isin(top_sec)]
    pivot   = heat_df.pivot_table(values="Amount", index="Family",
                                  columns="Cross Section", aggfunc="sum", fill_value=0)
    fig10 = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale=[[0, NAVY3],[0.3,"#1a3a6e"],[0.7, CYAN],[1, GOLD]],
        hoverongaps=False,
        hovertemplate="<b>Section:</b> %{x}<br><b>Famille:</b> %{y}<br><b>CA:</b> %{z:,.0f} EUR<extra></extra>",
    ))
    fig10.update_layout(**PLOTLY, height=440,
                        xaxis_title="Section (mm²)", yaxis_title="Famille")
    st.plotly_chart(fig10, use_container_width=True)

    st.markdown('<div class="section-hdr"><span class="dot"></span>PRIX UNITAIRE — CU vs AV PAR CLIENT</div>', unsafe_allow_html=True)
    sample = fdf.sample(min(3000, len(fdf)), random_state=42)
    fig11 = px.scatter(
        sample, x="CU", y="AV", color="Customer", size="QTY M",
        size_max=20, opacity=0.78,
        color_discrete_sequence=VIVID,
        labels={"CU":"Prix CU","AV":"Prix AV","Customer":"Client"},
        hover_data=["Family","Cross Section"],
    )
    fig11.update_traces(marker=dict(line=dict(color=NAVY2, width=1)))
    fig11.update_layout(**PLOTLY, height=390)
    st.plotly_chart(fig11, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-hdr"><span class="dot"></span>DONNÉES BRUTES FILTRÉES</div>', unsafe_allow_html=True)
    st.markdown(
        f'<p style="font-family:JetBrains Mono,monospace;font-size:0.69rem;color:{MUTED};margin-top:-10px;margin-bottom:16px;">'
        f'{len(fdf):,} lignes · {len(fdf.columns)} colonnes</p>',
        unsafe_allow_html=True
    )

    search = st.text_input("🔍 Rechercher", placeholder="Famille, client, référence…")
    if search:
        mask = fdf.apply(lambda col: col.astype(str).str.contains(
            search, case=False, na=False)).any(axis=1)
        display_df = fdf[mask]
    else:
        display_df = fdf

    st.dataframe(
        display_df.drop(columns=["Month","YearWeek","Cross Section Num"], errors="ignore"),
        use_container_width=True, height=520,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col_dl, _ = st.columns([1, 5])
    with col_dl:
        csv = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Exporter CSV",
            data=csv, file_name="coficab_ventes.csv", mime="text/csv",
        )
