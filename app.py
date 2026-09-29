import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Dashboard page setup
st.set_page_config(page_title="Pharmeasy Operational Metrics", layout="wide")

# Connect to local SQLite database (zero external API keys or network access needed)
conn = sqlite3.connect("pharmeasy.db")
df_orders = pd.read_sql_query("SELECT * FROM orders_clean", conn)
df_regions = pd.read_sql_query("SELECT region FROM regions_master", conn)
conn.close()

# Format order_date and extract month
df_orders["order_date"] = pd.to_datetime(df_orders["order_date"])
df_orders["month"] = df_orders["order_date"].dt.strftime("%Y-%m")

# -------------------------------------------------------------
# Task 4.2: Embedded Executive Summary (3-5 sentences)
# -------------------------------------------------------------
st.title("Pharmeasy Regional Sales & Performance Dashboard")

total_sales_val = df_orders["sales_inr"].sum()
total_profit_val = df_orders["profit_inr"].sum()
distinct_orders_val = df_orders["order_id"].nunique()

st.markdown(f"""
> ### Executive Summary
> **Across Q2 2026, the retail network generated total sales of INR {total_sales_val:,.2f} with total profit of INR {total_profit_val:,.2f} across {distinct_orders_val:,} verified orders.**
> While baseline performance stabilized across southern territories into June, Guntur surged by +122.19% from April to May, driving exceptional order volume expansion.
> Regional supply chain managers must immediately prioritize buffer inventory allocation toward Guntur to prevent stockouts while monitoring post-surge demand stability.
""")

st.markdown("---")

# -------------------------------------------------------------
# Task 4.1: Interactive Region Filter (st.selectbox)
# -------------------------------------------------------------
canonical_regions = ["All Regions"] + sorted(df_regions["region"].unique().tolist())
selected_region = st.selectbox("Select Regional Focus (Connects all three levels):", canonical_regions)

# Dynamic dataframe filtering connected to all 3 levels
filtered_df = df_orders if selected_region == "All Regions" else df_orders[df_orders["region"] == selected_region]

# -------------------------------------------------------------
# Level 1: Overview KPIs (Using DISTINCT order_id count)
# -------------------------------------------------------------
st.subheader("Level 1: Network Overview KPIs")
kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric("Total Sales (INR)", f"₹{filtered_df['sales_inr'].sum():,.2f}")
kpi2.metric("Total Profit (INR)", f"₹{filtered_df['profit_inr'].sum():,.2f}")
# Explicit distinct count of order_id as strictly mandated by acceptance criteria
kpi3.metric("Total Order Count (Distinct)", f"{filtered_df['order_id'].nunique():,}")

st.markdown("---")

# -------------------------------------------------------------
# Level 2: Category Breakdown & Visualizations
# -------------------------------------------------------------
st.subheader("Level 2: Category Breakdown & Visualizations")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # 1. Trend line chart: Sales by region across April, May, June
    monthly_trend = filtered_df.groupby("month", as_index=False)["sales_inr"].sum()
    fig_line = px.line(
        monthly_trend,
        x="month",
        y="sales_inr",
        markers=True,
        title="What is the monthly sales trend across Q2 2026? (INR)"
    )
    fig_line.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig_line, use_container_width=True)

with chart_col2:
    # 2. Comparison bar chart: Total sales by region with Guntur highlighted
    region_sales = df_orders.groupby("region", as_index=False)["sales_inr"].sum()
    region_sales["flag_color"] = region_sales["region"].apply(
        lambda r: "Flagged (+122.19% Surge)" if r == "Guntur" else "Normal Region"
    )
    fig_bar = px.bar(
        region_sales,
        x="region",
        y="sales_inr",
        color="flag_color",
        color_discrete_map={"Flagged (+122.19% Surge)": "#E45756", "Normal Region": "#4C78A8"},
        title="What are total sales by region across the network? (INR)"
    )
    fig_bar.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig_bar, use_container_width=True)

# 3. Part-of-whole donut chart: Sales share by category (exactly 6 categories)
cat_sales = filtered_df.groupby("category", as_index=False)["sales_inr"].sum()
fig_donut = px.pie(
    cat_sales,
    names="category",
    values="sales_inr",
    hole=0.45,
    title="What is the sales share by category? (%)"
)
st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------
# Level 3: Detail Level (Per-region, per-month data table)
# -------------------------------------------------------------
st.subheader("Level 3: Per-Region Per-Month Detail Table")
detail_df = filtered_df.groupby(["region", "month"], as_index=False).agg(
    total_sales=("sales_inr", "sum"),
    total_profit=("profit_inr", "sum"),
    distinct_orders=("order_id", "nunique")
)
st.dataframe(detail_df, use_container_width=True)
