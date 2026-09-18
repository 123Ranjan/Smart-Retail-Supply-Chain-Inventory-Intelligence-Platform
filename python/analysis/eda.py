import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from python.etl.config.database import get_engine

def load_sales_data():
    engine = get_engine()

    query = """
    SELECT
        f.order_id,
        f.quantity,
        f.sales,
        f.profit,
        f.discount,
        f.shipping_cost,
        f.order_priority,
        d.full_date,
        d.year,
        d.month,
        d.month_name,
        p.product_id,
        p.product_name,
        c.category_name,
        c.sub_category_name,
        g.country,
        g.market,
        g.region,
        g.state,
        g.city,
        sm.ship_mode
    FROM retail_dw.fact_sales f

    JOIN retail_dw.dim_date d
        ON f.date_key = d.date_key

    JOIN retail_dw.dim_product p
        ON f.product_key = p.product_key

    JOIN retail_dw.dim_category c
        ON p.category_key = c.category_key

    JOIN retail_dw.dim_geography g
        ON f.geography_key = g.geography_key

    JOIN retail_dw.dim_ship_mode sm
        ON f.ship_mode_key = sm.ship_mode_key;
    """

    return pd.read_sql(query, engine)


def basic_analysis(df):

    print("\n" + "=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)

    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nNumerical Summary:")
    print(
        df[
            [
                "quantity",
                "sales",
                "profit",
                "discount",
                "shipping_cost"
            ]
        ].describe()
    )


def business_kpis(df):

    total_sales = df["sales"].sum()
    total_profit = df["profit"].sum()
    total_quantity = df["quantity"].sum()
    total_orders = df["order_id"].nunique()

    profit_margin = (
        total_profit / total_sales
        if total_sales != 0
        else 0
    )

    average_order_value = (
        total_sales / total_orders
        if total_orders != 0
        else 0
    )

    print("\n" + "=" * 60)
    print("BUSINESS KPIs")
    print("=" * 60)

    print(f"Total Sales       : {total_sales:,.2f}")
    print(f"Total Profit      : {total_profit:,.2f}")
    print(f"Total Quantity    : {total_quantity:,}")
    print(f"Total Orders      : {total_orders:,}")
    print(f"Profit Margin     : {profit_margin:.2%}")
    print(f"Average Order Value: {average_order_value:,.2f}")


def sales_by_category(df):

    result = (
        df.groupby("category_name")
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            total_quantity=("quantity", "sum")
        )
        .sort_values(
            "total_sales",
            ascending=False
        )
    )

    print("\n" + "=" * 60)
    print("SALES BY CATEGORY")
    print("=" * 60)

    print(result)

    return result


def sales_by_region(df):

    result = (
        df.groupby("region")
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            total_quantity=("quantity", "sum")
        )
        .sort_values(
            "total_sales",
            ascending=False
        )
    )

    print("\n" + "=" * 60)
    print("SALES BY REGION")
    print("=" * 60)

    print(result)

    return result


def profit_by_category(df):

    result = (
        df.groupby("category_name")
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum")
        )
    )

    result["profit_margin"] = (
        result["total_profit"]
        / result["total_sales"]
    )

    result = result.sort_values(
        "total_profit",
        ascending=False
    )

    print("\n" + "=" * 60)
    print("PROFIT ANALYSIS BY CATEGORY")
    print("=" * 60)

    print(result)

    return result


def monthly_sales(df):

    result = (
        df.groupby("full_date")
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum")
        )
        .reset_index()
    )

    return result


def plot_monthly_sales(df):

    monthly = monthly_sales(df)

    plt.figure(figsize=(12, 6))

    plt.plot(
        monthly["full_date"],
        monthly["total_sales"]
    )

    plt.title("Sales Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Sales")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def plot_profit_distribution(df):

    plt.figure(figsize=(10, 6))

    plt.hist(
        df["profit"],
        bins=50
    )

    plt.title("Profit Distribution")
    plt.xlabel("Profit")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()


def discount_profit_analysis(df):

    result = (
        df.groupby("discount")
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            transactions=("order_id", "count")
        )
        .reset_index()
    )

    result["profit_margin"] = (
        result["total_profit"]
        / result["total_sales"]
    )

    print("\n" + "=" * 60)
    print("DISCOUNT VS PROFIT ANALYSIS")
    print("=" * 60)

    print(result)

    return result

