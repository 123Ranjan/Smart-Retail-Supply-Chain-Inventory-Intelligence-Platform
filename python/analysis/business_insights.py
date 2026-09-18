import pandas as pd
import numpy as np

from python.etl.config.database import get_engine


# =========================================================
# LOAD INVENTORY RCA DATA
# =========================================================

def load_inventory_data():

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

            c.category_name

        FROM retail_dw.fact_inventory fi

        LEFT JOIN retail_dw.dim_product p
            ON fi.product_key = p.product_key

        LEFT JOIN retail_dw.dim_category c
            ON p.category_key = c.category_key
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
# CALCULATE INVENTORY METRICS
# =========================================================

def calculate_metrics(df):

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
    # DEMAND THRESHOLD
    # -----------------------------------------------------

    demand_threshold = np.percentile(
        result["sales_volume"],
        75
    )

    # -----------------------------------------------------
    # TURNOVER THRESHOLD
    # -----------------------------------------------------

    turnover_threshold = (
        result["inventory_turnover_rate"]
        .median()
    )

    # -----------------------------------------------------
    # DEMAND LEVEL
    # -----------------------------------------------------

    result["demand_level"] = np.select(
        [
            result["sales_volume"]
            >= demand_threshold,

            result["sales_volume"]
            >= result["sales_volume"].median()
        ],

        [
            "High Demand",
            "Medium Demand"
        ],

        default="Low Demand"
    )

    # -----------------------------------------------------
    # RCA CATEGORY
    # -----------------------------------------------------

    result["rca_category"] = np.select(
        [
            (
                result["reorder_required"]
                &
                (
                    result["demand_level"]
                    == "High Demand"
                )
            ),

            (
                result["reorder_required"]
                &
                (
                    result["inventory_turnover_rate"]
                    >= turnover_threshold
                )
            ),

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
# EXECUTIVE KPIs
# =========================================================

def executive_kpis(df):

    total_products = (
        df["product_key"]
        .nunique()
    )

    reorder_products = (
        df["reorder_required"]
        .sum()
    )

    high_demand_risk = (
        df["rca_category"]
        ==
        "High Demand + Low Stock"
    ).sum()

    fast_turnover_risk = (
        df["rca_category"]
        ==
        "Fast Turnover + Low Stock"
    ).sum()

    total_stock_gap = (
        df.loc[
            df["reorder_required"],
            "stock_gap"
        ]
        .sum()
    )

    average_stock_gap = (
        df.loc[
            df["reorder_required"],
            "stock_gap_pct"
        ]
        .mean()
    )

    print("\n" + "=" * 65)
    print("EXECUTIVE INVENTORY INSIGHTS")
    print("=" * 65)

    print(
        f"Total Products             : "
        f"{total_products:,}"
    )

    print(
        f"Products Requiring Reorder : "
        f"{reorder_products:,}"
    )

    print(
        f"Overall Reorder Risk       : "
        f"{reorder_products / total_products * 100:.2f}%"
    )

    print(
        f"High Demand + Low Stock    : "
        f"{high_demand_risk:,}"
    )

    print(
        f"Fast Turnover + Low Stock  : "
        f"{fast_turnover_risk:,}"
    )

    print(
        f"Total Stock Gap            : "
        f"{total_stock_gap:,.0f}"
    )

    print(
        f"Average Stock Gap %        : "
        f"{average_stock_gap:.2f}%"
    )


# =========================================================
# TOP RISK CATEGORIES
# =========================================================

def top_risk_categories(df):

    result = (
        df.groupby("category_name")
        .agg(
            products=(
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

    print("\n" + "=" * 65)
    print("TOP RISK CATEGORIES")
    print("=" * 65)

    print(
        result.to_string(
            index=False
        )
    )

    return result


# =========================================================
# TOP PRIORITY PRODUCTS
# =========================================================

def top_priority_products(df):

    result = (
        df[
            df["reorder_required"]
        ]
        .copy()
    )

    # -----------------------------------------------------
    # PRIORITY SCORE
    # -----------------------------------------------------

    result["priority_score"] = (
        result["stock_gap_pct"] * 0.5
        +
        (
            result["sales_volume"]
            /
            result["sales_volume"].max()
            * 100
        ) * 0.3
        +
        (
            result["inventory_turnover_rate"]
            /
            result["inventory_turnover_rate"].max()
            * 100
        ) * 0.2
    )

    result = (
        result
        .sort_values(
            "priority_score",
            ascending=False
        )
        .reset_index(drop=True)
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
        "rca_category",
        "priority_score"
    ]

    print("\n" + "=" * 65)
    print("TOP PRIORITY PRODUCTS")
    print("=" * 65)

    print(
        result[
            columns
        ]
        .head(20)
        .to_string(
            index=False
        )
    )

    return result


# =========================================================
# BUSINESS RECOMMENDATIONS
# =========================================================

def generate_recommendations(
    df,
    category_result
):

    print("\n" + "=" * 65)
    print("BUSINESS RECOMMENDATIONS")
    print("=" * 65)

    # -----------------------------------------------------
    # TOP CATEGORY
    # -----------------------------------------------------

    top_category = (
        category_result
        .iloc[0]["category_name"]
    )

    top_category_rate = (
        category_result
        .iloc[0]["reorder_rate"]
    )

    print(
        f"1. Prioritize {top_category}, "
        f"which has the highest reorder rate "
        f"at {top_category_rate:.2f}%."
    )

    # -----------------------------------------------------
    # HIGH DEMAND RISK
    # -----------------------------------------------------

    high_demand_count = (
        (
            df["rca_category"]
            ==
            "High Demand + Low Stock"
        )
        .sum()
    )

    print(
        f"2. Immediately review the "
        f"{high_demand_count:,} high-demand "
        f"products currently below reorder level."
    )

    # -----------------------------------------------------
    # FAST TURNOVER
    # -----------------------------------------------------

    fast_turnover_count = (
        (
            df["rca_category"]
            ==
            "Fast Turnover + Low Stock"
        )
        .sum()
    )

    print(
        f"3. Increase replenishment attention "
        f"for {fast_turnover_count:,} products "
        f"with fast turnover and insufficient stock."
    )

    # -----------------------------------------------------
    # DATA-DRIVEN WARNING
    # -----------------------------------------------------

    print(
        "4. Supplier and warehouse-level RCA "
        "should not be treated as a primary "
        "business conclusion until those "
        "dimensions contain enough repeated "
        "entities for meaningful comparison."
    )


# =========================================================
# MAIN
# =========================================================

def main():

    print(
        "Starting Business Insights analysis..."
    )

    df = load_inventory_data()

    df = calculate_metrics(
        df
    )

    executive_kpis(
        df
    )

    category_result = (
        top_risk_categories(
            df
        )
    )

    top_priority_products(
        df
    )

    generate_recommendations(
        df,
        category_result
    )

    print("\n" + "=" * 65)
    print(
        "BUSINESS INSIGHTS ANALYSIS COMPLETED"
    )
    print("=" * 65)


if __name__ == "__main__":
    main()