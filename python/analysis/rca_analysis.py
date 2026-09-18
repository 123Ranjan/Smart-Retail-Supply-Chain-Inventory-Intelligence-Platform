import pandas as pd
import numpy as np

from python.etl.config.database import get_engine


# =========================================================
# LOAD SALES + INVENTORY DATA
# =========================================================

def load_rca_data():

    engine = get_engine()

    query = """
        SELECT
            fi.product_key,
            fi.stock_quantity,
            fi.reorder_level,
            fi.reorder_quantity,
            fi.sales_volume,
            fi.inventory_turnover_rate,

            p.product_id,
            p.product_name,
            p.category_key,

            c.category_name,

            s.supplier_name,

            w.warehouse_location

        FROM retail_dw.fact_inventory fi

        LEFT JOIN retail_dw.dim_product p
            ON fi.product_key = p.product_key

        LEFT JOIN retail_dw.dim_category c
            ON p.category_key = c.category_key

        LEFT JOIN retail_dw.dim_supplier s
            ON fi.supplier_key = s.supplier_key

        LEFT JOIN retail_dw.dim_warehouse w
            ON fi.warehouse_key = w.warehouse_key
    """

    print("Loading RCA data...")

    df = pd.read_sql(
        query,
        engine
    )

    print(
        "RCA data loaded:",
        len(df),
        "rows"
    )

    return df


# =========================================================
# INVENTORY PRESSURE
# =========================================================

def calculate_inventory_pressure(df):

    result = df.copy()

    # -----------------------------------------------------
    # STOCK GAP
    # -----------------------------------------------------

    result["stock_gap"] = (
        result["reorder_level"]
        -
        result["stock_quantity"]
    )

    # -----------------------------------------------------
    # STOCK GAP %
    # -----------------------------------------------------

    result["stock_gap_pct"] = np.where(
        result["reorder_level"] > 0,

        (
            result["reorder_level"]
            -
            result["stock_quantity"]
        )
        /
        result["reorder_level"]
        * 100,

        0
    )

    # Negative gap is not inventory shortage
    result["stock_gap_pct"] = (
        result["stock_gap_pct"]
        .clip(lower=0)
    )

    # -----------------------------------------------------
    # REORDER STATUS
    # -----------------------------------------------------

    result["reorder_required"] = (
        result["stock_quantity"]
        <
        result["reorder_level"]
    )

    return result


# =========================================================
# DEMAND CLASSIFICATION
# =========================================================

def classify_demand(df):

    result = df.copy()

    # -----------------------------------------------------
    # SALES VOLUME THRESHOLDS
    # -----------------------------------------------------

    demand_75 = np.percentile(
        result["sales_volume"],
        75
    )

    demand_50 = np.percentile(
        result["sales_volume"],
        50
    )

    # -----------------------------------------------------
    # DEMAND LEVEL
    # -----------------------------------------------------

    result["demand_level"] = np.select(
        [
            result["sales_volume"] >= demand_75,

            result["sales_volume"] >= demand_50
        ],

        [
            "High Demand",

            "Medium Demand"
        ],

        default="Low Demand"
    )

    return result


# =========================================================
# RCA CLASSIFICATION
# =========================================================

def classify_inventory_risk(df):

    result = df.copy()

    # -----------------------------------------------------
    # MEDIAN TURNOVER
    # -----------------------------------------------------

    median_turnover = (
        result["inventory_turnover_rate"]
        .median()
    )

    # -----------------------------------------------------
    # RCA CATEGORY
    # -----------------------------------------------------

    result["rca_category"] = np.select(

        [

            # ---------------------------------------------
            # 1. HIGH DEMAND + LOW STOCK
            # ---------------------------------------------

            (
                result["reorder_required"]
                &
                (
                    result["demand_level"]
                    == "High Demand"
                )
            ),

            # ---------------------------------------------
            # 2. FAST TURNOVER + LOW STOCK
            # ---------------------------------------------

            (
                result["reorder_required"]
                &
                (
                    result["inventory_turnover_rate"]
                    >= median_turnover
                )
                &
                (
                    result["demand_level"]
                    != "High Demand"
                )
            ),

            # ---------------------------------------------
            # 3. LOW STOCK
            # ---------------------------------------------

            result["reorder_required"]
        ],

        [
            "High Demand + Low Stock",

            "Fast Turnover + Low Stock",

            "Low Stock"
        ],

        default="Normal"
    )

    return result


# =========================================================
# RCA SUMMARY
# =========================================================

def rca_summary(df):

    summary = (
        df["rca_category"]
        .value_counts()
        .reset_index()
    )

    summary.columns = [
        "rca_category",
        "product_count"
    ]

    summary["percentage"] = (
        summary["product_count"]
        /
        len(df)
        * 100
    )

    print("\n" + "=" * 60)
    print("INVENTORY RCA SUMMARY")
    print("=" * 60)

    print(
        summary.to_string(
            index=False
        )
    )

    return summary


