import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="OMARX Analytics",
    page_icon="👑",
    layout="wide"
)

# =========================
# HEADER
# =========================

st.title("👑 OMARX Analytics | Sales Analytics")

st.subheader(
    "Professional Business Intelligence Dashboard"
)

st.caption(
    "Transforming Excel & CSV data into clear business insights."
)

st.divider()

# =========================
# DEMO DATA
# =========================

def create_demo_data():

    data = {
        "Date": [
            "2026-08-01",
            "2026-08-02",
            "2026-08-03",
            "2026-08-04",
            "2026-08-05",
            "2026-08-06",
            "2026-08-07",
            "2026-08-08",
            "2026-08-09",
            "2026-08-10"
        ],

        "Product": [
            "Laptop",
            "Smartphone",
            "Laptop",
            "Headphones",
            "Tablet",
            "Smartphone",
            "Laptop",
            "Smartwatch",
            "Tablet",
            "Headphones"
        ],

        "Category": [
            "Electronics",
            "Electronics",
            "Electronics",
            "Accessories",
            "Electronics",
            "Electronics",
            "Electronics",
            "Accessories",
            "Electronics",
            "Accessories"
        ],

        "Quantity": [
            5,
            10,
            3,
            20,
            7,
            8,
            6,
            12,
            5,
            18
        ],

        "Price": [
            1000,
            600,
            1000,
            100,
            400,
            600,
            1000,
            250,
            400,
            100
        ],

        "Cost": [
            750,
            450,
            700,
            60,
            280,
            450,
            750,
            170,
            280,
            60
        ]
    }

    df = pd.DataFrame(data)

    df["Date"] = pd.to_datetime(df["Date"])

    return df


# =========================
# SIDEBAR
# =========================

st.sidebar.title("👑 OMARX Analytics")

st.sidebar.subheader("Choose your data")

demo_button = st.sidebar.button(
    "🚀 Try Demo Dashboard",
    use_container_width=True
)

uploaded_file = st.sidebar.file_uploader(
    "📂 Upload your Excel or CSV file",
    type=["xlsx", "xls", "csv"]
)

# =========================
# SELECT DATA
# =========================

if uploaded_file is not None:

    try:

        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

        st.success(
            f"✅ File uploaded: {uploaded_file.name}"
        )

    except Exception as e:

        st.error(
            f"❌ Error reading the file: {e}"
        )

        st.stop()

elif demo_button:

    df = create_demo_data()

    st.success(
        "🚀 Demo Dashboard is running with sample data."
    )

else:

    st.info(
        "👈 Upload an Excel/CSV file or click "
        "**🚀 Try Demo Dashboard** from the sidebar."
    )

    st.markdown("""
    ## 📊 What OMARX Analytics can do

    - 💰 Calculate total sales
    - 📈 Calculate total profit
    - 🏆 Find the best-selling product
    - ⚠️ Find the lowest-selling product
    - 📊 Create professional charts
    - 🧠 Generate business insights
    - 📥 Download analyzed data
    """)

    st.stop()


# =========================
# CLEAN COLUMN NAMES
# =========================

df.columns = [
    str(column).strip()
    for column in df.columns
]


# =========================
# CHECK REQUIRED COLUMNS
# =========================

required_columns = [
    "Product",
    "Quantity",
    "Price",
    "Cost"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(
        "❌ Missing columns: "
        + ", ".join(missing_columns)
    )

    st.info("""
    Your file must contain:

    Product
    Quantity
    Price
    Cost

    Date and Category are recommended.
    """)

    st.stop()


# =========================
# OPTIONAL COLUMNS
# =========================

if "Category" not in df.columns:

    df["Category"] = "General"


if "Date" not in df.columns:

    df["Date"] = pd.Timestamp.today()


# =========================
# CONVERT DATA TYPES
# =========================

df["Quantity"] = pd.to_numeric(
    df["Quantity"],
    errors="coerce"
)

df["Price"] = pd.to_numeric(
    df["Price"],
    errors="coerce"
)

df["Cost"] = pd.to_numeric(
    df["Cost"],
    errors="coerce"
)

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)


