import pandas as pd


def transform_fact_inventory(
    inventory_df,
    product_dimension,
    supplier_dimension,
    warehouse_dimension
):

    inventory = inventory_df.copy()

    # -------------------------
    # Product Key
    # -------------------------

    product_lookup = (
        product_dimension[
            [
                "product_key",
                "product_id"
            ]
        ]
        .drop_duplicates(
            subset=["product_id"]
        )
    )

    inventory = inventory.merge(
        product_lookup,
        left_on="Product_ID",
        right_on="product_id",
        how="left"
    )

    # -------------------------
    # Supplier Key
    # -------------------------

    supplier_lookup = (
        supplier_dimension[
            [
                "supplier_key",
                "supplier_id"
            ]
        ]
        .drop_duplicates(
            subset=["supplier_id"]
        )
    )

    inventory = inventory.merge(
        supplier_lookup,
        left_on="Supplier_ID",
        right_on="supplier_id",
        how="left"
    )

    # -------------------------
    # Warehouse Key
    # -------------------------

    warehouse_lookup = (
        warehouse_dimension[
            [
                "warehouse_key",
                "warehouse_location"
            ]
        ]
        .drop_duplicates(
            subset=["warehouse_location"]
        )
    )

    inventory = inventory.merge(
        warehouse_lookup,
        left_on="Warehouse_Location",
        right_on="warehouse_location",
        how="left"
    )

    # -------------------------
    # Numeric Cleaning
    # -------------------------

    numeric_columns = [
        "Stock_Quantity",
        "Reorder_Level",
        "Reorder_Quantity",
        "Sales_Volume",
        "Inventory_Turnover_Rate"
    ]

    for column in numeric_columns:
        inventory[column] = pd.to_numeric(
            inventory[column],
            errors="coerce"
        )

    # -------------------------
    # Fact Table
    # -------------------------

    fact_inventory = inventory[
        [
            "product_key",
            "supplier_key",
            "warehouse_key",
            "Stock_Quantity",
            "Reorder_Level",
            "Reorder_Quantity",
            "Sales_Volume",
            "Inventory_Turnover_Rate"
        ]
    ].copy()

    fact_inventory = fact_inventory.rename(
        columns={
            "Stock_Quantity": "stock_quantity",
            "Reorder_Level": "reorder_level",
            "Reorder_Quantity": "reorder_quantity",
            "Sales_Volume": "sales_volume",
            "Inventory_Turnover_Rate":
                "inventory_turnover_rate"
        }
    )

    return fact_inventory.reset_index(drop=True)