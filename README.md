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
- [Power BI Dashboard](#-power-bi-dashboard)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Running the Project](#-running-the-project)
- [Key Business Insights](#-key-business-insights)
- [Dashboard Screenshots](#-dashboard-screenshots)
- [Future Improvements](#-future-improvements)

---

# 🎯 Overview

The **Smart Retail Supply Chain & Inventory Intelligence Platform** is an end-to-end analytics project designed to analyze retail sales, profitability, inventory health, product performance, returns, and supply-chain risk.

The project combines:

- Python-based data preparation and analysis
- PostgreSQL data warehousing
- SQL business analytics
- Power BI interactive dashboards
- DAX-based KPI and analytical modeling

The platform transforms raw retail datasets into structured analytical data and provides decision-support insights for sales performance, profitability, inventory planning, and root-cause analysis.

---

# ✨ Key Features

## 📊 Sales & Profitability Analytics

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

## 📦 Inventory Intelligence

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

## 🔎 Root Cause Analysis

The platform performs inventory-focused Root Cause Analysis to identify the drivers behind stock pressure.

Key analytical areas include:

- Inventory Risk Drivers by Category
- Stock Gap Contribution by Category
- Category × Inventory Risk Heatmap
- Demand vs Inventory Turnover
- Decomposition Tree analysis
- High-risk product identification

---

## 🛍️ Product & Decision Intelligence

- Top profitable products
- Top products by sales
- Product sales vs profitability
- Discount vs profit margin analysis
- Product performance ranking
- Top and bottom product profitability
- Product portfolio analysis
- Product-level drill-through analysis

---

# 📈 Project Highlights

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

# 🛠️ Tech Stack

## Data Processing & Analysis

| Technology | Purpose |
|---|---|
| **Python** | Data processing, ETL, analysis and automation |
| **Pandas** | Data cleaning, transformation, merging and aggregation |
| **NumPy** | Numerical calculations and statistical thresholds |
| **Matplotlib** | Exploratory Data Analysis and visualization |

## Database & Analytics

| Technology | Purpose |
|---|---|
| **PostgreSQL** | Data warehouse |
| **SQL** | Business analysis and analytical views |
| **SQLAlchemy** | Database connectivity and loading |

## Business Intelligence

| Technology | Purpose |
|---|---|
| **Power BI** | Interactive dashboards |
| **DAX** | Measures, KPIs, rankings and time intelligence |

---

# 🔄 Data Pipeline

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
