import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Spotify End-to-End AWS Data Pipeline", layout="wide")

st.title("🎵 Spotify End-to-End AWS Data Engineering Pipeline")
st.markdown("Automated sales data transformation and analytics dashboard.")

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "sales.csv"

if st.button("🚀 Run Live ETL Pipeline"):
    df = pd.read_csv(DATA_FILE)
    df.columns = df.columns.str.strip().str.lower()
    df = df.drop_duplicates(subset=["order_id"])
    df["city"] = df["city"].str.strip().str.title()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["order_id", "quantity", "price"])
    df["total_amount"] = df["quantity"] * df["price"]

    out_dir = BASE_DIR / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "cleaned_sales.csv", index=False)
    st.success("✅ ETL pipeline executed successfully!")

if DATA_FILE.exists():
    df_raw = pd.read_csv(DATA_FILE)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📥 Raw Input Data")
        st.dataframe(df_raw, use_container_width=True)

    cleaned_file = BASE_DIR / "output" / "cleaned_sales.csv"
    if cleaned_file.exists():
        df_clean = pd.read_csv(cleaned_file)
        with col2:
            st.subheader("📤 Processed Output Data")
            st.dataframe(df_clean, use_container_width=True)

        st.divider()
        st.subheader("📊 Key Metrics")
        m1, m2, m3 = st.columns(3)
        total_sales = df_clean["total_amount"].sum()
        m1.metric("Total Records", len(df_clean))
        m2.metric("Total Sales Amount", f"₹{total_sales:,.2f}")
        m3.metric("Unique Cities", df_clean["city"].nunique())