# =========================================================
# HIGH-PRIORITY INVENTORY RCA
# =========================================================

def high_priority_rca(df):

    # -----------------------------------------------------
    # IMPORTANT:
    # Use the same RCA labels created by
    # classify_inventory_risk()
    # -----------------------------------------------------

    result = (
        df[
            df["rca_category"]
            .isin(
                [
                    "High Demand + Low Stock",
                    "Fast Turnover + Low Stock"
                ]
            )
        ]
        .sort_values(
            [
                "stock_gap_pct",
                "sales_volume"
            ],
            ascending=False
        )
    )

    columns = [
        "product_id",
        "product_name",
        "category_name",
        "stock_quantity",
        "reorder_level",
        "stock_gap",
        "stock_gap_pct",
        "sales_volume",
        "inventory_turnover_rate",
        "supplier_name",
        "warehouse_location",
        "demand_level",
        "rca_category"
    ]

    print("\n" + "=" * 60)
    print("HIGH-PRIORITY INVENTORY RCA")
    print("=" * 60)

    print(
        result[
            columns
        ]
        .head(30)
        .to_string(
            index=False
        )
    )

    return result


# =========================================================
# CATEGORY INVENTORY RCA
# =========================================================

def category_rca(df):

    result = (
        df.groupby("category_name")
        .agg(

            products=(
                "product_key",
                "count"
            ),

            total_stock=(
                "stock_quantity",
                "sum"
            ),

            total_sales_volume=(
                "sales_volume",
                "sum"
            ),

            avg_turnover=(
                "inventory_turnover_rate",
                "mean"
            ),

            reorder_products=(
                "reorder_required",
                "sum"
            )
        )
        .reset_index()
    )

    # -----------------------------------------------------
    # REORDER RATE
    # -----------------------------------------------------

    result["reorder_rate"] = (
        result["reorder_products"]
        /
        result["products"]
        * 100
    )

    result = (
        result
        .sort_values(
            "reorder_rate",
            ascending=False
        )
        .reset_index(drop=True)
    )

    print("\n" + "=" * 60)
    print("CATEGORY INVENTORY RCA")
    print("=" * 60)

    print(
        result.to_string(
            index=False
        )
    )

    return result


# =========================================================
# CATEGORY RCA DEEP DIVE
# =========================================================

def category_rca_deep_dive(df):

    result = (
        df.groupby("category_name")
        .agg(

            # ---------------------------------------------
            # PRODUCT COUNT
            # ---------------------------------------------

            total_products=(
                "product_key",
                "count"
            ),

            # ---------------------------------------------
            # REORDER PRODUCTS
            # ---------------------------------------------

            reorder_products=(
                "reorder_required",
                "sum"
            ),

            # ---------------------------------------------
            # HIGH DEMAND + LOW STOCK
            # ---------------------------------------------

            high_demand_low_stock=(
                "rca_category",
                lambda x: (
                    x
                    ==
                    "High Demand + Low Stock"
                ).sum()
            ),

            # ---------------------------------------------
            # FAST TURNOVER + LOW STOCK
            # ---------------------------------------------

            fast_turnover_low_stock=(
                "rca_category",
                lambda x: (
                    x
                    ==
                    "Fast Turnover + Low Stock"
                ).sum()
            ),

            # ---------------------------------------------
            # TOTAL STOCK
            # ---------------------------------------------

            total_stock=(
                "stock_quantity",
                "sum"
            ),

            # ---------------------------------------------
            # TOTAL SALES VOLUME
            # ---------------------------------------------

            total_sales_volume=(
                "sales_volume",
                "sum"
            ),

            # ---------------------------------------------
            # AVERAGE TURNOVER
            # ---------------------------------------------

            avg_turnover=(
                "inventory_turnover_rate",
                "mean"
            ),

            # ---------------------------------------------
            # AVERAGE REORDER LEVEL
            # ---------------------------------------------

            avg_reorder_level=(
                "reorder_level",
                "mean"
            ),

            # ---------------------------------------------
            # AVERAGE STOCK
            # ---------------------------------------------

            avg_stock=(
                "stock_quantity",
                "mean"
            ),

            # ---------------------------------------------
            # AVERAGE STOCK GAP %
            # ---------------------------------------------

            avg_stock_gap_pct=(
                "stock_gap_pct",
                "mean"
            )
        )
        .reset_index()
    )

    # -----------------------------------------------------
    # REORDER RATE
    # -----------------------------------------------------

    result["reorder_rate"] = (
        result["reorder_products"]
        /
        result["total_products"]
        * 100
    )

    # -----------------------------------------------------
    # HIGH DEMAND RISK RATE
    # -----------------------------------------------------

    result["high_demand_risk_rate"] = (
        result["high_demand_low_stock"]
        /
        result["total_products"]
        * 100
    )

    # -----------------------------------------------------
    # FAST TURNOVER RISK RATE
    # -----------------------------------------------------

    result["fast_turnover_risk_rate"] = (
        result["fast_turnover_low_stock"]
        /
        result["total_products"]
        * 100
    )

    # -----------------------------------------------------
    # SORT
    # -----------------------------------------------------

    result = (
        result
        .sort_values(
            "reorder_rate",
            ascending=False
        )
        .reset_index(drop=True)
    )

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    print("\n" + "=" * 70)
    print("CATEGORY RCA DEEP DIVE")
    print("=" * 70)

    print(
        result[
            [
                "category_name",
                "total_products",
                "reorder_products",
                "reorder_rate",
                "high_demand_low_stock",
                "high_demand_risk_rate",
                "fast_turnover_low_stock",
                "fast_turnover_risk_rate",
                "avg_turnover",
                "avg_reorder_level",
                "avg_stock",
                "avg_stock_gap_pct"
            ]
        ]
        .to_string(
            index=False
        )
    )

    return result


