
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "sales.csv"
OUTPUT_FILE = BASE_DIR / "output" / "cleaned_sales.csv"

# Extract
df = pd.read_csv(INPUT_FILE)

# Transform
df.columns = df.columns.str.strip().str.lower()
df = df.drop_duplicates(subset=["order_id"])

df["city"] = df["city"].str.strip().str.title()
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")

df = df.dropna(subset=["order_id", "quantity", "price"])

df["total_amount"] = df["quantity"] * df["price"]

# Load
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print("ETL pipeline completed successfully!")
print("Total sales:", df["total_amount"].sum())
print("Total records:", len(df))
print("Output file:", OUTPUT_FILE)
