import pandas as pd


def transform_fact_sales(
    sales_df,
    product_dimension,
    customer_dimension,
    geography_dimension,
    ship_mode_dimension
):

    sales = sales_df.copy()

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

    sales = sales.merge(
        product_lookup,
        left_on="Product.ID",
        right_on="product_id",
        how="left"
    )

    # -------------------------
    # Customer Key
    # -------------------------

    customer_lookup = (
        customer_dimension[
            [
                "customer_key",
                "customer_id"
            ]
        ]
        .drop_duplicates(
            subset=["customer_id"]
        )
    )

    sales = sales.merge(
        customer_lookup,
        left_on="Customer.ID",
        right_on="customer_id",
        how="left"
    )

    # -------------------------
    # Geography Key
    # -------------------------

    geography_lookup = geography_dimension[
        [
            "geography_key",
            "country",
            "market",
            "region",
            "state",
            "city"
        ]
    ]

    sales = sales.merge(
        geography_lookup,
        left_on=[
            "Country",
            "Market",
            "Region",
            "State",
            "City"
        ],
        right_on=[
            "country",
            "market",
            "region",
            "state",
            "city"
        ],
        how="left"
    )

    # -------------------------
    # Ship Mode Key
    # -------------------------

    ship_lookup = ship_mode_dimension[
        [
            "ship_mode_key",
            "ship_mode"
        ]
    ]

    sales = sales.merge(
        ship_lookup,
        left_on="Ship.Mode",
        right_on="ship_mode",
        how="left"
    )

    # -------------------------
    # Date Key
    # -------------------------

    sales["Order.Date"] = pd.to_datetime(
        sales["Order.Date"],
        errors="coerce"
    )

    sales["date_key"] = (
        sales["Order.Date"]
        .dt.strftime("%Y%m%d")
    )

    sales = sales.dropna(
        subset=["date_key"]
    )

    sales["date_key"] = (
        sales["date_key"].astype(int)
    )

    # -------------------------
    # Fact Table
    # -------------------------

    fact_sales = sales[
        [
            "Order.ID",
            "product_key",
            "customer_key",
            "geography_key",
            "ship_mode_key",
            "date_key",
            "Quantity",
            "Sales",
            "Profit",
            "Discount",
            "Shipping.Cost",
            "Order.Priority"
        ]
    ].copy()

    fact_sales = fact_sales.rename(
        columns={
            "Order.ID": "order_id",
            "Quantity": "quantity",
            "Sales": "sales",
            "Profit": "profit",
            "Discount": "discount",
            "Shipping.Cost": "shipping_cost",
            "Order.Priority": "order_priority"
        }
    )

    return fact_sales.reset_index(drop=True)