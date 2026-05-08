import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="COFICAB Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stMetric"] {
    background-color: #1F2937;
    border: 1px solid #374151;
    padding: 15px;
    border-radius: 12px;
}

h1, h2, h3 {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_excel("ventes.xlsx")

    # clean columns
    df.columns = df.columns.str.strip()

    # numeric columns
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

    # date
    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(
            df["Date"].astype(str),
            errors="coerce"
        )

    # EUR conversion
    EUR_RATE = 10.8

    if "Amount" in df.columns:
        df["Amount_EUR"] = df["Amount"] / EUR_RATE

    if "CU" in df.columns:
        df["CU_EUR"] = df["CU"] / EUR_RATE

    if "AV" in df.columns:
        df["AV_EUR"] = df["AV"] / EUR_RATE

    return df


df = load_data()

# =========================================================
# TITLE
# =========================================================

st.title("📊 COFICAB Executive Dashboard")

st.markdown("Interactive Sales Analytics")

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.title("Filters")

filtered_df = df.copy()

# ENTITY
if "Entities" in df.columns:

    entity = st.sidebar.selectbox(
        "Entity",
        ["All"] + sorted(
            df["Entities"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    if entity != "All":

        filtered_df = filtered_df[
            filtered_df["Entities"] == entity
        ]

# CUSTOMER
if "Customer" in df.columns:

    customer = st.sidebar.selectbox(
        "Customer",
        ["All"] + sorted(
            df["Customer"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    if customer != "All":

        filtered_df = filtered_df[
            filtered_df["Customer"] == customer
        ]

# FAMILY
if "Family" in df.columns:

    family = st.sidebar.selectbox(
        "Family",
        ["All"] + sorted(
            df["Family"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    if family != "All":

        filtered_df = filtered_df[
            filtered_df["Family"] == family
        ]

# CROSS SECTION
if "Cross Section" in df.columns:

    cross = st.sidebar.selectbox(
        "Cross Section",
        ["All"] + sorted(
            filtered_df["Cross Section"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )

    if cross != "All":

        filtered_df = filtered_df[
            filtered_df["Cross Section"]
            .astype(str) == cross
        ]

# =========================================================
# KPI
# =========================================================

st.markdown("---")

sales = 0
qty_m = 0
qty_km = 0
avg_qty = 0
customers = 0

if "Amount_EUR" in filtered_df.columns:
    sales = filtered_df["Amount_EUR"].sum()

if "QTY M" in filtered_df.columns:
    qty_m = filtered_df["QTY M"].sum()
    avg_qty = filtered_df["QTY M"].mean()

if "QTY KM" in filtered_df.columns:
    qty_km = filtered_df["QTY KM"].sum()

if "Customer" in filtered_df.columns:
    customers = filtered_df["Customer"].nunique()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Sales EUR",
    f"{sales:,.0f} €"
)

c2.metric(
    "Quantity M",
    f"{qty_m:,.0f}"
)

c3.metric(
    "Quantity KM",
    f"{qty_km:,.1f}"
)

c4.metric(
    "Average Qty",
    f"{avg_qty:,.0f}"
)

c5.metric(
    "Customers",
    customers
)

st.markdown("---")

# =========================================================
# SALES BY CUSTOMER
# =========================================================

if "Customer" in filtered_df.columns and "Amount_EUR" in filtered_df.columns:

    st.subheader("💰 Sales by Customer")

    customer_sales = (
        filtered_df
        .groupby("Customer")["Amount_EUR"]
        .sum()
        .reset_index()
        .sort_values("Amount_EUR", ascending=False)
    )

    fig1 = px.bar(
        customer_sales,
        x="Customer",
        y="Amount_EUR",
        color="Amount_EUR",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# =========================================================
# SALES EVOLUTION
# =========================================================

if "Date" in filtered_df.columns and "Amount_EUR" in filtered_df.columns:

    st.subheader("📈 Sales Evolution")

    sales_date = (
        filtered_df
        .groupby("Date")["Amount_EUR"]
        .sum()
        .reset_index()
    )

    fig2 = px.line(
        sales_date,
        x="Date",
        y="Amount_EUR",
        markers=True,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =========================================================
# FAMILY ANALYSIS
# =========================================================

if "Family" in filtered_df.columns and "Amount_EUR" in filtered_df.columns:

    st.subheader("🏭 Family Distribution")

    family_sales = (
        filtered_df
        .groupby("Family")["Amount_EUR"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        family_sales,
        names="Family",
        values="Amount_EUR",
        hole=0.5,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# =========================================================
# SCATTER
# =========================================================

if "CU_EUR" in filtered_df.columns and "AV_EUR" in filtered_df.columns:

    st.subheader("📊 CU vs AV")

    sample = filtered_df.sample(
        min(2000, len(filtered_df)),
        random_state=1
    )

    fig4 = px.scatter(
        sample,
        x="CU_EUR",
        y="AV_EUR",
        color="Customer" if "Customer" in sample.columns else None,
        size="QTY M" if "QTY M" in sample.columns else None,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# =========================================================
# TABLE
# =========================================================

st.subheader("📋 Detailed Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500
)

# =========================================================
# DOWNLOAD
# =========================================================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download CSV",
    csv,
    "dashboard_export.csv",
    "text/csv"
)
