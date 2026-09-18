from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data Folder
DATA_FOLDER = PROJECT_ROOT / "data" / "raw"

# Files
GLOBAL_SUPERSTORE = DATA_FOLDER / "superstore.csv"

GROCERY_INVENTORY = DATA_FOLDER / "Grocery_Inventory_and_Sales_Dataset.csv"

SUPERSTORE_DATASET = DATA_FOLDER / "Superstore Dataset.xlsx"