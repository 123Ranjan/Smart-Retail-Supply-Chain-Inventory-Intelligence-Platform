import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT / "python" / "etl")
)

from config.database import get_engine


inventory = pd.read_csv(
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Grocery_Inventory_and_Sales_Dataset.csv"
)

engine = get_engine()

categories = pd.read_sql(
    """
    SELECT
        category_key,
        category_name,
        sub_category_name
    FROM retail_dw.dim_category
    """,
    engine
)

inventory_categories = (
    inventory["Catagory"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
)

database_categories = (
    categories["category_name"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
)

unmatched = sorted(
    set(inventory_categories)
    - set(database_categories)
)

print("=" * 50)
print("INVENTORY CATEGORY CHECK")
print("=" * 50)

print(
    "Inventory categories:",
    len(inventory_categories)
)

print(
    "Database categories:",
    len(database_categories)
)

print(
    "Unmatched categories:",
    len(unmatched)
)

print("\nUnmatched categories:")

for category in unmatched:
    count = (
        inventory["Catagory"]
        .astype(str)
        .str.strip()
        .eq(category)
        .sum()
    )

    print(
        f"{category} -> {count} products"
    )