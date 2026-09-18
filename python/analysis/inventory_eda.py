import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from python.etl.config.database import get_engine


# =========================================================
# LOAD INVENTORY DATA
# =========================================================

def load_inventory_data():

    engine = get_engine()

    query = """
        SELECT
            fi.inventory_key,
            fi.product_key,
            fi.supplier_key,
            fi.warehouse_key,
            fi.stock_quantity,
            fi.reorder_level,
            fi.reorder_quantity,
            fi.sales_volume,
            fi.inventory_turnover_rate,

            p.product_id,
            p.product_name,
            p.category_key,

            s.supplier_id,
            s.supplier_name,

            w.warehouse_location

        FROM retail_dw.fact_inventory fi

        LEFT JOIN retail_dw.dim_product p
            ON fi.product_key = p.product_key

        LEFT JOIN retail_dw.dim_supplier s
            ON fi.supplier_key = s.supplier_key

        LEFT JOIN retail_dw.dim_warehouse w
            ON fi.warehouse_key = w.warehouse_key
    """

    print("Loading inventory data...")

    df = pd.read_sql(
        query,
        engine
    )

    print(
        "Inventory data loaded:",
        len(df),
        "rows"
    )

    return df


# =========================================================
# BASIC INVENTORY ANALYSIS
# =========================================================

def basic_inventory_analysis(df):

    print("\n" + "=" * 60)
    print("INVENTORY DATASET OVERVIEW")
    print("=" * 60)

    print(
        "Rows:",
        len(df)
    )

    print(
        "Columns:",
        len(df.columns)
    )

    print("\nColumns:")

    print(
        df.columns.tolist()
    )

    print("\nData Types:")

    print(
        df.dtypes
    )

    print("\nMissing Values:")

    print(
        df.isnull().sum()
    )

    print("\nDuplicate Rows:")

    print(
        df.duplicated().sum()
    )


# =========================================================
# INVENTORY KPIs
# =========================================================

def inventory_kpis(df):

    total_stock = (
        df["stock_quantity"]
        .sum()
    )

    total_sales_volume = (
        df["sales_volume"]
        .sum()
    )

    average_turnover = (
        df["inventory_turnover_rate"]
        .mean()
    )

    products_below_reorder = (
        df["stock_quantity"]
        <
        df["reorder_level"]
    ).sum()

    total_products = (
        df["product_key"]
        .nunique()
    )

    risk_percentage = (
        products_below_reorder
        /
        total_products
        * 100
    )

    print("\n" + "=" * 60)
    print("INVENTORY KPIs")
    print("=" * 60)

    print(
        f"Total Stock Quantity     : "
        f"{total_stock:,.0f}"
    )

    print(
        f"Total Sales Volume       : "
        f"{total_sales_volume:,.0f}"
    )

    print(
        f"Average Turnover Rate    : "
        f"{average_turnover:.2f}"
    )

    print(
        f"Products Below Reorder   : "
        f"{products_below_reorder:,}"
    )

    print(
        f"Total Products           : "
        f"{total_products:,}"
    )

    print(
        f"Reorder Risk %           : "
        f"{risk_percentage:.2f}%"
    )


# =========================================================
# REORDER RISK ANALYSIS
# =========================================================

def reorder_risk_analysis(df):

    result = df.copy()

    result["reorder_status"] = np.where(
        result["stock_quantity"]
        <
        result["reorder_level"],
        "Reorder Required",
        "Stock Sufficient"
    )

    summary = (
        result["reorder_status"]
        .value_counts()
    )

    print("\n" + "=" * 60)
    print("REORDER RISK ANALYSIS")
    print("=" * 60)

    print(summary)

    return result


# =========================================================
# SUPPLIER RISK ANALYSIS
# =========================================================