def profit_statistics(df):

    profit = df["profit"].dropna().to_numpy()

    q1 = np.percentile(profit, 25)
    median = np.median(profit)
    q3 = np.percentile(profit, 75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = df[
        (df["profit"] < lower_bound) |
        (df["profit"] > upper_bound)
    ]

    print("\n" + "=" * 60)
    print("NUMPY PROFIT STATISTICAL ANALYSIS")
    print("=" * 60)

    print(f"Mean Profit       : {np.mean(profit):,.2f}")
    print(f"Median Profit     : {median:,.2f}")
    print(f"Std Deviation     : {np.std(profit):,.2f}")
    print(f"Q1                : {q1:,.2f}")
    print(f"Q3                : {q3:,.2f}")
    print(f"IQR               : {iqr:,.2f}")
    print(f"Lower Bound       : {lower_bound:,.2f}")
    print(f"Upper Bound       : {upper_bound:,.2f}")
    print(f"Outlier Rows      : {len(outliers):,}")

    return outliers


def extreme_profit_analysis(df):

    print("\n" + "=" * 60)
    print("EXTREME PROFIT / LOSS TRANSACTIONS")
    print("=" * 60)

    extreme = (
        df[
            [
                "order_id",
                "product_name",
                "category_name",
                "sub_category_name",
                "region",
                "discount",
                "sales",
                "shipping_cost",
                "profit"
            ]
        ]
        .sort_values("profit")
        .head(20)
    )

    print(extreme.to_string(index=False))

    return extreme


def plot_discount_vs_profit(df):

    result = (
        df.groupby("discount")
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            transactions=("order_id", "count")
        )
        .reset_index()
        .sort_values("discount")
    )

    result["profit_margin"] = (
        result["total_profit"] /
        result["total_sales"]
    )

    fig, ax1 = plt.subplots(
        figsize=(12, 6)
    )

    # -----------------------------------------
    # Profit Margin
    # -----------------------------------------

    ax1.plot(
        result["discount"] * 100,
        result["profit_margin"] * 100,
        marker="o",
        linewidth=2,
        label="Profit Margin"
    )

    ax1.axhline(
        y=0,
        linestyle="--"
    )

    ax1.set_xlabel(
        "Discount (%)"
    )

    ax1.set_ylabel(
        "Profit Margin (%)"
    )

    ax1.set_title(
        "Discount vs Profitability"
    )

    ax1.grid(
        True,
        alpha=0.3
    )

    # -----------------------------------------
    # Sales Volume
    # -----------------------------------------

    ax2 = ax1.twinx()

    ax2.bar(
        result["discount"] * 100,
        result["total_sales"],
        width=1.5,
        alpha=0.25,
        label="Sales"
    )

    ax2.set_ylabel(
        "Total Sales"
    )

    # -----------------------------------------
    # Final Layout
    # -----------------------------------------

    fig.tight_layout()

    plt.show()


def plot_category_performance(df):

    result = (
        df.groupby("category_name")
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum")
        )
        .reset_index()
    )

    result["profit_margin"] = (
        result["total_profit"] /
        result["total_sales"]
    )

    result = result.sort_values(
        "profit_margin",
        ascending=True
    )

    x = np.arange(len(result))
    width = 0.35

    fig, ax1 = plt.subplots(
        figsize=(11, 6)
    )

    # -----------------------------------------
    # Sales
    # -----------------------------------------

    ax1.bar(
        x - width / 2,
        result["total_sales"],
        width,
        label="Sales"
    )

    ax1.set_xlabel(
        "Category"
    )

    ax1.set_ylabel(
        "Total Sales"
    )

    ax1.set_xticks(x)

    ax1.set_xticklabels(
        result["category_name"]
    )

    # -----------------------------------------
    # Profit Margin
    # -----------------------------------------

    ax2 = ax1.twinx()

    ax2.bar(
        x + width / 2,
        result["profit_margin"] * 100,
        width,
        alpha=0.7,
        label="Profit Margin"
    )

    ax2.set_ylabel(
        "Profit Margin (%)"
    )

    ax2.axhline(
        0,
        linestyle="--"
    )

    # -----------------------------------------
    # Title
    # -----------------------------------------

    plt.title(
        "Category Sales vs Profit Margin"
    )

    # -----------------------------------------
    # Combined Legend
    # -----------------------------------------

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(
        handles1 + handles2,
        labels1 + labels2,
        loc="upper left"
    )

    plt.tight_layout()
    plt.show()

def plot_region_performance(df):

    result = (
        df.groupby("region")
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum")
        )
        .reset_index()
    )

    result["profit_margin"] = (
        result["total_profit"] /
        result["total_sales"]
    )

    # Sort by profitability
    result = result.sort_values(
        "profit_margin",
        ascending=True
    )

    y = np.arange(len(result))
    height = 0.35

    fig, ax1 = plt.subplots(
        figsize=(14, 8)
    )

    # -----------------------------------------
    # Total Sales
    # -----------------------------------------

    ax1.barh(
        y - height / 2,
        result["total_sales"],
        height,
        label="Sales"
    )

    ax1.set_xlabel(
        "Total Sales"
    )

    ax1.set_ylabel(
        "Region"
    )

    ax1.set_yticks(y)

    ax1.set_yticklabels(
        result["region"]
    )

    # -----------------------------------------
    # Profit Margin
    # -----------------------------------------

    ax2 = ax1.twiny()

    ax2.barh(
        y + height / 2,
        result["profit_margin"] * 100,
        height,
        alpha=0.7,
        label="Profit Margin"
    )

    ax2.set_xlabel(
        "Profit Margin (%)"
    )

    ax2.axvline(
        0,
        linestyle="--"
    )

    # -----------------------------------------
    # Title
    # -----------------------------------------

    plt.title(
        "Regional Sales vs Profitability"
    )

    # -----------------------------------------
    # Combined Legend
    # -----------------------------------------

    handles1, labels1 = (
        ax1.get_legend_handles_labels()
    )

    handles2, labels2 = (
        ax2.get_legend_handles_labels()
    )

    ax1.legend(
        handles1 + handles2,
        labels1 + labels2,
        loc="lower right"
    )

    plt.tight_layout()
    plt.show()

