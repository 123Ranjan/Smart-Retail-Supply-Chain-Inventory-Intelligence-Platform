import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT / "python" / "etl")
)

from config.database import get_engine


# Load inventory CSV
inventory = pd.read_csv(
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Grocery_Inventory_and_Sales_Dataset.csv"
)


# Read products from PostgreSQL
engine = get_engine()

products = pd.read_sql(
    """
    SELECT product_id
    FROM retail_dw.dim_product
    """,
    engine
)


# Convert IDs to strings
inventory_ids = set(
    inventory["Product_ID"]
    .dropna()
    .astype(str)
    .str.strip()
)

superstore_ids = set(
    products["product_id"]
    .dropna()
    .astype(str)
    .str.strip()
)


# Compare
matched = inventory_ids.intersection(
    superstore_ids
)

unmatched = inventory_ids - superstore_ids


print("=" * 50)
print("PRODUCT ID MATCH CHECK")
print("=" * 50)

print(
    f"Inventory unique Product_ID : {len(inventory_ids)}"
)

print(
    f"Superstore unique Product_ID: {len(superstore_ids)}"
)

print(
    f"Matched Product_ID          : {len(matched)}"
)

print(
    f"Unmatched Product_ID        : {len(unmatched)}"
)


print("\nSample Inventory IDs:")
for value in list(inventory_ids)[:10]:
    print(value)


print("\nSample Superstore IDs:")
for value in list(superstore_ids)[:10]:
    print(value)


print("\nSample Unmatched Inventory IDs:")
for value in list(unmatched)[:10]:
    print(value)