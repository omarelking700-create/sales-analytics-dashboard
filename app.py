import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ============================================================
# OMARX ANALYTICS | Professional Sales & Business Intelligence
# ============================================================

st.set_page_config(
    page_title="OMARX Analytics",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: #0b1020;
        color: #f5f7fb;
    }

    [data-testid="stSidebar"] {
        background: #111827;
    }

    .brand {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: .5px;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #aab4c3;
        font-size: 15px;
        margin-bottom: 22px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 12px;
    }

    .small-note {
        color: #9ca3af;
        font-size: 13px;
    }

    div[data-testid="stMetric"] {
        background: #151e31;
        border: 1px solid #26344d;
        border-radius: 16px;
        padding: 16px;
    }

    .insight {
        background: #151e31;
        border: 1px solid #26344d;
        border-radius: 14px;
        padding: 15px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Demo data
# -----------------------------
@st.cache_data
def make_demo_data():
    products = ["Laptop", "Smartphone", "Tablet", "Headphones", "Smartwatch"]
    rows = [
        ("2026-01-05", "Laptop", 1000, 700, 8),
        ("2026-01-10", "Smartphone", 500, 330, 18),
        ("2026-01-14", "Tablet", 300, 190, 12),
        ("2026-01-20", "Headphones", 150, 85, 30),
        ("2026-01-28", "Smartwatch", 200, 120, 20),
        ("2026-02-04", "Laptop", 1000, 700, 11),
        ("2026-02-09", "Smartphone", 500, 330, 22),
        ("2026-02-16", "Tablet", 300, 190, 17),
        ("2026-02-22", "Headphones", 150, 85, 34),
        ("2026-02-27", "Smartwatch", 200, 120, 24),
        ("2026-03-03", "Laptop", 1000, 700, 9),
        ("2026-03-08", "Smartphone", 500, 330, 25),
        ("2026-03-15", "Tablet", 300, 190, 14),
        ("2026-03-21", "Headphones", 150, 85, 38),
        ("2026-03-29", "Smartwatch", 200, 120, 27),
    ]
    df = pd.DataFrame(rows, columns=["Date", "Product", "Price", "Cost", "Quantity"])
    df["Date"] = pd.to_datetime(df["Date"])
    return df

# -----------------------------
# Helpers
# -----------------------------
def normalize_columns(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    aliases = {
        "product": "Product",
        "products": "Product",
        "item": "Product",
        "date": "Date",
        "day": "Date",
        "price": "Price",
        "unit price": "Price",
        "cost": "Cost",
        "unit cost": "Cost",
        "quantity": "Quantity",
        "qty": "Quantity",
        "units": "Quantity",
        "units sold": "Quantity",
        "profit": "Profit",
        "sales": "Total Sales",
        "total sales": "Total Sales",
        "revenue": "Total Sales",
    }
    rename = {}
    for c in df.columns:
        key = c.lower().strip()
        if key in aliases:
            rename[c] = aliases[key]
    df = df.rename(columns=rename)

    for col in ["Price", "Cost", "Quantity", "Profit", "Total Sales"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    return df

def prepare_data(df):
    df = normalize_columns(df)

    if "Product" not in df.columns:
        df["Product"] = "Unknown"

    if "Quantity" not in df.columns:
        df["Quantity"] = 0

    if "Total Sales" not in df.columns:
        if "Price" in df.columns:
            df["Total Sales"] = df["Price"].fillna(0) * df["Quantity"].fillna(0)
        else:
            df["Total Sales"] = 0

    if "Profit" not in df.columns:
        if "Price" in df.columns and "Cost" in df.columns:
            df["Profit"] = (
                (df["Price"].fillna(0) - df["Cost"].fillna(0))
                * df["Quantity"].fillna(0)
            )
        else:
            df["Profit"] = 0

    if "Date" not in df.columns:
        df["Date"] = pd.Timestamp.today().normalize()

    df = df.dropna(subset=["Product"]).copy()
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)
    df["Total Sales"] = pd.to_numeric(df["Total Sales"], errors="coerce").fillna(0)
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce").fillna(0)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Date"] = df["Date"].fillna(pd.Timestamp.today().normalize())

    df["Profit Margin"] = np.where(
        df["Total Sales"] != 0,
        df["Profit"] / df["Total Sales"] * 100,
        0
    )

    return df

def money(value):
    return f"${value:,.2f}"

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="brand">👑 OMARX Analytics</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Professional Sales & Business Intelligence Dashboard</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.markdown("## 👑 OMARX Analytics")
st.sidebar.caption("Sales • Profit • Business Intelligence")

demo = st.sidebar.button("🚀 Try Demo Dashboard", use_container_width=True)

uploaded = st.sidebar.file_uploader(
    "📁 Upload your Excel or CSV file",
    type=["xlsx", "xls", "csv"],
    help="Supported files: XLSX, XLS, CSV"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Data format")
st.sidebar.caption(
    "Recommended columns: Product, Date, Price, Cost, Quantity. "
    "The app also accepts Profit or Total Sales if already calculated."
)

# -----------------------------
# Load data
# -----------------------------
if demo or uploaded is None:
    df = make_demo_data()
    demo_mode = True
else:
    try:
        if uploaded.name.lower().endswith(".csv"):
            raw = pd.read_csv(uploaded)
        else:
            raw = pd.read_excel(uploaded)

        df = prepare_data(raw)
        demo_mode = False
    except Exception as e:
        st.error(f"Could not read the file: {e}")
        st.stop()

df = prepare_data(df)

# -----------------------------
# Filters
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔎 Filters")

products = sorted(df["Product"].dropna().astype(str).unique().tolist())
selected_products = st.sidebar.multiselect(
    "Products",
    products,
    default=products,
)

date_min = df["Date"].min().date()
date_max = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max,
)

filtered = df[df["Product"].astype(str).isin(selected_products)].copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        (filtered["Date"].dt.date >= start_date)
        & (filtered["Date"].dt.date <= end_date)
    ]

