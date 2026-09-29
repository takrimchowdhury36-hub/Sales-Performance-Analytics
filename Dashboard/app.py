import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page settings
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Performance Dashboard")
st.caption("Interactive retail sales analytics")

# Load dataset
@st.cache_data
def load_data():
    file_path = (
        Path(__file__).resolve().parent.parent
        / "Dataset"
        / "sample_-_superstore.xls"
    )
    data = pd.read_excel(file_path, sheet_name="Orders")
    data["Order Date"] = pd.to_datetime(data["Order Date"])
    return data

df = load_data()

# Sidebar filters
st.sidebar.header("Dashboard Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

filtered_df = df[
    df["Region"].isin(regions)
    & df["Category"].isin(categories)
].copy()

if filtered_df.empty:
    st.warning("No data matches your filters.")
    st.stop()

# Calculate KPIs
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
profit_margin = total_profit / total_sales * 100

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Profit Margin", f"{profit_margin:.2f}%")
col4.metric("Total Orders", f"{total_orders:,}")

# Regional sales
st.subheader("Regional Sales Performance")

regional = (
    filtered_df.groupby("Region", as_index=False)["Sales"]
    .sum()
)

fig_region = px.bar(
    regional,
    x="Region",
    y="Sales",
    color="Region",
    title="Total Sales by Region"
)

st.plotly_chart(fig_region, use_container_width=True)

# Monthly sales
st.subheader("Monthly Sales Trend")

monthly = (
    filtered_df
    .set_index("Order Date")
    .resample("MS")["Sales"]
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Revenue"
)

st.plotly_chart(fig_monthly, use_container_width=True)

# Category performance
st.subheader("Product Category Performance")

category = (
    filtered_df.groupby("Category", as_index=False)
    [["Sales", "Profit"]]
    .sum()
)

fig_category = px.bar(
    category,
    x="Category",
    y=["Sales", "Profit"],
    barmode="group",
    title="Sales and Profit by Category"
)

st.plotly_chart(fig_category, use_container_width=True)

# Top products
st.subheader("Top 10 Products")

top_products = (
    filtered_df.groupby("Product Name", as_index=False)
    ["Sales"]
    .sum()
    .nlargest(10, "Sales")
    .sort_values("Sales")
)

fig_products = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Revenue"
)

st.plotly_chart(fig_products, use_container_width=True)

st.caption("Sales Performance Analytics | Python & Streamlit")
