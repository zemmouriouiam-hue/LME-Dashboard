# Code complet Streamlit Dashboard Professionnel (EUR + Cross Section)

```python
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

# ── CSS DESIGN ────────────────────────────────────────────────────────────────

st.markdown("""
<style>

.stApp {
    background-color: #050d1a;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #0a1628;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0f2040 0%, #0a1628 100%);
    border: 1px solid #1a3560;
    border-radius: 12px;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)

# ── COLORS ───────────────────────────────────────────────────────────────────

GOLD = "#f0b429"
CYAN = "#00d4ff"
GREEN = "#00e87a"
CORAL = "#ff5757"
VIOLET = "#a855f7"

VIVID = [
    CYAN,
    GOLD,
    GREEN,
    CORAL,
    VIOLET
]

# ── LOAD DATA ────────────────────────────────────────────────────────────────

@st.cache_data
def load_data():

    df = pd.read_excel("ventes.xlsx")

    df.columns = df.columns.str.strip()

    # DATE
    df["Date"] = pd.to_datetime(
        df["Date"].astype(str),
        format="%Y%m%d"
    )

    # PERIODS
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["YearWeek"] = df["Date"].dt.strftime("%Y-W%V")

    # NUMERIC
    numeric_cols = [
        "Amount",
        "QTY M",
        "QTY KM",
        "LME",
        "CU",
        "AV"
    ]

    for col in numeric_cols:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # EUR CONVERSION
    EUR_RATE = 10.8

    df["Amount_EUR"] = df["Amount"] / EUR_RATE
    df["CU_EUR"] = df["CU"] / EUR_RATE
    df["AV_EUR"] = df["AV"] / EUR_RATE

    return df


df = load_data()

# ── SIDEBAR ──────────────────────────────────────────────────────────────────

with st.sidebar:

    st.title("⚡ COFICAB")

    st.markdown("### Dashboard Analytics")

    entity = st.selectbox(
        "Entity",
        ["Tous"] + sorted(
            df["Entities"].dropna().unique().tolist()
        )
    )

    customer = st.selectbox(
        "Customer",
        ["Tous"] + sorted(
            df["Customer"].dropna().unique().tolist()
        )
    )

    family = st.selectbox(
        "Family",
        ["Tous"] + sorted(
            df["Family"].dropna().unique().tolist()
        )
    )

    cross_section = st.selectbox(
        "Cross Section",
        ["Tous"] + sorted(
            df["Cross Section"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )

    date_min = df["Date"].min().date()
    date_max = df["Date"].max().date()

    date_range = st.date_input(
        "Date Range",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max
    )

# ── FILTERS ──────────────────────────────────────────────────────────────────

fdf = df.copy()

if entity != "Tous":
    fdf = fdf[fdf["Entities"] == entity]

if customer != "Tous":
    fdf = fdf[fdf["Customer"] == customer]

if family != "Tous":
    fdf = fdf[fdf["Family"] == family]

if cross_section != "Tous":
    fdf = fdf[
        fdf["Cross Section"].astype(str) == cross_section
    ]

if len(date_range) == 2:

    fdf = fdf[
        (fdf["Date"].dt.date >= date_range[0]) &
        (fdf["Date"].dt.date <= date_range[1])
    ]

# ── HEADER ───────────────────────────────────────────────────────────────────

st.title("📊 Executive Sales Dashboard")

st.markdown("Professional Business Intelligence Analytics")

# ── KPI ──────────────────────────────────────────────────────────────────────

st.markdown("---")

ca_total = fdf["Amount_EUR"].sum()
qty_m = fdf["QTY M"].sum()
qty_km = fdf["QTY KM"].sum()
qty_avg = fdf["QTY M"].mean()
lme_avg = fdf["LME"].mean()
customers = fdf["Customer"].nunique()
invoices = fdf["Invoice"].nunique()

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

c1.metric(
    "CA Total",
    f"{ca_total/1e6:.2f}M EUR"
)

c2.metric(
    "Quantité m",
    f"{qty_m/1e3:.1f}K"
)

c3.metric(
    "Quantité km",
    f"{qty_km:.1f}"
)

c4.metric(
    "Qté Moyenne",
    f"{qty_avg:,.0f}"
)

c5.metric(
    "LME Moyen",
    f"{lme_avg:.2f}"
)

c6.metric(
    "Factures",
    invoices
)

c7.metric(
    "Clients",
    customers
)

st.markdown("---")

# ── TABS ─────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tendances",
    "👥 Clients",
    "📦 Produits",
    "📋 Données"
])

# ── TAB 1 ────────────────────────────────────────────────────────────────────

with tab1:

    monthly = (
        fdf
        .groupby("Month")
        .agg(
            Amount_EUR=("Amount_EUR", "sum"),
            QTY_M=("QTY M", "sum")
        )
        .reset_index()
    )

    fig1 = make_subplots(specs=[[{"secondary_y": True}]])

    fig1.add_trace(
        go.Bar(
            x=monthly["Month"],
            y=monthly["Amount_EUR"],
            name="CA EUR",
            marker_color=GOLD
        ),
        secondary_y=False
    )

    fig1.add_trace(
        go.Scatter(
            x=monthly["Month"],
            y=monthly["QTY_M"],
            name="QTY M",
            mode="lines+markers",
            line=dict(color=CYAN, width=3)
        ),
        secondary_y=True
    )

    fig1.update_layout(
        height=400,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    by_entity = (
        fdf
        .groupby("Entities")["Amount_EUR"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        by_entity,
        values="Amount_EUR",
        names="Entities",
        hole=0.5,
        color_discrete_sequence=VIVID
    )

    fig2.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ── TAB 2 ────────────────────────────────────────────────────────────────────

with tab2:

    by_customer = (
        fdf
        .groupby("Customer")
        .agg(
            Montant=("Amount_EUR", "sum"),
            QTY_M=("QTY M", "sum"),
            QTY_KM=("QTY KM", "sum")
        )
        .reset_index()
        .sort_values("Montant", ascending=False)
    )

    fig3 = px.bar(
        by_customer,
        x="Montant",
        y="Customer",
        orientation="h",
        color="Montant",
        color_continuous_scale="Blues"
    )

    fig3.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.dataframe(
        by_customer,
        use_container_width=True
    )

# ── TAB 3 ────────────────────────────────────────────────────────────────────

with tab3:

    by_family = (
        fdf
        .groupby("Family")["Amount_EUR"]
        .sum()
        .nlargest(20)
        .reset_index()
    )

    fig4 = px.bar(
        by_family,
        x="Amount_EUR",
        y="Family",
        orientation="h",
        color="Amount_EUR",
        color_continuous_scale="Viridis"
    )

    fig4.update_layout(
        template="plotly_dark",
        height=600
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    sample = fdf.sample(
        min(3000, len(fdf)),
        random_state=42
    )

    fig5 = px.scatter(
        sample,
        x="CU_EUR",
        y="AV_EUR",
        color="Customer",
        size="QTY M",
        hover_data=[
            "Family",
            "Cross Section"
        ]
    )

    fig5.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

# ── TAB 4 ────────────────────────────────────────────────────────────────────

with tab4:

    search = st.text_input(
        "🔍 Rechercher"
    )

    if search:

        mask = fdf.apply(
            lambda col:
            col.astype(str)
            .str.contains(search, case=False, na=False)
        ).any(axis=1)

        display_df = fdf[mask]

    else:

        display_df = fdf

    st.dataframe(
        display_df,
        use_container_width=True,
        height=600
    )

    csv = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Export CSV",
        data=csv,
        file_name="coficab_dashboard.csv",
        mime="text/csv"
    )
```

## requirements.txt

```txt
streamlit
pandas
plotly
openpyxl
```

