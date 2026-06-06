import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import datetime as dt
import warnings
warnings.filterwarnings('ignore')

print("=" * 50)
print("STEP 1: LOADING DATA")
print("=" * 50)

df = pd.read_excel("data/online_retail.xlsx")

print(f"Initial Shape       : {df.shape}")
print(f"\nColumn Names        :\n{df.columns.tolist()}")
print(f"\nFirst 5 Rows:\n{df.head()}")

print("\n" + "=" * 50)
print("STEP 2: DATA CLEANING & PREPROCESSING")
print("=" * 50)

print("\n[Missing Values BEFORE Cleaning]")
print(df.isnull().sum())

df = df.dropna(subset=['CustomerID'])         
df['Description'] = df['Description'].fillna("Unknown")   

before = len(df)
df = df.drop_duplicates()
after = len(df)
print(f"\nDuplicates Removed  : {before - after}")

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
df = df.dropna(subset=['InvoiceDate'])        

df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]

df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

print("\n[Missing Values AFTER Cleaning]")
print(df.isnull().sum())
print(f"\nFinal Cleaned Shape : {df.shape}")
print("\n" + "=" * 50)
print("STEP 3: ANALYSIS & VISUALIZATION")
print("=" * 50)
print("\n[A] Top 10 Customers by Revenue")

top_revenue = (df.groupby('CustomerID')['TotalAmount']
               .sum()
               .sort_values(ascending=False)
               .head(10))

print(top_revenue)

plt.figure(figsize=(10, 5))
top_revenue.plot(kind='bar', color='steelblue', edgecolor='black')
plt.title("Top 10 Customers by Revenue", fontsize=14)
plt.ylabel("Total Revenue")
plt.xlabel("Customer ID")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_customers_revenue.png", dpi=150)
plt.show()

print("\n[B] Top 10 Customers by Frequency")

top_frequency = (df.groupby('CustomerID')['InvoiceNo']
                 .nunique()
                 .sort_values(ascending=False)
                 .head(10))

print(top_frequency)

plt.figure(figsize=(10, 5))
top_frequency.plot(kind='bar', color='coral', edgecolor='black')
plt.title("Top 10 Customers by Purchase Frequency", fontsize=14)
plt.ylabel("Number of Orders")
plt.xlabel("Customer ID")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_customers_frequency.png", dpi=150)
plt.show()

print("\n[C] Monthly Revenue Trend")

df['Month'] = df['InvoiceDate'].dt.to_period('M')
monthly_sales = df.groupby('Month')['TotalAmount'].sum()

print(monthly_sales)

plt.figure(figsize=(12, 5))
monthly_sales.plot(kind='line', marker='o', color='green', linewidth=2)
plt.title("Monthly Revenue Trend", fontsize=14)
plt.ylabel("Total Revenue")
plt.xlabel("Month")
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("monthly_trend.png", dpi=150)
plt.show()

print("\n[D] Weekly Revenue Trend")

weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['Weekday'] = df['InvoiceDate'].dt.day_name()
weekly_sales = df.groupby('Weekday')['TotalAmount'].sum().reindex(weekday_order)

print(weekly_sales)

plt.figure(figsize=(10, 5))
weekly_sales.plot(kind='bar', color='mediumpurple', edgecolor='black')
plt.title("Weekly Revenue Trend", fontsize=14)
plt.ylabel("Total Revenue")
plt.xlabel("Day of Week")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("weekly_trend.png", dpi=150)
plt.show()

print("\n[E] Top 10 Products by Quantity Sold")

top_products = (df.groupby('Description')['Quantity']
                .sum()
                .sort_values(ascending=False)
                .head(10))

print(top_products)

plt.figure(figsize=(12, 5))
top_products.plot(kind='bar', color='darkorange', edgecolor='black')
plt.title("Top 10 Products by Quantity Sold", fontsize=14)
plt.ylabel("Quantity Sold")
plt.xlabel("Product")
plt.xticks(rotation=75)
plt.tight_layout()
plt.savefig("product_popularity.png", dpi=150)
plt.show()

print("\n[F] Sales Heatmap (Weekday vs Hour)")

df['Hour'] = df['InvoiceDate'].dt.hour

heatmap_data = df.pivot_table(
    values='TotalAmount',
    index='Weekday',
    columns='Hour',
    aggfunc='sum'
).reindex(weekday_order)

plt.figure(figsize=(14, 6))
sns.heatmap(heatmap_data, cmap='YlOrRd', linewidths=0.5)
plt.title("Sales Heatmap: Weekday vs Hour", fontsize=14)
plt.tight_layout()
plt.savefig("sales_heatmap.png", dpi=150)
plt.show()


print("\n" + "=" * 50)
print("STEP 4: CUSTOMER SEGMENTATION (RFM + K-MEANS)")
print("=" * 50)

snapshot_date = df['InvoiceDate'].max() + dt.timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate' : lambda x: (snapshot_date - x.max()).days,   
    'InvoiceNo'   : 'nunique',                                  
    'TotalAmount' : 'sum'                                        
})
rfm.columns = ['Recency', 'Frequency', 'Monetary']

scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)

inertia = []
k_range = range(2, 8)

for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(rfm_scaled)
    inertia.append(km.inertia_)

plt.figure(figsize=(8, 4))
plt.plot(list(k_range), inertia, marker='o', color='teal', linewidth=2)
plt.title("Elbow Method — Optimal Number of Clusters", fontsize=13)
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("elbow_method.png", dpi=150)
plt.show()

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

cluster_summary = rfm.groupby('Cluster').mean().round(2)
print("\nCluster Summary (Mean RFM values per segment):")
print(cluster_summary)

plt.figure(figsize=(9, 5))
sns.scatterplot(
    data=rfm,
    x='Frequency',
    y='Monetary',
    hue='Cluster',
    palette='tab10',
    alpha=0.7
)
plt.title("Customer Segments: Frequency vs Monetary", fontsize=13)
plt.tight_layout()
plt.savefig("customer_segments.png", dpi=150)
plt.show()

print("\n" + "=" * 50)
print("STEP 5: SUMMARY REPORT")
print("=" * 50)

total_revenue      = df['TotalAmount'].sum()
total_customers    = df['CustomerID'].nunique()
total_orders       = df['InvoiceNo'].nunique()
top_cust_revenue   = top_revenue.sum()
top_cust_pct       = (top_cust_revenue / total_revenue) * 100
best_month         = monthly_sales.idxmax()
best_day           = weekly_sales.idxmax()
top_product        = top_products.index[0]

print(f"""
Customer Behavior Analysis — Key Insights
------------------------------------------
Total Revenue         : £{total_revenue:,.2f}
Total Customers       : {total_customers:,}
Total Orders          : {total_orders:,}
Top 10 Customer Share : {top_cust_pct:.1f}% of total revenue
Best Month            : {best_month}
Most Active Day       : {best_day}
Top Selling Product   : {top_product}

Business Recommendations:
  1. Launch a loyalty program for high-value customers.
  2. Run re-engagement campaigns for at-risk/inactive customers.
  3. Increase inventory before peak months ({best_month}).
  4. Promote slow-moving products through bundles.
  5. Schedule flash sales on peak day ({best_day}).
------------------------------------------
All charts saved as PNG files in the project folder.
""")