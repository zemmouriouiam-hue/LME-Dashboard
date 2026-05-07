import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("📊 Interactive Sales Dashboard")
st.markdown("Professional Sales Analysis Dashboard")

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    df = pd.read_excel("ventes.xlsx")

    # Convert date column
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    # Numeric columns
    numeric_columns = [
        "QTY M",
        "QTY KM",
        "Amount ",
        "LME",
        "CU",
        "AV"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # Margin calculation
    if "Amount " in df.columns:
        df["Estimated Margin"] = df["Amount "] * 0.03

    return df


df = load_data()

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("🔎 Filters")

# Entity filter
if "Entities" in df.columns:

    entity_filter = st.sidebar.multiselect(
        "Entities",
        options=df["Entities"].dropna().unique(),
        default=df["Entities"].dropna().unique()
    )

else:
    entity_filter = []

# Customer filter
if "Customer" in df.columns:

    customer_filter = st.sidebar.multiselect(
        "Customer",
        options=df["Customer"].dropna().unique(),
        default=df["Customer"].dropna().unique()
    )

else:
    customer_filter = []

# Family filter
if "Family" in df.columns:

    family_filter = st.sidebar.multiselect(
        "Family",
        options=df["Family"].dropna().unique(),
        default=df["Family"].dropna().unique()
    )

else:
    family_filter = []

# =====================================================
# APPLY FILTERS
# =====================================================

filtered_df = df.copy()

if "Entities" in df.columns and len(entity_filter) > 0:
    filtered_df = filtered_df[
        filtered_df["Entities"].isin(entity_filter)
    ]

if "Customer" in df.columns and len(customer_filter) > 0:
    filtered_df = filtered_df[
        filtered_df["Customer"].isin(customer_filter)
    ]

if "Family" in df.columns and len(family_filter) > 0:
    filtered_df = filtered_df[
        filtered_df["Family"].isin(family_filter)
    ]

# =====================================================
# KPI SECTION
# =====================================================

st.subheader("📌 Key Indicators")

col1, col2, col3, col4 = st.columns(4)

# Total Sales
with col1:

    total_sales = 0

    if "Amount " in filtered_df.columns:
        total_sales = filtered_df["Amount "].sum()

    st.metric(
        "Total Sales",
        f"{total_sales:,.2f} €"
    )

# Quantity
with col2:

    total_qty = 0

    if "QTY KM" in filtered_df.columns:
        total_qty = filtered_df["QTY KM"].sum()

    st.metric(
        "Total Quantity KM",
        f"{total_qty:,.2f}"
    )

# Margin
with col3:

    total_margin = 0

    if "Estimated Margin" in filtered_df.columns:
        total_margin = filtered_df["Estimated Margin"].sum()

    st.metric(
        "Estimated Margin",
        f"{total_margin:,.2f} €"
    )

# Customers
with col4:

    total_customers = 0

    if "Customer" in filtered_df.columns:
        total_customers = filtered_df["Customer"].nunique()

    st.metric(
        "Customers",
        total_customers
    )

# =====================================================
# SALES BY CUSTOMER
# =====================================================

if "Customer" in filtered_df.columns and "Amount " in filtered_df.columns:

    st.subheader("💰 Sales by Customer")

    sales_customer = (
        filtered_df
        .groupby("Customer", as_index=False)["Amount "]
        .sum()
        .sort_values(by="Amount ", ascending=False)
    )

    fig_customer = px.bar(
        sales_customer,
        x="Customer",
        y="Amount ",
        title="Sales by Customer",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_customer,
        use_container_width=True
    )

# =====================================================
# SALES EVOLUTION
# =====================================================

if "Date" in filtered_df.columns and "Amount " in filtered_df.columns:

    st.subheader("📈 Sales Evolution")

    sales_date = (
        filtered_df
        .groupby("Date", as_index=False)["Amount "]
        .sum()
    )

    fig_date = px.line(
        sales_date,
        x="Date",
        y="Amount ",
        title="Sales Evolution",
        markers=True
    )

    st.plotly_chart(
        fig_date,
        use_container_width=True
    )

# =====================================================
# FAMILY ANALYSIS
# =====================================================

if "Family" in filtered_df.columns and "Amount " in filtered_df.columns:

    st.subheader("🏭 Family Analysis")

    family_sales = (
        filtered_df
        .groupby("Family", as_index=False)["Amount "]
        .sum()
    )

    fig_family = px.pie(
        family_sales,
        names="Family",
        values="Amount ",
        title="Sales Distribution by Family"
    )

    st.plotly_chart(
        fig_family,
        use_container_width=True
    )

# =====================================================
# TOP ITEMS
# =====================================================

if "ITEMS" in filtered_df.columns and "Amount " in filtered_df.columns:

    st.subheader("🏆 Top Selling Items")

    items_sales = (
        filtered_df
        .groupby("ITEMS", as_index=False)["Amount "]
        .sum()
        .sort_values(by="Amount ", ascending=False)
        .head(10)
    )

    fig_items = px.bar(
        items_sales,
        x="ITEMS",
        y="Amount ",
        title="Top 10 Items",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_items,
        use_container_width=True
    )

# =====================================================
# DATA TABLE
# =====================================================

st.subheader("📋 Detailed Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# =====================================================
# DOWNLOAD BUTTON
# =====================================================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv")
