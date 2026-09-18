import pandas as pd
from pathlib import Path


def extract_inventory():

    project_root = Path(__file__).resolve().parents[3]

    file_path = (
        project_root
        / "data"
        / "raw"
        / "Grocery_Inventory_and_Sales_Dataset.csv"
    )

    df = pd.read_csv(file_path)

    print(f"Inventory extracted: {len(df)} rows")

    return df