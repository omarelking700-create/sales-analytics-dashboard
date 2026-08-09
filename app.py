import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="EL-King Omar | Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# =========================
# HEADER
# =========================

st.title("👑 EL-King Omar | Sales Analytics")
st.subheader("Professional Business Intelligence Dashboard")
st.caption(
    "Transforming Excel & CSV data into clear business insights."
)

# =========================
# UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "📂 Upload your Excel or CSV file",
    type=["xlsx", "xls", "csv"]
)

if uploaded_file:

    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Prepare data
    df["Date"] = pd.to_datetime(df["Date"])

    df["Sales"] = df["Quantity"] * df["Price"]

    df["Total Cost"] = df["Quantity"] * df["Cost"]

    df["Profit"] = df["Sales"] - df["Total Cost"]

    df["Profit Margin"] = (
        df["Profit"] / df["Sales"] * 100
    )

    # =========================
    # SIDEBAR
    # =========================

    st.sidebar.title("🔎 Filters")

    products = st.sidebar.multiselect(
        "Products",
        df["Product"].unique(),
        default=list(df["Product"].unique())
    )

    categories = st.sidebar.multiselect(
        "Categories",
        df["Category"].unique(),
        default=list(df["Category"].unique())
    )

    filtered_df = df[
        (df["Product"].isin(products)) &
        (df["Category"].isin(categories))
    ]

    # =========================
    # KPIs
    # =========================

    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_quantity = filtered_df["Quantity"].sum()

    if not filtered_df.empty:
        average_margin = filtered_df["Profit Margin"].mean()
    else:
        average_margin = 0

    st.divider()

    st.subheader("📊 Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Total Sales",
        f"${total_sales:,.2f}"
    )

    col2.metric(
        "📈 Total Profit",
        f"${total_profit:,.2f}"
    )

    col3.metric(
        "📦 Units Sold",
        f"{total_quantity:,}"
    )

    col4.metric(
        "📊 Profit Margin",
        f"{average_margin:.2f}%"
    )

    st.divider()

    # =========================
    # SALES BY PRODUCT
    # =========================

    product_sales = (
        filtered_df
        .groupby("Product")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    st.subheader("💰 Sales by Product")

    fig_sales = px.bar(
        product_sales,
        x="Product",
        y="Sales",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_sales,
        use_container_width=True
    )

    # =========================
    # PROFIT BY PRODUCT
    # =========================

    product_profit = (
        filtered_df
        .groupby("Product")["Profit"]
        .sum()
        .reset_index()
        .sort_values("Profit", ascending=False)
    )

    st.subheader("📈 Profit by Product")

    fig_profit = px.bar(
        product_profit,
        x="Product",
        y="Profit",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )

    # =========================
    # SALES OVER TIME
    # =========================

    daily_sales = (
        filtered_df
        .groupby("Date")["Sales"]
        .sum()
        .reset_index()
    )

    st.subheader("📅 Sales Over Time")

    fig_time = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        markers=True
    )

    st.plotly_chart(
        fig_time,
        use_container_width=True
    )

    # =========================
    # BUSINESS INSIGHTS
    # =========================

    st.subheader("🧠 Business Insights")

    if not product_sales.empty:

        best_product = product_sales.iloc[0]["Product"]
        worst_product = product_sales.iloc[-1]["Product"]

        best_sales = product_sales.iloc[0]["Sales"]

        st.success(
            f"🏆 Best-selling product: {best_product} "
            f"with ${best_sales:,.2f} in sales."
        )

        st.warning(
            f"⚠️ Lowest-selling product: {worst_product}."
        )

        st.info(
            f"💡 Your total profit is "
            f"${total_profit:,.2f}."
        )

    # =========================
    # DATA
    # =========================

    st.subheader("📋 Detailed Data")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    # =========================
    # DOWNLOAD
    # =========================

    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Analysis",
        csv,
        "sales_analysis.csv",
        "text/csv"
    )

else:

    st.info(
        "👆 Upload an Excel or CSV file to start."
    )