def supplier_risk_analysis(df):

    result = df.copy()

    result["reorder_required"] = (
        result["stock_quantity"]
        <
        result["reorder_level"]
    )

    supplier = (
        result
        .groupby("supplier_name")
        .agg(
            total_products=(
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
            reorder_required=(
                "reorder_required",
                "sum"
            )
        )
        .reset_index()
    )

    supplier["reorder_rate"] = (
        supplier["reorder_required"]
        /
        supplier["total_products"]
        * 100
    )

    supplier = (
        supplier
        .sort_values(
            "reorder_rate",
            ascending=False
        )
    )

    print("\n" + "=" * 60)
    print("SUPPLIER INVENTORY RISK")
    print("=" * 60)

    print(
        supplier.to_string(
            index=False
        )
    )

    return supplier


# =========================================================
# WAREHOUSE RISK ANALYSIS
# =========================================================

def warehouse_risk_analysis(df):

    result = df.copy()

    result["reorder_required"] = (
        result["stock_quantity"]
        <
        result["reorder_level"]
    )

    warehouse = (
        result
        .groupby("warehouse_location")
        .agg(
            total_products=(
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
            reorder_required=(
                "reorder_required",
                "sum"
            )
        )
        .reset_index()
    )

    warehouse["reorder_rate"] = (
        warehouse["reorder_required"]
        /
        warehouse["total_products"]
        * 100
    )

    warehouse = (
        warehouse
        .sort_values(
            "reorder_rate",
            ascending=False
        )
    )

    print("\n" + "=" * 60)
    print("WAREHOUSE INVENTORY RISK")
    print("=" * 60)

    print(
        warehouse.to_string(
            index=False
        )
    )

    return warehouse


# =========================================================
# HIGH-RISK PRODUCTS
# =========================================================

def high_risk_products(df):

    result = df.copy()

    result["reorder_required"] = (
        result["stock_quantity"]
        <
        result["reorder_level"]
    )

    high_risk = (
        result[
            result["reorder_required"]
        ]
        .sort_values(
            [
                "sales_volume",
                "inventory_turnover_rate"
            ],
            ascending=False
        )
        [
            [
                "product_id",
                "product_name",
                "stock_quantity",
                "reorder_level",
                "reorder_quantity",
                "sales_volume",
                "inventory_turnover_rate",
                "supplier_name",
                "warehouse_location"
            ]
        ]
        .head(20)
    )

    print("\n" + "=" * 60)
    print("HIGH-RISK PRODUCTS BY DEMAND")
    print("=" * 60)

    print(
        high_risk.to_string(
            index=False
        )
    )

    return high_risk


# =========================================================
# INVENTORY RISK SCORE
# =========================================================

def inventory_risk_score(df):

    result = df.copy()

    # -----------------------------------------------------
    # STOCK GAP
    # -----------------------------------------------------

    result["stock_gap"] = (
        result["reorder_level"]
        -
        result["stock_quantity"]
    )

    # Positive stock_gap means the product
    # is below its reorder level.

    # -----------------------------------------------------
    # STOCK GAP PERCENTAGE
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

    # A negative value means stock is above
    # the reorder level.

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

    # -----------------------------------------------------
    # DEMAND PERCENTILE
    # -----------------------------------------------------

    result["demand_percentile"] = (
        result["sales_volume"]
        .rank(
            pct=True
        )
        * 100
    )

    # -----------------------------------------------------
    # TURNOVER PERCENTILE
    # -----------------------------------------------------

    result["turnover_percentile"] = (
        result["inventory_turnover_rate"]
        .rank(
            pct=True
        )
        * 100
    )

    # -----------------------------------------------------
    # RISK COMPONENTS
    # -----------------------------------------------------

    # Stock risk:
    # Maximum contribution = 50 points
    #
    # A product 100% or more below reorder
    # receives the full 50 points.

    stock_risk = (
        result["stock_gap_pct"]
        .clip(
            lower=0,
            upper=100
        )
        * 0.50
    )

    # Demand risk:
    # Maximum contribution = 30 points

    demand_risk = (
        result["demand_percentile"]
        * 0.30
    )

    # Turnover risk:
    # Maximum contribution = 20 points

    turnover_risk = (
        result["turnover_percentile"]
        * 0.20
    )

    # -----------------------------------------------------
    # FINAL RISK SCORE
    # -----------------------------------------------------

    result["risk_score"] = (
        stock_risk
        +
        demand_risk
        +
        turnover_risk
    )

    result["risk_score"] = (
        result["risk_score"]
        .round(2)
    )

    # -----------------------------------------------------
    # RISK CATEGORY
    # -----------------------------------------------------

    result["risk_category"] = np.select(
        [
            result["risk_score"] >= 70,
            result["risk_score"] >= 40
        ],
        [
            "High Risk",
            "Medium Risk"
        ],
        default="Low Risk"
    )

    # -----------------------------------------------------
    # PRINT SUMMARY
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("INVENTORY RISK SCORE ANALYSIS")
    print("=" * 60)

    print(
        "Risk Score Components:"
    )

    print(
        "Stock Gap Risk     : 50%"
    )

    print(
        "Demand Risk        : 30%"
    )

    print(
        "Turnover Risk      : 20%"
    )

    print("\nRisk Categories:")

    risk_summary = (
        result["risk_category"]
        .value_counts()
    )

    print(
        risk_summary
    )

    print("\nRisk Percentage:")

    risk_percentage = (
        result["risk_category"]
        .value_counts(
            normalize=True
        )
        * 100
    )

    print(
        risk_percentage.round(2)
    )

    return result


# =========================================================
# INVENTORY RCA
# =========================================================

def inventory_rca(df):

    high_risk = (
        df[
            df["risk_category"]
            ==
            "High Risk"
        ]
        .sort_values(
            [
                "risk_score",
                "stock_gap_pct",
                "sales_volume"
            ],
            ascending=False
        )
    )

    print("\n" + "=" * 60)
    print("HIGH-RISK INVENTORY RCA")
    print("=" * 60)

    columns = [
        "product_id",
        "product_name",
        "stock_quantity",
        "reorder_level",
        "stock_gap",
        "stock_gap_pct",
        "sales_volume",
        "inventory_turnover_rate",
        "demand_percentile",
        "turnover_percentile",
        "supplier_name",
        "warehouse_location",
        "risk_score",
        "risk_category"
    ]

    print(
        high_risk[
            columns
        ]
        .head(30)
        .to_string(
            index=False
        )
    )

    return high_risk


# =========================================================
# MATPLOTLIB
# REORDER RISK
# =========================================================

def plot_reorder_risk(df):

    result = df.copy()

    result["reorder_status"] = np.where(
        result["stock_quantity"]
        <
        result["reorder_level"],
        "Reorder Required",
        "Stock Sufficient"
    )

    summary = (
        result["reorder_status"]
        .value_counts()
    )

    plt.figure(
        figsize=(8, 6)
    )

    plt.bar(
        summary.index,
        summary.values
    )

    plt.title(
        "Inventory Reorder Risk"
    )

    plt.xlabel(
        "Inventory Status"
    )

    plt.ylabel(
        "Number of Products"
    )

    for i, value in enumerate(
        summary.values
    ):

        plt.text(
            i,
            value + 10,
            f"{value:,}",
            ha="center"
        )

    plt.tight_layout()

    plt.show()


# =========================================================
# MATPLOTLIB
# STOCK VS REORDER LEVEL
# =========================================================

def plot_stock_vs_reorder_level(df):

    plt.figure(
        figsize=(10, 7)
    )

    plt.scatter(
        df["reorder_level"],
        df["stock_quantity"],
        alpha=0.6
    )

    max_value = max(
        df["reorder_level"].max(),
        df["stock_quantity"].max()
    )

    plt.plot(
        [0, max_value],
        [0, max_value],
        linestyle="--",
        label="Reorder Threshold"
    )

    plt.title(
        "Stock Quantity vs Reorder Level"
    )

    plt.xlabel(
        "Reorder Level"
    )

    plt.ylabel(
        "Current Stock Quantity"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plt.show()


# =========================================================
# MATPLOTLIB
# SALES VOLUME VS TURNOVER
# =========================================================

def plot_sales_vs_turnover(df):

    plt.figure(
        figsize=(10, 7)
    )

    plt.scatter(
        df["sales_volume"],
        df["inventory_turnover_rate"],
        alpha=0.6
    )

    plt.title(
        "Sales Volume vs Inventory Turnover Rate"
    )

    plt.xlabel(
        "Sales Volume"
    )

    plt.ylabel(
        "Inventory Turnover Rate"
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plt.show()


# =========================================================
# MATPLOTLIB
# SUPPLIER RISK
# =========================================================

def plot_supplier_risk(df):

    result = df.copy()

    result["reorder_required"] = (
        result["stock_quantity"]
        <
        result["reorder_level"]
    )

    supplier = (
        result
        .groupby("supplier_name")
        .agg(
            total_products=(
                "product_key",
                "count"
            ),
            reorder_required=(
                "reorder_required",
                "sum"
            )
        )
        .reset_index()
    )

    supplier["reorder_rate"] = (
        supplier["reorder_required"]
        /
        supplier["total_products"]
        * 100
    )

    supplier = (
        supplier
        .sort_values(
            "reorder_rate",
            ascending=False
        )
        .head(15)
    )

    plt.figure(
        figsize=(12, 7)
    )

    plt.barh(
        supplier["supplier_name"],
        supplier["reorder_rate"]
    )

    plt.title(
        "Top 15 Suppliers by Reorder Risk"
    )

    plt.xlabel(
        "Reorder Rate (%)"
    )

    plt.ylabel(
        "Supplier"
    )

    plt.gca().invert_yaxis()

    plt.tight_layout()

    plt.show()


# =========================================================
# MATPLOTLIB
# WAREHOUSE RISK
# =========================================================

def plot_warehouse_risk(df):

    result = df.copy()

    result["reorder_required"] = (
        result["stock_quantity"]
        <
        result["reorder_level"]
    )

    warehouse = (
        result
        .groupby("warehouse_location")
        .agg(
            total_products=(
                "product_key",
                "count"
            ),
            reorder_required=(
                "reorder_required",
                "sum"
            )
        )
        .reset_index()
    )

    warehouse["reorder_rate"] = (
        warehouse["reorder_required"]
        /
        warehouse["total_products"]
        * 100
    )

    warehouse = (
        warehouse
        .sort_values(
            "reorder_rate",
            ascending=False
        )
        .head(15)
    )

    plt.figure(
        figsize=(12, 7)
    )

    plt.barh(
        warehouse["warehouse_location"],
        warehouse["reorder_rate"]
    )

    plt.title(
        "Top 15 Warehouses by Reorder Risk"
    )

    plt.xlabel(
        "Reorder Rate (%)"
    )

    plt.ylabel(
        "Warehouse"
    )

    plt.gca().invert_yaxis()

    plt.tight_layout()

    plt.show()


# =========================================================
# MATPLOTLIB
# HIGH-RISK PRODUCTS
# =========================================================

def plot_high_risk_products(df):

    result = df.copy()

    result["reorder_required"] = (
        result["stock_quantity"]
        <
        result["reorder_level"]
    )

    high_risk = (
        result[
            result["reorder_required"]
        ]
        .sort_values(
            "sales_volume",
            ascending=False
        )
        .head(15)
    )

    plt.figure(
        figsize=(12, 7)
    )

    plt.barh(
        high_risk["product_name"],
        high_risk["sales_volume"]
    )

    plt.title(
        "Top High-Risk Products by Sales Volume"
    )

    plt.xlabel(
        "Sales Volume"
    )

    plt.ylabel(
        "Product"
    )

    plt.gca().invert_yaxis()

    plt.tight_layout()

    plt.show()


# =========================================================
# MAIN
# =========================================================

def main():

    df = load_inventory_data()

    # -----------------------------------------------------
    # BASIC ANALYSIS
    # -----------------------------------------------------

    basic_inventory_analysis(
        df
    )

    # -----------------------------------------------------
    # INVENTORY KPIs
    # -----------------------------------------------------

    inventory_kpis(
        df
    )

    # -----------------------------------------------------
    # REORDER ANALYSIS
    # -----------------------------------------------------

    df = reorder_risk_analysis(
        df
    )

    # -----------------------------------------------------
    # SUPPLIER ANALYSIS
    # -----------------------------------------------------

    supplier_risk_analysis(
        df
    )

    # -----------------------------------------------------
    # WAREHOUSE ANALYSIS
    # -----------------------------------------------------

    warehouse_risk_analysis(
        df
    )

    # -----------------------------------------------------
    # HIGH-RISK PRODUCTS
    # -----------------------------------------------------

    high_risk_products(
        df
    )

    # -----------------------------------------------------
    # RISK SCORING
    # -----------------------------------------------------

    df = inventory_risk_score(
        df
    )

    # -----------------------------------------------------
    # RCA
    # -----------------------------------------------------

    inventory_rca(
        df
    )

    # -----------------------------------------------------
    # MATPLOTLIB ANALYSIS
    # -----------------------------------------------------

    plot_reorder_risk(
        df
    )

    plot_stock_vs_reorder_level(
        df
    )

    plot_sales_vs_turnover(
        df
    )

    plot_supplier_risk(
        df
    )

    plot_warehouse_risk(
        df
    )

    plot_high_risk_products(
        df
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()