if filtered.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# -----------------------------
# Demo notice
# -----------------------------
if demo_mode:
    st.success("🚀 Demo Dashboard is active. You are viewing sample business data.")
else:
    st.info(f"📁 Analyzing: {uploaded.name}")

# -----------------------------
# Overview KPIs
# -----------------------------
st.markdown('<div class="section-title">📊 Business Overview</div>', unsafe_allow_html=True)

total_sales = filtered["Total Sales"].sum()
total_profit = filtered["Profit"].sum()
units_sold = filtered["Quantity"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("💵 Total Sales", money(total_sales))
c2.metric("💰 Total Profit", money(total_profit))
c3.metric("📦 Units Sold", f"{units_sold:,.0f}")
c4.metric("📈 Profit Margin", f"{profit_margin:.2f}%")

# -----------------------------
# Sales & Profit section
# -----------------------------
st.markdown("---")
st.markdown('<div class="section-title">💰 Sales & Profit</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "📈 Sales & Profit",
    "📊 Profit Margin",
    "🏆 Top Products"
])

with tab1:
    product_summary = (
        filtered.groupby("Product", as_index=False)
        .agg(
            Sales=("Total Sales", "sum"),
            Profit=("Profit", "sum"),
            Units=("Quantity", "sum"),
        )
        .sort_values("Sales", ascending=False)
    )

    fig = px.bar(
        product_summary,
        x="Product",
        y=["Sales", "Profit"],
        barmode="group",
        title="Sales vs Profit by Product",
        text_auto=".2s",
    )
    fig.update_layout(template="plotly_dark", height=480)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    margin_summary = (
        filtered.groupby("Product", as_index=False)
        .agg(Sales=("Total Sales", "sum"), Profit=("Profit", "sum"))
    )
    margin_summary["Profit Margin"] = np.where(
        margin_summary["Sales"] != 0,
        margin_summary["Profit"] / margin_summary["Sales"] * 100,
        0
    )
    margin_summary = margin_summary.sort_values("Profit Margin", ascending=False)

    fig = px.bar(
        margin_summary,
        x="Product",
        y="Profit Margin",
        title="Profit Margin by Product",
        text="Profit Margin",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(template="plotly_dark", height=480, yaxis_title="Margin (%)")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    top = (
        filtered.groupby("Product", as_index=False)
        .agg(
            Sales=("Total Sales", "sum"),
            Profit=("Profit", "sum"),
            Units=("Quantity", "sum"),
        )
        .sort_values("Profit", ascending=False)
        .head(10)
    )

    st.dataframe(
        top.style.format({
            "Sales": "${:,.2f}",
            "Profit": "${:,.2f}",
            "Units": "{:,.0f}",
        }),
        use_container_width=True,
        hide_index=True,
    )

# -----------------------------
# Trend analysis
# -----------------------------
st.markdown("---")
st.markdown('<div class="section-title">📅 Sales Trend</div>', unsafe_allow_html=True)

daily = (
    filtered.groupby("Date", as_index=False)
    .agg(Sales=("Total Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Date")
)

fig = px.line(
    daily,
    x="Date",
    y=["Sales", "Profit"],
    markers=True,
    title="Sales & Profit Over Time",
)
fig.update_layout(template="plotly_dark", height=450)
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Automated business insights
# -----------------------------
st.markdown("---")
st.markdown('<div class="section-title">🤖 Business Insights</div>', unsafe_allow_html=True)

summary = (
    filtered.groupby("Product", as_index=False)
    .agg(
        Sales=("Total Sales", "sum"),
        Profit=("Profit", "sum"),
        Units=("Quantity", "sum"),
    )
)

if not summary.empty:
    best_sales = summary.loc[summary["Sales"].idxmax()]
    best_profit = summary.loc[summary["Profit"].idxmax()]
    best_margin = summary.assign(
        Margin=np.where(summary["Sales"] != 0, summary["Profit"] / summary["Sales"] * 100, 0)
    ).loc[
        lambda x: x["Margin"].idxmax()
    ]

    insights = [
        f"🏆 Best product by sales: **{best_sales['Product']}** with {money(best_sales['Sales'])}.",
        f"💰 Highest profit product: **{best_profit['Product']}** with {money(best_profit['Profit'])}.",
        f"📈 Highest profit margin: **{best_margin['Product']}** at {best_margin['Margin']:.2f}%.",
        f"📦 Total units sold in the selected period: **{units_sold:,.0f}**.",
    ]

    if profit_margin < 10:
        insights.append("⚠️ Overall profit margin is below 10%. Review costs and pricing.")
    elif profit_margin >= 30:
        insights.append("🔥 Overall profit margin is strong at 30% or more.")

    for text in insights:
        st.markdown(f'<div class="insight">{text}</div>', unsafe_allow_html=True)

# -----------------------------
# Detailed data
# -----------------------------
st.markdown("---")
st.markdown('<div class="section-title">📋 Detailed Data</div>', unsafe_allow_html=True)

display_df = filtered.copy()
display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
)

# -----------------------------
# Downloads
# -----------------------------
st.markdown("---")
st.markdown('<div class="section-title">⬇️ Export</div>', unsafe_allow_html=True)

csv_data = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download filtered data as CSV",
    data=csv_data,
    file_name="omarx_analytics_report.csv",
    mime="text/csv",
)

st.caption("OMARX Analytics • Professional Sales & Business Intelligence")
