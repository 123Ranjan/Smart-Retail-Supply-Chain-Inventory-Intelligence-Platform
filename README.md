# 📊 Smart Retail Supply Chain & Inventory Intelligence Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24+-013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-11557C.svg?style=for-the-badge&logo=matplotlib&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Analytics-orange.svg?style=for-the-badge)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811.svg?style=for-the-badge&logo=powerbi&logoColor=black)
![DAX](https://img.shields.io/badge/DAX-35%2B%20Measures-purple.svg?style=for-the-badge)

</div>

> An end-to-end **retail analytics, supply chain, and inventory intelligence platform** built using Python, PostgreSQL, SQL, Power BI, and DAX to transform raw retail data into actionable business insights.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Project Highlights](#-project-highlights)
- [Tech Stack](#-tech-stack)
- [Data Pipeline](#-data-pipeline)
- [Data Warehouse](#-data-warehouse)
- [Power BI Dashboard](#-power-bi-dashboard)
- [DAX Analytics](#-dax-analytics)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Project](#-running-the-project)
- [Key Business Insights](#-key-business-insights)
- [Dashboard Screenshots](#-dashboard-screenshots)
- [Power BI Report](#-power-bi-report)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

## 🎯 Overview

The **Smart Retail Supply Chain & Inventory Intelligence Platform** is an end-to-end analytics project designed to analyze retail sales, profitability, inventory health, product performance, returns, and supply-chain risk.

The project combines:

- Python-based data preparation and analysis
- PostgreSQL data warehousing
- SQL business analytics
- Power BI interactive dashboards
- DAX-based KPI and analytical modeling

The platform transforms raw retail datasets into structured analytical data and provides decision-support insights for sales performance, profitability, inventory planning, and root-cause analysis.

---

## ✨ Key Features

### 📊 Sales & Profitability Analytics

- Total Sales and Total Profit analysis
- Profit Margin analysis
- Sales and profit trends
- Category profitability
- Regional performance analysis
- Product-level sales and profitability
- Average Order Value
- Profit per Order
- Discount impact analysis
- Shipping cost analysis
- Year-over-Year growth analysis

---

### 📦 Inventory Intelligence

- Total inventory stock monitoring
- Reorder risk analysis
- Stock-gap analysis
- Inventory turnover analysis
- Demand vs inventory pressure
- Category-level inventory health
- Critical product identification
- Low-stock product analysis
- Inventory risk classification

Inventory risk is classified into:

- Normal
- Low Stock
- Fast Turnover + Low Stock
- High Demand + Low Stock

---

### 🔎 Root Cause Analysis

The platform performs inventory-focused Root Cause Analysis to identify the drivers behind stock pressure.

Key analytical areas include:

- Inventory Risk Drivers by Category
- Stock Gap Contribution by Category
- Category × Inventory Risk Heatmap
- Demand vs Inventory Turnover
- Decomposition Tree analysis
- High-risk product identification

---

### 🛍️ Product & Decision Intelligence

- Top profitable products
- Top products by sales
- Product sales vs profitability
- Discount vs profit margin analysis
- Product performance ranking
- Top and bottom product profitability
- Product portfolio analysis
- Product-level drill-through analysis

---

## 📈 Project Highlights

| Metric | Value |
|---|---:|
| Sales Transactions | **51,290** |
| Inventory Records | **990** |
| Return Records | **296** |
| Customers | **4,873** |
| Products | **11,282** |
| Categories | **25** |
| DAX Measures & KPIs | **35+** |
| Power BI Dashboard Pages | **6** |

---

## 🛠️ Tech Stack

### Data Processing & Analysis

| Technology | Purpose |
|---|---|
| **Python** | Data processing, ETL, analysis and automation |
| **Pandas** | Data cleaning, transformation, merging and aggregation |
| **NumPy** | Numerical calculations and statistical thresholds |
| **Matplotlib** | Exploratory Data Analysis and visualization |

### Database & Analytics

| Technology | Purpose |
|---|---|
| **PostgreSQL** | Data warehouse |
| **SQL** | Business analysis and analytical views |
| **SQLAlchemy** | Database connectivity and loading |

### Business Intelligence

| Technology | Purpose |
|---|---|
| **Power BI** | Interactive dashboards |
| **DAX** | Measures, KPIs, rankings and time intelligence |

---

## 🔄 Data Pipeline

```text
                    RAW DATA
                       │
                       ▼
              ┌─────────────────┐
              │ Python Cleaning │
              │   Pandas        │
              └─────────────────┘
                       │
                       ▼
              PROCESSED DATA
                       │
                       ▼
              ┌─────────────────┐
              │ Python ETL      │
              │ Extract         │
              │ Transform       │
              │ Load            │
              └─────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   PostgreSQL    │
              │   Data Warehouse│
              └─────────────────┘
                       │
                       ▼
                 SQL Analytics
                       │
                       ▼
              ┌─────────────────┐
              │    Power BI     │
              │  + DAX Model    │
              └─────────────────┘
                       │
                       ▼
              BUSINESS INSIGHTS
```

---

## 🏗️ Data Warehouse

The PostgreSQL warehouse follows a dimensional modeling approach with fact and dimension tables.

### Fact Tables

```text
fact_sales
fact_inventory
fact_returns
```

### Dimension Tables

```text
dim_date
dim_product
dim_category
dim_customer
dim_geography
dim_ship_mode
dim_supplier
dim_warehouse
dim_order
```

This structure supports flexible analytical reporting and Power BI modeling.

---

## 📊 Power BI Dashboard

The final Power BI solution contains six analytical views.

| Page | Purpose |
|---|---|
| **Executive Command Center** | Executive KPIs and overall business health |
| **Sales & Profitability Intelligence** | Sales, profit, discount and regional performance |
| **Inventory Intelligence** | Inventory health, reorder risk and stock pressure |
| **Root Cause Analysis** | Inventory risk drivers and stock-gap analysis |
| **Product & Decision Intelligence** | Product profitability and ranking analysis |
| **Product Detail & Decision View** | Product-level drill-through analysis |

### Dashboard Capabilities

- Interactive slicers
- Drill-through analysis
- Dynamic KPIs
- DAX measures
- Product rankings
- Decomposition Tree
- Scatter plots
- Heatmaps
- Matrix analysis
- Risk analysis
- Time intelligence
- Cross-filtering

---

## 🧮 DAX Analytics

The Power BI model contains **35+ DAX measures and KPIs** covering:

```text
Sales
Profit
Profit Margin
Orders
Average Order Value
Sales Growth
YoY Analysis
Inventory Turnover
Reorder Risk
Stock Gap
Inventory Risk
Product Ranking
Category Analysis
Shipping Cost
Discount Analysis
Return Rate
```

---

## 📁 Project Structure

```text
Smart-Retail-Supply-Chain-Inventory-Intelligence-Platform/
│
├── 📁 config/
│   └── database.example.ini
│
├── 📁 data/
│   ├── 📁 raw/
│   │   ├── superstore.csv
│   │   ├── Grocery_Inventory_and_Sales_Dataset.csv
│   │   └── Superstore Dataset.xlsx
│   │
│   └── 📁 processed/
│       ├── superstore_cleaned.csv
│       ├── inventory_cleaned.csv
│       └── returns_cleaned.csv
│
├── 📁 documentation/
│   ├── data_dictionary.xlsx
│   ├── project_architecture.md
│   ├── project_plan.md
│   └── source_to_target_mapping.xlsx
│
├── 📁 Dashboard_Images/
│
├── 📁 python/
│   │
│   ├── 📁 analysis/
│   │   ├── eda.py
│   │   ├── inventory_eda.py
│   │   ├── rca_analysis.py
│   │   └── business_insights.py
│   │
│   ├── 📁 cleaning/
│   │   └── data_cleaning.py
│   │
│   ├── 📁 etl/
│   │   ├── extract/
│   │   ├── transform/
│   │   ├── load/
│   │   ├── config/
│   │   └── utils/
│   │
│   ├── 📁 profiling/
│   │   └── data_profiling.py
│   │
│   └── 📁 utils/
│       ├── config.py
│       └── helper_functions.py
│
├── 📁 sql/
│   └── 📁 analytics/
│       └── kpi_views.sql
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Installation

### Prerequisites

Make sure you have installed:

| Software | Version |
|---|---|
| **Python** | 3.11+ |
| **PostgreSQL** | 15+ |
| **Git** | Latest |
| **Power BI Desktop** | Latest |

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/123Ranjan/Smart-Retail-Supply-Chain-Inventory-Intelligence-Platform.git
cd Smart-Retail-Supply-Chain-Inventory-Intelligence-Platform
```

---

### Step 2: Create a Virtual Environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Create your local database configuration using the provided example:

```text
config/database.example.ini
```

Create:

```text
config/database.ini
```

and configure your PostgreSQL connection locally.

**Do not commit `database.ini` or database passwords to GitHub.**

---

## ▶️ Running the Project

### 1. Run Data Cleaning

```bash
python -m python.cleaning.data_cleaning
```

This generates cleaned datasets inside:

```text
data/processed/
```

---

### 2. Run Data Profiling

```bash
python -m python.profiling.data_profiling
```

---

### 3. Run Exploratory Data Analysis

```bash
python -m python.analysis.eda
```

---

### 4. Run Inventory Analysis

```bash
python -m python.analysis.inventory_eda
```

---

### 5. Run Root Cause Analysis

```bash
python -m python.analysis.rca_analysis
```

---

### 6. Generate Business Insights

```bash
python -m python.analysis.business_insights
```

---

### 7. Run ETL Pipeline

```bash
python -m python.etl.etl_pipeline
```

The pipeline loads the transformed data into the PostgreSQL data warehouse.

---

## 💡 Key Business Insights

The analysis identified several important inventory and profitability indicators:

- **45.96%** of products require replenishment.
- **455 products** are below their reorder level.
- Total stock gap is approximately **13,946 units**.
- **112 products** fall into the High Demand + Low Stock category.
- **170 products** fall into the Fast Turnover + Low Stock category.
- **28%+ of products** fall into the combined high-demand/fast-turnover low-stock pressure groups.
- Technology and Office Supplies show stronger profitability compared with Furniture in the analyzed dataset.

These findings are used in the Power BI dashboard to support inventory prioritization and business analysis.

---

## 🖼️ Dashboard Screenshots

Dashboard images can be found in:

```text
Dashboard_Images/
```

Recommended organization:

```text
Dashboard_Images/
│
├── Executive_Command_Center/
├── Sales_Profitability/
├── Inventory_Intelligence/
├── Root_Cause_Analysis/
├── Product_Decision_Intelligence/
└── Product_Detail/
```

Example:

```markdown
## Executive Command Center

![Executive Dashboard](Dashboard_Images/Executive_Command_Center/executive_command_center.png)
```

---

## 📄 Power BI Report

The repository also contains the exported Power BI dashboard report:

```text
Smart_Retail_Supply_Chain_Inventory_Intelligence_Powerbi_Dashboard.pdf
```

---

## 🔮 Future Improvements

- Automated scheduled ETL
- Data quality monitoring
- Cloud deployment
- Advanced demand forecasting
- Automated inventory replenishment recommendations
- What-If analysis for inventory planning
- Machine learning-based demand prediction
- Automated dashboard refresh pipelines

---

## 👨‍💻 Author

**Malaya Ranjan Mohanty**

Data Analyst | Python | SQL | PostgreSQL | Power BI

[GitHub](https://github.com/123Ranjan)

---

<div align="center">

### ⭐ If you find this project useful, consider giving the repository a star!

**Built with Python • PostgreSQL • SQL • Power BI • DAX**

</div>
