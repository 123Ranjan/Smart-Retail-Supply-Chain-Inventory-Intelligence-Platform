def transform_fact_returns(returns_df):

    returns = returns_df.copy()

    # Standardize column names
    returns.columns = (
        returns.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(".", "_", regex=False)
    )

    # Handle common variants
    rename_map = {}

    if "order_id" not in returns.columns:
        raise ValueError(
            "Returns dataset does not contain an Order ID column."
        )

    if "returned" not in returns.columns:
        raise ValueError(
            "Returns dataset does not contain a Returned column."
        )

    fact_returns = returns[
        [
            "order_id",
            "returned"
        ]
    ].copy()

    fact_returns = (
        fact_returns
        .dropna(subset=["order_id"])
        .drop_duplicates()
        .reset_index(drop=True)
    )

    return fact_returns