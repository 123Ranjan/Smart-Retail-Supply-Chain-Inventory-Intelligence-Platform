import pandas as pd
from python.utils.config import (
    GLOBAL_SUPERSTORE,
    GROCERY_INVENTORY,
    SUPERSTORE_DATASET,
)

from python.utils.helper_functions import (
    load_csv,
    load_excel,
)

def profile(df, dataset_name):

    print("=" * 80)
    print(dataset_name)
    print("=" * 80)

    print(f"Rows : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumn Names")
    print(df.columns.tolist())

    print("\nData Types")
    print(df.dtypes)

    print("\nMissing Values")
    print(df.isnull().sum())

    print("\nDuplicate Rows")
    print(df.duplicated().sum())

    print("\nSummary Statistics")
    print(df.describe(include="all"))

    print("\n")


def main():

    global_df = load_csv(GLOBAL_SUPERSTORE)

    inventory_df = load_csv(GROCERY_INVENTORY)

    orders_df = load_excel(
        SUPERSTORE_DATASET,
        "Orders"
    )

    returns_df = load_excel(
        SUPERSTORE_DATASET,
        "Returns"
    )

    profile(global_df, "GLOBAL SUPERSTORE")

    profile(inventory_df, "GROCERY INVENTORY")

    profile(orders_df, "SUPERSTORE ORDERS")

    profile(returns_df, "SUPERSTORE RETURNS")


if __name__ == "__main__":
    main()