# =========================================================
# SUPPLIER RCA
# =========================================================

def supplier_rca(df):

    result = (
        df.groupby("supplier_name")
        .agg(

            total_products=(
                "product_key",
                "count"
            ),

            reorder_products=(
                "reorder_required",
                "sum"
            ),

            total_sales_volume=(
                "sales_volume",
                "sum"
            ),

            avg_turnover=(
                "inventory_turnover_rate",
                "mean"
            ),

            avg_stock_gap_pct=(
                "stock_gap_pct",
                "mean"
            )
        )
        .reset_index()
    )

    result["reorder_rate"] = (
        result["reorder_products"]
        /
        result["total_products"]
        * 100
    )

    result = (
        result
        .sort_values(
            "reorder_rate",
            ascending=False
        )
        .reset_index(drop=True)
    )

    print("\n" + "=" * 60)
    print("SUPPLIER INVENTORY RCA")
    print("=" * 60)

    print(
        result.head(20)
        .to_string(
            index=False
        )
    )

    return result


# =========================================================
# WAREHOUSE RCA
# =========================================================

def warehouse_rca(df):

    result = (
        df.groupby("warehouse_location")
        .agg(

            total_products=(
                "product_key",
                "count"
            ),

            reorder_products=(
                "reorder_required",
                "sum"
            ),

            total_stock=(
                "stock_quantity",
                "sum"
            ),

            total_sales_volume=(
                "sales_volume",
                "sum"
            ),

            avg_turnover=(
                "inventory_turnover_rate",
                "mean"
            ),

            avg_stock_gap_pct=(
                "stock_gap_pct",
                "mean"
            )
        )
        .reset_index()
    )

    result["reorder_rate"] = (
        result["reorder_products"]
        /
        result["total_products"]
        * 100
    )

    result = (
        result
        .sort_values(
            "reorder_rate",
            ascending=False
        )
        .reset_index(drop=True)
    )

    print("\n" + "=" * 60)
    print("WAREHOUSE INVENTORY RCA")
    print("=" * 60)

    print(
        result.head(20)
        .to_string(
            index=False
        )
    )

    return result


# =========================================================
# MAIN
# =========================================================

def main():

    print("Starting Inventory RCA analysis...")

    # -----------------------------------------------------
    # LOAD
    # -----------------------------------------------------

    df = load_rca_data()

    # -----------------------------------------------------
    # INVENTORY PRESSURE
    # -----------------------------------------------------

    df = calculate_inventory_pressure(
        df
    )

    # -----------------------------------------------------
    # DEMAND CLASSIFICATION
    # -----------------------------------------------------

    df = classify_demand(
        df
    )

    # -----------------------------------------------------
    # RCA CLASSIFICATION
    # -----------------------------------------------------

    df = classify_inventory_risk(
        df
    )

    # -----------------------------------------------------
    # RCA SUMMARY
    # -----------------------------------------------------

    rca_summary(
        df
    )

    # -----------------------------------------------------
    # HIGH-PRIORITY PRODUCTS
    # -----------------------------------------------------

    high_priority_rca(
        df
    )

    # -----------------------------------------------------
    # CATEGORY RCA
    # -----------------------------------------------------

    category_rca(
        df
    )

    # -----------------------------------------------------
    # CATEGORY RCA DEEP DIVE
    # -----------------------------------------------------

    category_rca_deep_dive(
        df
    )

    # -----------------------------------------------------
    # SUPPLIER RCA
    # -----------------------------------------------------

    supplier_rca(
        df
    )

    # -----------------------------------------------------
    # WAREHOUSE RCA
    # -----------------------------------------------------

    warehouse_rca(
        df
    )

    print("\n" + "=" * 60)
    print("INVENTORY RCA ANALYSIS COMPLETED")
    print("=" * 60)


# =========================================================
# SCRIPT ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()