def plot_profit_distribution_with_outliers(df):

    profit = (
        df["profit"]
        .dropna()
        .to_numpy()
    )

    # =========================================================
    # NUMPY OUTLIER CALCULATION
    # =========================================================

    q1 = np.percentile(
        profit,
        25
    )

    median = np.median(
        profit
    )

    q3 = np.percentile(
        profit,
        75
    )

    iqr = q3 - q1

    lower_bound = (
        q1 - 1.5 * iqr
    )

    upper_bound = (
        q3 + 1.5 * iqr
    )

    # =========================================================
    # OUTLIER COUNTS
    # =========================================================

    lower_outliers = np.sum(
        profit < lower_bound
    )

    upper_outliers = np.sum(
        profit > upper_bound
    )

    total_outliers = (
        lower_outliers +
        upper_outliers
    )

    # =========================================================
    # CREATE FIGURE
    # =========================================================

    fig, ax = plt.subplots(
        figsize=(13, 7)
    )

    # =========================================================
    # HISTOGRAM
    # =========================================================

    ax.hist(
        profit,
        bins=100
    )

    # =========================================================
    # MEDIAN
    # =========================================================

    ax.axvline(
        median,
        linestyle="-",
        linewidth=2,
        label=f"Median: {median:.2f}"
    )

    # =========================================================
    # LOWER OUTLIER BOUNDARY
    # =========================================================

    ax.axvline(
        lower_bound,
        linestyle="--",
        linewidth=2,
        label=f"Lower Bound: {lower_bound:.2f}"
    )

    # =========================================================
    # UPPER OUTLIER BOUNDARY
    # =========================================================

    ax.axvline(
        upper_bound,
        linestyle="--",
        linewidth=2,
        label=f"Upper Bound: {upper_bound:.2f}"
    )

    # =========================================================
    # ZERO PROFIT LINE
    # =========================================================

    ax.axvline(
        0,
        linestyle=":",
        linewidth=2,
        label="Break-even: 0"
    )

    # =========================================================
    # TITLES
    # =========================================================

    ax.set_title(
        "Profit Distribution and Statistical Outliers",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel(
        "Profit"
    )

    ax.set_ylabel(
        "Frequency"
    )

    # =========================================================
    # INFORMATION BOX
    # =========================================================

    statistics_text = (
        f"Mean: {np.mean(profit):,.2f}\n"
        f"Median: {median:,.2f}\n"
        f"Q1: {q1:,.2f}\n"
        f"Q3: {q3:,.2f}\n"
        f"IQR: {iqr:,.2f}\n"
        f"Lower Outliers: {lower_outliers:,}\n"
        f"Upper Outliers: {upper_outliers:,}\n"
        f"Total Outliers: {total_outliers:,}"
    )

    ax.text(
        0.98,
        0.97,
        statistics_text,
        transform=ax.transAxes,
        verticalalignment="top",
        horizontalalignment="right",
        fontsize=9,
        bbox=dict(
            boxstyle="round",
            alpha=0.8
        )
    )

    ax.legend()

    ax.grid(
        axis="y",
        alpha=0.3
    )

    plt.tight_layout()

    plt.show()

def main():

    print("Loading sales data...")

    df = load_sales_data()

    print("Sales data loaded:", len(df), "rows")

    # BASIC EDA

    basic_analysis(df)

    # BUSINESS KPIs

    business_kpis(df)

    # BUSINESS ANALYSIS

    sales_by_category(df)

    sales_by_region(df)

    profit_by_category(df)

    discount_profit_analysis(df)

    # NUMPY STATISTICAL ANALYSIS

    profit_statistics(df)

    extreme_profit_analysis(df)

    # MATPLOTLIB EDA VISUALIZATIONS
    plot_monthly_sales(df)

    plot_profit_distribution(df)

    plot_discount_vs_profit(df)

    plot_category_performance(df)

    plot_region_performance(df)

    plot_profit_distribution_with_outliers(df)


if __name__ == "__main__":
    main()