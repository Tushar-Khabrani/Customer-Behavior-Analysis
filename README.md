# 🛒 Customer Behavior Analysis

End-to-end customer behavior analysis on a retail transactions dataset using **Python** and **MySQL** — uncovering purchasing patterns, revenue trends, and customer segmentation insights.

---

## 📁 Project Structure

    customer-behavior-analysis/
    ├── python-analysis/
    │   ├── analysis.py
    │   ├── data/
    │   │   └── online_retail.xlsx
    │   └── graphs/  (8 visualizations)
    ├── sql-analysis/
    │   ├── sql/
    │   │   └── customer_data.sql
    │   ├── csv_exports/  (5 CSV files)
    │   ├── graphs/  (8 visualizations)
    │   ├── analysis.py
    │   └── export_csv.py
    ├── report/
    │   └── customer_behavior_analysis.pdf
    └── README.md
---

## 📊 Analysis Performed

### 🐍 Python Analysis
- Cleaned and preprocessed raw data using **Pandas** — handled null values, removed duplicates, standardized formats
- Analyzed revenue trends across **9 months (Jan–Sep 2024)** — Total Revenue: ₹5.42L | Avg Order Value: ₹27.1K | Peak Month: July 2024 (₹1.4L)
- Identified **Electronics** as dominant category — 89% of total revenue; top products: iPhone 14, Laptop HP
- City-wise revenue: **Bangalore ₹2.21L** | Ahmedabad ₹1.46L | Mumbai ₹75K (across 9 Indian cities)
- **K-Means Clustering** (Scikit-learn) — segmented 15 customers into 3 groups:
  - 🔴 High-Value: 4 customers, ₹1.10L avg — contributed 65%+ of total revenue
  - 🟡 Medium-Value: 6 customers, ₹14K avg
  - 🟢 Low-Value: 5 customers, ₹3K avg
- Built **8 visualizations** — monthly trend lines, category pie charts, city bar charts, category × city heatmap

### 🗄️ SQL Analysis
- Designed a **normalized MySQL relational database** with 4 tables: Customers, Products, Orders, Order Items (20+ records)
- Advanced SQL — JOINs across 4 tables, Window Functions (RANK, LAG, SUM OVER), Views, Stored Procedures, Triggers, CTEs, Subqueries
- Exported query results to CSV for further analysis

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Data cleaning, analysis, visualization |
| Pandas | Data preprocessing |
| Matplotlib & Seaborn | 8 charts and graphs |
| Scikit-learn | K-Means customer segmentation |
| MySQL | Relational database + advanced queries |

**Domain:** Retail Analytics · Customer Segmentation · Business Intelligence

---

## 🤖 AI Integration
Leveraged AI coding assistants to accelerate scripting and code optimization — all data analysis, business logic, and insight interpretation independently developed and validated.

---

## 📄 Report
Full analysis report available in [`/report/customer_behavior_analysis.pdf`](./report/customer_behavior_analysis.pdf)
