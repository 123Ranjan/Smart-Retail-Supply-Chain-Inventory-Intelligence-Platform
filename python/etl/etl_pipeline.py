from .config.database import get_engine

from .extract.superstore import extract_superstore
from .extract.inventory import extract_inventory
from .extract.returns import extract_returns

from .transform.dimensions import (
    transform_category,
    transform_customer,
    transform_product,
    transform_geography,
    transform_ship_mode,
    transform_supplier,
    transform_warehouse,
    create_date_dimension
)

from .transform.fact_sales import transform_fact_sales
from .transform.fact_inventory import transform_fact_inventory
from .transform.fact_returns import transform_fact_returns

from .load.loader import (
    truncate_tables,
    load_dataframe,
    read_table
)

from .utils.logger import get_logger

logger = get_logger()


def main():

    logger.info(
        "ETL pipeline started."
    )

    engine = get_engine()

    try:

        # =====================================
        # EXTRACT
        # =====================================

        logger.info("Extracting datasets...")

        superstore = extract_superstore()
        inventory = extract_inventory()
        returns = extract_returns()

        # =====================================
        # CLEAR OLD DATA
        # =====================================

        truncate_tables(engine)

        # =====================================
        # DIM CATEGORY
        # =====================================
        # =====================================
# DIM CATEGORY
# =====================================

        category = transform_category(
            superstore,
            inventory
        )

        load_dataframe(
            engine,
            category,
            "dim_category"
        )

        category_dimension = read_table(
            engine,
            "dim_category"
        )
        # =====================================
        # DIM CUSTOMER
        # =====================================

        customer = transform_customer(
            superstore
        )

        load_dataframe(
            engine,
            customer,
            "dim_customer"
        )

        # =====================================
        # DIM PRODUCT
        # =====================================

        product = transform_product(
            superstore,
            inventory,
            category_dimension
        )

        load_dataframe(
            engine,
            product,
            "dim_product"
        )

        # =====================================
        # DIM GEOGRAPHY
        # =====================================

        geography = transform_geography(
            superstore
        )

        load_dataframe(
            engine,
            geography,
            "dim_geography"
        )

        # =====================================
        # DIM SHIP MODE
        # =====================================

        ship_mode = transform_ship_mode(
            superstore
        )

        load_dataframe(
            engine,
            ship_mode,
            "dim_ship_mode"
        )

        # =====================================
        # DIM SUPPLIER
        # =====================================

        supplier = transform_supplier(
            inventory
        )

        load_dataframe(
            engine,
            supplier,
            "dim_supplier"
        )

        # =====================================
        # DIM WAREHOUSE
        # =====================================

        warehouse = transform_warehouse(
            inventory
        )

        load_dataframe(
            engine,
            warehouse,
            "dim_warehouse"
        )

        # =====================================
        # DIM DATE
        # =====================================

        date_dimension = (
            create_date_dimension()
        )

        load_dataframe(
            engine,
            date_dimension,
            "dim_date"
        )

        # =====================================
        # READ DIMENSIONS WITH SURROGATE KEYS
        # =====================================

        product_dimension = read_table(
            engine,
            "dim_product"
        )

        customer_dimension = read_table(
            engine,
            "dim_customer"
        )

        geography_dimension = read_table(
            engine,
            "dim_geography"
        )

        ship_mode_dimension = read_table(
            engine,
            "dim_ship_mode"
        )

        supplier_dimension = read_table(
            engine,
            "dim_supplier"
        )

        warehouse_dimension = read_table(
            engine,
            "dim_warehouse"
        )

        # =====================================
        # FACT SALES
        # =====================================

        fact_sales = transform_fact_sales(
            superstore,
            product_dimension,
            customer_dimension,
            geography_dimension,
            ship_mode_dimension
        )

        load_dataframe(
            engine,
            fact_sales,
            "fact_sales"
        )

        # =====================================
        # FACT INVENTORY
        # =====================================

        fact_inventory = (
            transform_fact_inventory(
                inventory,
                product_dimension,
                supplier_dimension,
                warehouse_dimension
            )
        )

        # Don't blindly load invalid
        # product relationships.
        missing_products = (
            fact_inventory[
                "product_key"
            ]
            .isna()
            .sum()
        )

        logger.info(
            "Inventory rows with missing "
            f"product_key: {missing_products}"
        )

        if missing_products == 0:

            load_dataframe(
                engine,
                fact_inventory,
                "fact_inventory"
            )

        else:

            logger.warning(
                "fact_inventory was NOT loaded "
                "because inventory Product_ID "
                "values do not fully map to "
                "dim_product."
            )

        # =====================================
        # FACT RETURNS
        # =====================================

        fact_returns = (
            transform_fact_returns(
                returns
            )
        )

        load_dataframe(
            engine,
            fact_returns,
            "fact_returns"
        )

        logger.info(
            "ETL pipeline completed successfully."
        )

    except Exception:

        logger.exception(
            "ETL pipeline failed."
        )

        raise


if __name__ == "__main__":
    main()