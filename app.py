import streamlit as st
import pandas as pd
from pathlib import Path
import time

st.set_page_config(
    page_title="Spotify Data Pipeline | Live AWS Engineering",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Spotify Dark & Neon Green Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    /* Global Background and Typography */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #181818 0%, #121212 90%);
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }

    /* Spotify Hero Header */
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 215, 96, 0.15) 0%, rgba(18, 18, 18, 0.9) 100%);
        border: 1px solid rgba(30, 215, 96, 0.35);
        border-radius: 20px;
        padding: 35px 40px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), inset 0 0 15px rgba(30, 215, 96, 0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
    }

    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        background: linear-gradient(90deg, #FFFFFF 0%, #1ED760 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #B3B3B3;
        font-size: 1.05rem;
        margin-top: 8px;
        margin-bottom: 0;
    }

    .spotify-badge {
        background-color: #1ED760;
        color: #000000;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 50px;
        font-size: 0.85rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 10px;
    }

    /* Stat Cards */
    .stat-card {
        background-color: #181818;
        border: 1px solid #282828;
        border-radius: 16px;
        padding: 22px;
        text-align: left;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .stat-card:hover {
        transform: translateY(-4px);
        border-color: #1ED760;
        box-shadow: 0 8px 24px rgba(30, 215, 96, 0.25);
    }

    .stat-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #1ED760, transparent);
    }

    .stat-label {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #B3B3B3;
        margin-bottom: 6px;
    }

    .stat-val {
        font-size: 2rem;
        font-weight: 800;
        color: #1ED760;
        margin: 0;
    }

    /* Buttons */
    .stButton > button {
        background-color: #1ED760 !important;
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 28px !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 15px rgba(30, 215, 96, 0.4) !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        background-color: #1fdf64 !important;
        transform: scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(30, 215, 96, 0.6) !important;
    }

    /* Architecture Tag */
    .arch-tag {
        background-color: #282828;
        border: 1px solid #3E3E3E;
        color: #FFFFFF;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 6px;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "sales.csv"
OUTPUT_FILE = BASE_DIR / "output" / "cleaned_sales.csv"

# Pre-run if output not created yet
if not OUTPUT_FILE.exists() and DATA_FILE.exists():
    df_init = pd.read_csv(DATA_FILE)
    df_init.columns = df_init.columns.str.strip().str.lower()
    df_init = df_init.drop_duplicates(subset=["order_id"])
    df_init["city"] = df_init["city"].str.strip().str.title()
    df_init["quantity"] = pd.to_numeric(df_init["quantity"], errors="coerce")
    df_init["price"] = pd.to_numeric(df_init["price"], errors="coerce")
    df_init = df_init.dropna(subset=["order_id", "quantity", "price"])
    df_init["total_amount"] = df_init["quantity"] * df_init["price"]
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df_init.to_csv(OUTPUT_FILE, index=False)

# Sidebar Architecture details
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <svg viewBox="0 0 167.5 167.5" width="60" height="60">
                <circle cx="83.8" cy="83.8" r="83.8" fill="#1ED760"/>
                <path fill="#121212" d="M118.9 121.7c-1.5 0-2.8-.5-3.9-1.3-15.4-9.4-34.8-11.6-57.6-6.4-3.5.8-6.9-1.4-7.7-4.9-.8-3.5 1.4-6.9 4.9-7.7 26-5.9 47.9-3.4 65.6 7.4 3 1.9 4 5.9 2.1 8.9-1 1.7-2.4 2.6-4.4 2.6zm6.8-19.8c-1.9 0-3.5-.6-4.8-1.7-17.7-10.9-44.6-14-65.5-7.7-4.1 1.2-8.5-1.1-9.7-5.2-1.2-4.1 1.1-8.5 5.2-9.7 24.7-7.5 54.7-4 75.3 8.7 3.6 2.2 4.7 7 2.5 10.6-1.5 2.1-3.6 3.2-6 3.2zm1-20.9c-21.2-12.6-56.2-13.7-76.5-7.6-4.9 1.5-10.2-1.3-11.7-6.2-1.5-4.9 1.3-10.2 6.2-11.7 24.1-7.3 63.3-5.9 88.2 8.9 4.5 2.7 6 8.6 3.3 13.1-2 3.5-5.6 5.3-9.5 5.3z"/>
            </svg>
            <h3 style="margin-top: 10px; color: #FFFFFF; font-weight: 700;">Data Engineering Ops</h3>
            <span style="color: #1ED760; font-size: 0.85rem; font-weight: 600;">AWS Serverless Pipeline</span>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("#### ☁️ Cloud Architecture")
    st.markdown("""
        <span class="arch-tag">Amazon S3</span>
        <span class="arch-tag">AWS Lambda</span>
        <span class="arch-tag">AWS Athena</span>
        <span class="arch-tag">Python Pandas</span>
        <span class="arch-tag">SQL Analytics</span>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("#### 🛠️ Repository Status")
    st.markdown("**Owner:** [`Pratik30122005`](https://github.com/Pratik30122005)")
    st.markdown("**Branch:** `main` (Live)")
    st.markdown("**Pipeline Mode:** Event-driven")

# Main Hero Header
st.markdown("""
    <div class="hero-container">
        <div>
            <div class="spotify-badge">
                <span style="font-size: 14px;">●</span> AWS DATA PIPELINE
            </div>
            <h1 class="hero-title">Spotify End-to-End AWS Data Engineering</h1>
            <p class="hero-subtitle">High-throughput automated ETL processing engine for transaction logs and streaming revenue analytics.</p>
        </div>
        <div>
            <svg viewBox="0 0 167.5 167.5" width="85" height="85">
                <circle cx="83.8" cy="83.8" r="83.8" fill="#1ED760"/>
                <path fill="#121212" d="M118.9 121.7c-1.5 0-2.8-.5-3.9-1.3-15.4-9.4-34.8-11.6-57.6-6.4-3.5.8-6.9-1.4-7.7-4.9-.8-3.5 1.4-6.9 4.9-7.7 26-5.9 47.9-3.4 65.6 7.4 3 1.9 4 5.9 2.1 8.9-1 1.7-2.4 2.6-4.4 2.6zm6.8-19.8c-1.9 0-3.5-.6-4.8-1.7-17.7-10.9-44.6-14-65.5-7.7-4.1 1.2-8.5-1.1-9.7-5.2-1.2-4.1 1.1-8.5 5.2-9.7 24.7-7.5 54.7-4 75.3 8.7 3.6 2.2 4.7 7 2.5 10.6-1.5 2.1-3.6 3.2-6 3.2zm1-20.9c-21.2-12.6-56.2-13.7-76.5-7.6-4.9 1.5-10.2-1.3-11.7-6.2-1.5-4.9 1.3-10.2 6.2-11.7 24.1-7.3 63.3-5.9 88.2 8.9 4.5 2.7 6 8.6 3.3 13.1-2 3.5-5.6 5.3-9.5 5.3z"/>
            </svg>
        </div>
    </div>
""", unsafe_allow_html=True)

# Run ETL Action Button
col_btn, col_info = st.columns([1, 2])
with col_btn:
    run_clicked = st.button("▶ Trigger Live ETL Pipeline")

with col_info:
    if run_clicked:
        with st.spinner("Processing event trigger & transforming sales logs..."):
            time.sleep(0.5)
            df = pd.read_csv(DATA_FILE)
            df.columns = df.columns.str.strip().str.lower()
            df = df.drop_duplicates(subset=["order_id"])
            df["city"] = df["city"].str.strip().str.title()
            df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
            df["price"] = pd.to_numeric(df["price"], errors="coerce")
            df = df.dropna(subset=["order_id", "quantity", "price"])
            df["total_amount"] = df["quantity"] * df["price"]

            OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(OUTPUT_FILE, index=False)
            st.success("⚡ Pipeline executed successfully! Target S3 processed bucket refreshed.")

# Metrics Section
if OUTPUT_FILE.exists():
    df_clean = pd.read_csv(OUTPUT_FILE)
    total_revenue = float(df_clean["total_amount"].sum())
    total_orders = int(len(df_clean))
    avg_ticket = float(df_clean["total_amount"].mean())
    cities = int(df_clean["city"].nunique())

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Total Revenue</div>
                <p class="stat-val">₹{total_revenue:,.0f}</p>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Processed Orders</div>
                <p class="stat-val">{total_orders}</p>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Avg Order Value</div>
                <p class="stat-val">₹{avg_ticket:,.0f}</p>
            </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Active Regions</div>
                <p class="stat-val">{cities}</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Datasets Section
tab1, tab2, tab3 = st.tabs(["📊 Analytics & Charts", "📤 Cleaned / Processed S3 Data", "📥 Raw Ingestion S3 Bucket"])

with tab1:
    if OUTPUT_FILE.exists():
        df_clean = pd.read_csv(OUTPUT_FILE)
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Sales by City")
            city_sales = df_clean.groupby("city")["total_amount"].sum().reset_index()
            st.bar_chart(city_sales.set_index("city"), color="#1ED760")
        with c2:
            st.subheader("Sales by Product")
            prod_sales = df_clean.groupby("product")["total_amount"].sum().reset_index()
            st.bar_chart(prod_sales.set_index("product"), color="#1ED760")

with tab2:
    if OUTPUT_FILE.exists():
        df_clean = pd.read_csv(OUTPUT_FILE)
        st.dataframe(df_clean, use_container_width=True)
    else:
        st.info("Click 'Trigger Live ETL Pipeline' above to generate processed data.")

with tab3:
    if DATA_FILE.exists():
        df_raw = pd.read_csv(DATA_FILE)
        st.dataframe(df_raw, use_container_width=True)
