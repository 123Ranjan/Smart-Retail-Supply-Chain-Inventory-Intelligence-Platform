"""
Data Cleaning Pipeline
Smart Retail Supply Chain & Inventory Intelligence Platform

Reads raw CSV/Excel datasets from:
    data/raw/

Writes cleaned datasets to:
    data/processed/

The original column names are preserved so the existing ETL pipeline
can consume the cleaned files with minimal changes.
"""

from pathlib import Path

import pandas as pd


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# Create processed directory if it does not exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# FILE PATHS
# =========================================================

SUPERSTORE_RAW = RAW_DIR / "superstore.csv"

INVENTORY_RAW = (
    RAW_DIR / "Grocery_Inventory_and_Sales_Dataset.csv"
)

RETURNS_RAW = (
    RAW_DIR / "Superstore Dataset.xlsx"
)

SUPERSTORE_OUTPUT = (
    PROCESSED_DIR / "superstore_cleaned.csv"
)

INVENTORY_OUTPUT = (
    PROCESSED_DIR / "inventory_cleaned.csv"
)

RETURNS_OUTPUT = (
    PROCESSED_DIR / "returns_cleaned.csv"
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove unnecessary whitespace from text columns.

    Empty strings are converted to missing values.
    """

    result = df.copy()

    text_columns = result.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:

        result[column] = (
            result[column]
            .astype("string")
            .str.strip()
            .str.replace(
                r"\s+",
                " ",
                regex=True
            )
        )

        result[column] = result[column].replace(
            "",
            pd.NA
        )

    return result


def clean_numeric_columns(
    df: pd.DataFrame,
    columns: list[str]
) -> pd.DataFrame:
    """
    Convert specified columns to numeric values.
    Invalid values become NaN.
    """

    result = df.copy()

    for column in columns:

        if column in result.columns:

            result[column] = pd.to_numeric(
                result[column],
                errors="coerce"
            )

    return result


def clean_date_columns(
    df: pd.DataFrame,
    columns: list[str]
) -> pd.DataFrame:
    """
    Convert specified columns into datetime.
    Invalid dates become NaT.
    """

    result = df.copy()

    for column in columns:

        if column in result.columns:

            result[column] = pd.to_datetime(
                result[column],
                errors="coerce"
            )

    return result


def print_quality_summary(
    df: pd.DataFrame,
    dataset_name: str
) -> None:
    """
    Print a basic data-quality summary.
    """

    print("\n" + "=" * 60)
    print(dataset_name)
    print("=" * 60)

    print(f"Rows              : {len(df):,}")
    print(f"Columns           : {len(df.columns):,}")
    print(f"Duplicate rows    : {df.duplicated().sum():,}")
    print(
        f"Missing values    : "
        f"{df.isna().sum().sum():,}"
    )

    missing = (
        df.isna()
        .sum()
        .sort_values(ascending=False)
    )

    missing = missing[missing > 0]

    if not missing.empty:

        print("\nColumns with missing values:")

        for column, count in missing.items():

            print(
                f"  {column}: {count:,}"
            )


# =========================================================
# 1. CLEAN SUPERSTORE SALES DATA
# =========================================================

def clean_superstore() -> pd.DataFrame:

    print("\nLoading Superstore dataset...")

    df = pd.read_csv(
        SUPERSTORE_RAW
    )

    original_rows = len(df)

    # -----------------------------------------------------
    # TEXT CLEANING
    # -----------------------------------------------------

    df = clean_text_columns(df)

    # -----------------------------------------------------
    # DATE CLEANING
    # -----------------------------------------------------

    df = clean_date_columns(
        df,
        [
            "Order.Date",
            "Ship.Date"
        ]
    )

    # -----------------------------------------------------
    # NUMERIC CLEANING
    # -----------------------------------------------------

    df = clean_numeric_columns(
        df,
        [
            "Discount",
            "记录数",
            "Profit",
            "Quantity",
            "Row.ID",
            "Sales",
            "Shipping.Cost",
            "Year",
            "weeknum"
        ]
    )

    # -----------------------------------------------------
    # VALIDATE REQUIRED COLUMNS
    # -----------------------------------------------------

    required_columns = [
        "Order.ID",
        "Product.ID",
        "Customer.ID",
        "Order.Date",
        "Sales",
        "Profit",
        "Quantity"
    ]

    missing_required = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_required:

        raise ValueError(
            "Missing required Superstore columns: "
            f"{missing_required}"
        )

    # -----------------------------------------------------
    # REMOVE EXACT DUPLICATES
    # -----------------------------------------------------

    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:

        df = df.drop_duplicates().reset_index(
            drop=True
        )

    # -----------------------------------------------------
    # VALIDATE CRITICAL FIELDS
    # -----------------------------------------------------

    critical_nulls = (
        df[required_columns]
        .isna()
        .sum()
    )

    critical_nulls = critical_nulls[
        critical_nulls > 0
    ]

    if not critical_nulls.empty:

        print(
            "\nWARNING: Critical Superstore fields "
            "contain missing values:"
        )

        print(critical_nulls)

    # -----------------------------------------------------
    # SAVE CLEANED DATA
    # -----------------------------------------------------

    df.to_csv(
        SUPERSTORE_OUTPUT,
        index=False
    )

    print(
        f"\nSuperstore rows: "
        f"{original_rows:,} → {len(df):,}"
    )

    print(
        f"Saved to: {SUPERSTORE_OUTPUT}"
    )

    print_quality_summary(
        df,
        "CLEANED SUPERSTORE DATA"
    )

    return df


# =========================================================
# 2. CLEAN INVENTORY DATA
# =========================================================

def clean_inventory() -> pd.DataFrame:

    print("\nLoading inventory dataset...")

    df = pd.read_csv(
        INVENTORY_RAW
    )

    original_rows = len(df)

    # -----------------------------------------------------
    # TEXT CLEANING
    # -----------------------------------------------------

    df = clean_text_columns(df)

    # -----------------------------------------------------
    # STANDARDIZE MISSING CATEGORY
    # -----------------------------------------------------
    # NOTE:
    # The source column is intentionally kept as
    # "Catagory" because the existing ETL expects it.

    if "Catagory" in df.columns:

        df["Catagory"] = (
            df["Catagory"]
            .fillna("Unknown")
        )

    # -----------------------------------------------------
    # UNIT PRICE CLEANING
    # -----------------------------------------------------

    if "Unit_Price" in df.columns:

        df["Unit_Price"] = (
            df["Unit_Price"]
            .astype("string")
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

        df["Unit_Price"] = pd.to_numeric(
            df["Unit_Price"],
            errors="coerce"
        )

    # -----------------------------------------------------
    # NUMERIC COLUMNS
    # -----------------------------------------------------

    df = clean_numeric_columns(
        df,
        [
            "Stock_Quantity",
            "Reorder_Level",
            "Reorder_Quantity",
            "Sales_Volume",
            "Inventory_Turnover_Rate"
        ]
    )

    # -----------------------------------------------------
    # DATE COLUMNS
    # -----------------------------------------------------

    df = clean_date_columns(
        df,
        [
            "Date_Received",
            "Last_Order_Date",
            "Expiration_Date"
        ]
    )

    # -----------------------------------------------------
    # REQUIRED COLUMN VALIDATION
    # -----------------------------------------------------

    required_columns = [
        "Product_ID",
        "Product_Name",
        "Catagory",
        "Stock_Quantity",
        "Reorder_Level",
        "Sales_Volume",
        "Inventory_Turnover_Rate"
    ]

    missing_required = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_required:

        raise ValueError(
            "Missing required Inventory columns: "
            f"{missing_required}"
        )

    # -----------------------------------------------------
    # REMOVE EXACT DUPLICATES
    # -----------------------------------------------------

    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:

        df = (
            df
            .drop_duplicates()
            .reset_index(drop=True)
        )

    # -----------------------------------------------------
    # CHECK NEGATIVE INVENTORY VALUES
    # -----------------------------------------------------

    numeric_inventory_columns = [
        "Stock_Quantity",
        "Reorder_Level",
        "Reorder_Quantity",
        "Sales_Volume",
        "Inventory_Turnover_Rate"
    ]

    for column in numeric_inventory_columns:

        if column in df.columns:

            negative_count = (
                df[column] < 0
            ).sum()

            if negative_count > 0:

                print(
                    f"WARNING: {column} contains "
                    f"{negative_count} negative values."
                )

    # -----------------------------------------------------
    # SAVE CLEANED DATA
    # -----------------------------------------------------

    df.to_csv(
        INVENTORY_OUTPUT,
        index=False
    )

    print(
        f"\nInventory rows: "
        f"{original_rows:,} → {len(df):,}"
    )

    print(
        f"Saved to: {INVENTORY_OUTPUT}"
    )

    print_quality_summary(
        df,
        "CLEANED INVENTORY DATA"
    )

    return df


# =========================================================
# 3. CLEAN RETURNS DATA
# =========================================================

def clean_returns() -> pd.DataFrame:

    print("\nLoading returns dataset...")

    df = pd.read_excel(
        RETURNS_RAW,
        sheet_name="Returns"
    )

    original_rows = len(df)

    # -----------------------------------------------------
    # TEXT CLEANING
    # -----------------------------------------------------

    df = clean_text_columns(df)

    # -----------------------------------------------------
    # VALIDATE REQUIRED COLUMNS
    # -----------------------------------------------------

    required_columns = [
        "Returned",
        "Order ID"
    ]

    missing_required = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_required:

        raise ValueError(
            "Missing required Returns columns: "
            f"{missing_required}"
        )

    # -----------------------------------------------------
    # REMOVE EXACT DUPLICATES
    # -----------------------------------------------------

    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:

        df = (
            df
            .drop_duplicates()
            .reset_index(drop=True)
        )

    # -----------------------------------------------------
    # REMOVE ROWS WITHOUT ORDER ID
    # -----------------------------------------------------

    df = (
        df
        .dropna(
            subset=["Order ID"]
        )
        .reset_index(drop=True)
    )

    # -----------------------------------------------------
    # SAVE CLEANED DATA
    # -----------------------------------------------------

    df.to_csv(
        RETURNS_OUTPUT,
        index=False
    )

    print(
        f"\nReturns rows: "
        f"{original_rows:,} → {len(df):,}"
    )

    print(
        f"Saved to: {RETURNS_OUTPUT}"
    )

    print_quality_summary(
        df,
        "CLEANED RETURNS DATA"
    )

    return df


# =========================================================
# MAIN PIPELINE
# =========================================================

def main():

    print("\n")
    print("=" * 70)
    print(
        "SMART RETAIL SUPPLY CHAIN "
        "& INVENTORY INTELLIGENCE"
    )
    print("DATA CLEANING PIPELINE")
    print("=" * 70)

    # -----------------------------------------------------
    # CLEAN DATASETS
    # -----------------------------------------------------

    clean_superstore()

    clean_inventory()

    clean_returns()

    # -----------------------------------------------------
    # COMPLETION MESSAGE
    # -----------------------------------------------------

    print("\n" + "=" * 70)
    print("DATA CLEANING COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print("\nProcessed files created:")

    print(
        f"  1. {SUPERSTORE_OUTPUT}"
    )

    print(
        f"  2. {INVENTORY_OUTPUT}"
    )

    print(
        f"  3. {RETURNS_OUTPUT}"
    )


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()