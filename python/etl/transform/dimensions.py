import pandas as pd


# =========================================================
# DIM CATEGORY
# =========================================================

def transform_category(superstore_df, inventory_df):

    # Superstore categories
    superstore_category = (
        superstore_df[
            ["Category", "Sub.Category"]
        ]
        .dropna(subset=["Category"])
        .rename(
            columns={
                "Category": "category_name",
                "Sub.Category": "sub_category_name"
            }
        )
    )

    # Inventory categories
    inventory_category = (
        inventory_df[
            ["Catagory"]
        ]
        .rename(
            columns={
                "Catagory": "category_name"
            }
        )
    )

    # Missing inventory category -> Unknown
    inventory_category["category_name"] = (
        inventory_category["category_name"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    # Inventory has no sub-category
    inventory_category["sub_category_name"] = None

    # Combine
    category = pd.concat(
        [
            superstore_category[
                ["category_name", "sub_category_name"]
            ],
            inventory_category[
                ["category_name", "sub_category_name"]
            ]
        ],
        ignore_index=True
    )

    # Clean category names
    category["category_name"] = (
        category["category_name"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    # Remove duplicates
    category = (
        category
        .drop_duplicates(
            subset=[
                "category_name",
                "sub_category_name"
            ]
        )
        .reset_index(drop=True)
    )

    # Guarantee Unknown exists
    if not category["category_name"].eq("Unknown").any():

        category = pd.concat(
            [
                category,
                pd.DataFrame(
                    [{
                        "category_name": "Unknown",
                        "sub_category_name": None
                    }]
                )
            ],
            ignore_index=True
        )

    return category


# =========================================================
# DIM CUSTOMER
# =========================================================

def transform_customer(df):

    customer = (
        df[
            [
                "Customer.ID",
                "Customer.Name",
                "Segment"
            ]
        ]
        .dropna(subset=["Customer.ID"])
        .drop_duplicates()
        .rename(
            columns={
                "Customer.ID": "customer_id",
                "Customer.Name": "customer_name",
                "Segment": "segment"
            }
        )
        .reset_index(drop=True)
    )

    return customer


# =========================================================
# DIM PRODUCT
# =========================================================

def transform_product(
    superstore_df,
    inventory_df,
    category_dimension
):

    # -----------------------------------------------------
    # CATEGORY LOOKUP
    # -----------------------------------------------------

    category_lookup = (
        category_dimension[
            [
                "category_key",
                "category_name"
            ]
        ]
        .copy()
    )

    category_lookup["category_name"] = (
        category_lookup["category_name"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    category_lookup = (
        category_lookup
        .drop_duplicates(
            subset=["category_name"]
        )
        .reset_index(drop=True)
    )

    # -----------------------------------------------------
    # SUPERSTORE PRODUCTS
    # -----------------------------------------------------

    superstore_products = (
        superstore_df[
            [
                "Product.ID",
                "Product.Name",
                "Category"
            ]
        ]
        .dropna(subset=["Product.ID"])
        .drop_duplicates()
        .rename(
            columns={
                "Product.ID": "product_id",
                "Product.Name": "product_name",
                "Category": "category_name"
            }
        )
    )

    superstore_products["category_name"] = (
        superstore_products["category_name"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    superstore_products = (
        superstore_products.merge(
            category_lookup,
            on="category_name",
            how="left"
        )
    )

    # Validate Superstore mapping
    missing = (
        superstore_products["category_key"]
        .isna()
        .sum()
    )

    if missing > 0:

        print(
            f"ERROR: {missing} Superstore products "
            "have missing category_key."
        )

        print(
            superstore_products[
                superstore_products["category_key"].isna()
            ][
                [
                    "product_id",
                    "product_name",
                    "category_name"
                ]
            ].head(20)
        )

        raise ValueError(
            "Superstore product category mapping failed."
        )

    superstore_products = superstore_products[
        [
            "product_id",
            "product_name",
            "category_key"
        ]
    ].copy()

    superstore_products["unit_price"] = None
    superstore_products["product_status"] = "Active"

    # -----------------------------------------------------
    # INVENTORY PRODUCTS
    # -----------------------------------------------------

    inventory_products = (
        inventory_df[
            [
                "Product_ID",
                "Product_Name",
                "Catagory",
                "Unit_Price",
                "Status"
            ]
        ]
        .dropna(subset=["Product_ID"])
        .drop_duplicates()
        .rename(
            columns={
                "Product_ID": "product_id",
                "Product_Name": "product_name",
                "Catagory": "category_name",
                "Unit_Price": "unit_price",
                "Status": "product_status"
            }
        )
    )

    # Missing category -> Unknown
    inventory_products["category_name"] = (
        inventory_products["category_name"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Map category
    inventory_products = (
        inventory_products.merge(
            category_lookup,
            on="category_name",
            how="left"
        )
    )

    # Clean price
    inventory_products["unit_price"] = (
        inventory_products["unit_price"]
        .astype(str)
        .str.replace(
            "$",
            "",
            regex=False
        )
        .str.replace(
            ",",
            "",
            regex=False
        )
        .str.strip()
    )

    inventory_products["unit_price"] = pd.to_numeric(
        inventory_products["unit_price"],
        errors="coerce"
    )

    # -----------------------------------------------------
    # FINAL VALIDATION
    # -----------------------------------------------------

    missing = (
        inventory_products["category_key"]
        .isna()
        .sum()
    )

    if missing > 0:

        print(
            f"ERROR: {missing} inventory products "
            "have missing category_key."
        )

        print(
            inventory_products[
                inventory_products["category_key"].isna()
            ][
                [
                    "product_id",
                    "product_name",
                    "category_name"
                ]
            ].head(20)
        )

        raise ValueError(
            "Inventory product category mapping failed."
        )

    inventory_products = inventory_products[
        [
            "product_id",
            "product_name",
            "category_key",
            "unit_price",
            "product_status"
        ]
    ].copy()

    # -----------------------------------------------------
    # COMBINE PRODUCTS
    # -----------------------------------------------------

    product = pd.concat(
        [
            superstore_products,
            inventory_products
        ],
        ignore_index=True
    )

    product = (
        product
        .drop_duplicates(
            subset=["product_id"]
        )
        .reset_index(drop=True)
    )

    return product


# =========================================================
# DIM GEOGRAPHY
# =========================================================

def transform_geography(df):

    geography = (
        df[
            [
                "Country",
                "Market",
                "Region",
                "State",
                "City"
            ]
        ]
        .drop_duplicates()
        .rename(
            columns={
                "Country": "country",
                "Market": "market",
                "Region": "region",
                "State": "state",
                "City": "city"
            }
        )
        .reset_index(drop=True)
    )

    return geography


# =========================================================
# DIM SHIP MODE
# =========================================================

def transform_ship_mode(df):

    ship_mode = (
        df[
            ["Ship.Mode"]
        ]
        .dropna()
        .drop_duplicates()
        .rename(
            columns={
                "Ship.Mode": "ship_mode"
            }
        )
        .reset_index(drop=True)
    )

    return ship_mode


# =========================================================
# DIM SUPPLIER
# =========================================================

def transform_supplier(df):

    supplier = (
        df[
            [
                "Supplier_ID",
                "Supplier_Name"
            ]
        ]
        .dropna(subset=["Supplier_ID"])
        .drop_duplicates()
        .rename(
            columns={
                "Supplier_ID": "supplier_id",
                "Supplier_Name": "supplier_name"
            }
        )
        .reset_index(drop=True)
    )

    return supplier


# =========================================================
# DIM WAREHOUSE
# =========================================================

def transform_warehouse(df):

    warehouse = (
        df[
            ["Warehouse_Location"]
        ]
        .dropna()
        .drop_duplicates()
        .rename(
            columns={
                "Warehouse_Location":
                    "warehouse_location"
            }
        )
        .reset_index(drop=True)
    )

    return warehouse


# =========================================================
# DIM DATE
# =========================================================

def create_date_dimension(
    start_date="2011-01-01",
    end_date="2015-12-31"
):

    dates = pd.date_range(
        start=start_date,
        end=end_date
    )

    date_df = pd.DataFrame()

    date_df["date_key"] = (
        dates
        .strftime("%Y%m%d")
        .astype(int)
    )

    date_df["full_date"] = dates.date
    date_df["day"] = dates.day
    date_df["month"] = dates.month
    date_df["month_name"] = dates.month_name()
    date_df["quarter"] = dates.quarter
    date_df["year"] = dates.year

    date_df["week_number"] = (
        dates
        .isocalendar()
        .week
        .astype(int)
        .to_numpy()
    )

    return date_df