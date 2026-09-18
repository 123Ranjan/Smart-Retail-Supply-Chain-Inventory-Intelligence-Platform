import pandas as pd
from sqlalchemy import text


SCHEMA = "retail_dw"


def truncate_tables(engine):

    tables = [
        "fact_sales",
        "fact_inventory",
        "fact_returns",
        "dim_product",
        "dim_customer",
        "dim_category",
        "dim_geography",
        "dim_ship_mode",
        "dim_supplier",
        "dim_warehouse",
        "dim_date"
    ]

    table_list = ", ".join(
        f"{SCHEMA}.{table}"
        for table in tables
    )

    sql = f"""
        TRUNCATE TABLE
        {table_list}
        RESTART IDENTITY CASCADE;
    """

    with engine.begin() as connection:
        connection.execute(text(sql))

    print("Existing warehouse data cleared.")


def load_dataframe(
    engine,
    dataframe,
    table_name
):

    dataframe.to_sql(
        table_name,
        engine,
        schema=SCHEMA,
        if_exists="append",
        index=False,
        chunksize=1000
    )

    print(
        f"{table_name} loaded: "
        f"{len(dataframe)} rows"
    )


def read_table(
    engine,
    table_name
):

    query = (
        f"SELECT * "
        f"FROM {SCHEMA}.{table_name}"
    )

    return pd.read_sql(
        query,
        engine
    )