df = df.dropna(
    subset=[
        "Product",
        "Quantity",
        "Price",
        "Cost"
    ]
)


# =========================
# CALCULATIONS
# =========================

df["Sales"] = (
    df["Quantity"] * df["Price"]
)

df["Total Cost"] = (
    df["Quantity"] * df["Cost"]
)

df["Profit"] = (
    df["Sales"] - df["Total Cost"]
)

df["Profit Margin"] = 0.0

df.loc[
    df["Sales"] != 0,
    "Profit Margin"
] = (
    df.loc[df["Sales"] != 0, "Profit"]
    /
    df.loc[df["Sales"] != 0, "Sales"]
    * 100
)


# =========================
# FILTERS
# =========================

st.sidebar.divider()

st.sidebar.header("🔎 Filters")

products = sorted(
    df["Product"].dropna().unique()
)

selected_products = st.sidebar.multiselect(
    "Products",
    products,
    default=products
)

categories = sorted(
    df["Category"].dropna().unique()
)

selected_categories = st.sidebar.multiselect(
    "Categories",
    categories,
    default=categories
)


filtered_df = df[
    (df["Product"].isin(selected_products))
    &
    (df["Category"].isin(selected_categories))
].copy()


if filtered_df.empty:

    st.warning(
        "⚠️ No data matches the selected filters."
    )

    st.stop()


# =========================
# KPI CALCULATIONS
# =========================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_quantity = filtered_df["Quantity"].sum()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)


# =========================
# BUSINESS OVERVIEW
# =========================

st.header("📊 Business Overview")

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
    f"{total_quantity:,.0f}"
)

col4.metric(
    "📊 Profit Margin",
    f"{profit_margin:.2f}%"
)


st.divider()


# =========================
# PRODUCT SALES
# =========================

product_sales = (
    filtered_df
    .groupby("Product")["Sales"]
    .sum()
    .reset_index()
    .sort_values(
        "Sales",
        ascending=False
    )
)


st.header("💰 Sales by Product")

fig_sales = px.bar(
    product_sales,
    x="Product",
    y="Sales",
    title="Sales Performance",
    text_auto=".2s"
)

st.plotly_chart(
    fig_sales,
    use_container_width=True
)


# =========================
# PRODUCT PROFIT
# =========================

product_profit = (
    filtered_df
    .groupby("Product")["Profit"]
    .sum()
    .reset_index()
    .sort_values(
        "Profit",
        ascending=False
    )
)


st.header("📈 Profit by Product")

fig_profit = px.bar(
    product_profit,
    x="Product",
    y="Profit",
    title="Profit Performance",
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
    .sort_values("Date")
)


st.header("📅 Sales Over Time")

fig_time = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    markers=True,
    title="Daily Sales"
)

st.plotly_chart(
    fig_time,
    use_container_width=True
)


# =========================
# BUSINESS INSIGHTS
# =========================

st.header("🧠 Business Insights")

if not product_sales.empty:

    best_product = product_sales.iloc[0]["Product"]

    worst_product = product_sales.iloc[-1]["Product"]

    best_sales = product_sales.iloc[0]["Sales"]

    st.success(
        f"🏆 Best-selling product: "
        f"{best_product} — "
        f"${best_sales:,.2f} sales."
    )

    st.warning(
        f"⚠️ Lowest-selling product: "
        f"{worst_product}."
    )

    st.info(
        f"💡 Total profit: "
        f"${total_profit:,.2f}"
    )


# =========================
# DETAILED DATA
# =========================

st.header("📋 Detailed Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# =========================
# DOWNLOAD
# =========================

st.header("📥 Export")

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Analysis",
    data=csv,
    file_name="OMARX_Analytics_Report.csv",
    mime="text/csv",
    use_container_width=True
)


# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "👑 OMARX Analytics | Analytics • Data • Intelligence"
)