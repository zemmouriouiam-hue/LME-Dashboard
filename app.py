import streamlit as st
    .sum()
    .sort_values(by="Amount ", ascending=False)
)

fig_family = px.pie(
    family_sales,
    names="Family",
    values="Amount ",
    title="Sales Distribution by Family"
)

st.plotly_chart(fig_family, use_container_width=True)

# ==================================================
# TOP ITEMS
# ==================================================

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
    text_auto='.2s',
    title="Top 10 Items"
)

st.plotly_chart(fig_items, use_container_width=True)

# ==================================================
# DETAILED TABLE
# ==================================================

st.subheader("📋 Detailed Data")

st.dataframe(filtered_df, use_container_width=True)

# ==================================================
# DOWNLOAD BUTTON
# ==================================================

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name='filtered_sales_data.csv',
    mime='text/csv')
