-- =========================================================
-- SALES KPI
-- =========================================================

CREATE OR REPLACE VIEW retail_dw.vw_sales_kpi AS
SELECT
    COUNT(*) AS total_transactions,
    SUM(quantity) AS total_quantity,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit,
    AVG(discount) AS avg_discount,
    AVG(shipping_cost) AS avg_shipping_cost
FROM retail_dw.fact_sales;


-- =========================================================
-- SALES BY CATEGORY
-- =========================================================

CREATE OR REPLACE VIEW retail_dw.vw_sales_by_category AS
SELECT
    c.category_name,
    c.sub_category_name,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    SUM(f.quantity) AS total_quantity
FROM retail_dw.fact_sales f
JOIN retail_dw.dim_product p
    ON f.product_key = p.product_key
JOIN retail_dw.dim_category c
    ON p.category_key = c.category_key
GROUP BY
    c.category_name,
    c.sub_category_name;


-- =========================================================
-- SALES BY YEAR
-- =========================================================

CREATE OR REPLACE VIEW retail_dw.vw_sales_by_year AS
SELECT
    d.year,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    SUM(f.quantity) AS total_quantity
FROM retail_dw.fact_sales f
JOIN retail_dw.dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year
ORDER BY d.year;


-- =========================================================
-- SALES BY REGION
-- =========================================================

CREATE OR REPLACE VIEW retail_dw.vw_sales_by_region AS
SELECT
    g.region,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    SUM(f.quantity) AS total_quantity
FROM retail_dw.fact_sales f
JOIN retail_dw.dim_geography g
    ON f.geography_key = g.geography_key
GROUP BY g.region
ORDER BY total_sales DESC;


-- =========================================================
-- TOP PRODUCTS
-- =========================================================

CREATE OR REPLACE VIEW retail_dw.vw_top_products AS
SELECT
    p.product_id,
    p.product_name,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit,
    SUM(f.quantity) AS total_quantity
FROM retail_dw.fact_sales f
JOIN retail_dw.dim_product p
    ON f.product_key = p.product_key
GROUP BY
    p.product_id,
    p.product_name
ORDER BY total_sales DESC;


-- =========================================================
-- INVENTORY OVERVIEW
-- =========================================================

CREATE OR REPLACE VIEW retail_dw.vw_inventory_overview AS
SELECT
    COUNT(*) AS total_inventory_records,
    SUM(stock_quantity) AS total_stock,
    SUM(reorder_quantity) AS total_reorder_quantity,
    SUM(sales_volume) AS total_sales_volume,
    AVG(inventory_turnover_rate) AS avg_inventory_turnover
FROM retail_dw.fact_inventory;


-- =========================================================
-- LOW STOCK PRODUCTS
-- =========================================================

CREATE OR REPLACE VIEW retail_dw.vw_low_stock_products AS
SELECT
    p.product_id,
    p.product_name,
    i.stock_quantity,
    i.reorder_level,
    i.reorder_quantity,
    s.supplier_name,
    w.warehouse_location
FROM retail_dw.fact_inventory i
JOIN retail_dw.dim_product p
    ON i.product_key = p.product_key
JOIN retail_dw.dim_supplier s
    ON i.supplier_key = s.supplier_key
JOIN retail_dw.dim_warehouse w
    ON i.warehouse_key = w.warehouse_key
WHERE i.stock_quantity <= i.reorder_level
ORDER BY i.stock_quantity;


-- =========================================================
-- SUPPLIER PERFORMANCE
-- =========================================================

CREATE OR REPLACE VIEW retail_dw.vw_supplier_performance AS
SELECT
    s.supplier_id,
    s.supplier_name,
    COUNT(*) AS inventory_records,
    SUM(i.stock_quantity) AS total_stock,
    SUM(i.sales_volume) AS total_sales_volume,
    AVG(i.inventory_turnover_rate) AS avg_turnover_rate
FROM retail_dw.fact_inventory i
JOIN retail_dw.dim_supplier s
    ON i.supplier_key = s.supplier_key
GROUP BY
    s.supplier_id,
    s.supplier_name
ORDER BY total_sales_volume DESC;


-- =========================================================
-- WAREHOUSE PERFORMANCE
-- =========================================================

CREATE OR REPLACE VIEW retail_dw.vw_warehouse_performance AS
SELECT
    w.warehouse_location,
    COUNT(*) AS inventory_records,
    SUM(i.stock_quantity) AS total_stock,
    SUM(i.sales_volume) AS total_sales_volume,
    AVG(i.inventory_turnover_rate) AS avg_turnover_rate
FROM retail_dw.fact_inventory i
JOIN retail_dw.dim_warehouse w
    ON i.warehouse_key = w.warehouse_key
GROUP BY
    w.warehouse_location
ORDER BY total_sales_volume DESC;


-- =========================================================
-- RETURN SUMMARY
-- =========================================================

CREATE OR REPLACE VIEW retail_dw.vw_return_summary AS
SELECT
    returned,
    COUNT(*) AS return_count
FROM retail_dw.fact_returns
GROUP BY returned
ORDER BY return_count DESC;