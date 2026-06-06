import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid", palette="muted")
fmt = mticker.FuncFormatter(lambda x, _: f"Rs.{x:,.0f}")

customers   = pd.read_csv("csv_exports/customers.csv")
products    = pd.read_csv("csv_exports/products.csv")
orders      = pd.read_csv("csv_exports/orders.csv")
order_items = pd.read_csv("csv_exports/order_items.csv")
df          = pd.read_csv("csv_exports/customer_data.csv")   

print("=" * 55)
print("  ALL TABLES LOADED")
print("=" * 55)
print(f"\n Customers   : {len(customers)} rows")
print(customers.to_string(index=False))
print(f"\n Products    : {len(products)} rows")
print(products.to_string(index=False))
print(f"\n Orders      : {len(orders)} rows")
print(orders.to_string(index=False))
print(f"\n Order Items : {len(order_items)} rows")
print(order_items.to_string(index=False))
print(f"\n Analytical Dataset (Joined) : {len(df)} rows")
print(df.to_string(index=False))

df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df["order_date"] = pd.to_datetime(df["order_date"])
df["revenue"]    = pd.to_numeric(df["revenue"],  errors="coerce")
df["quantity"]   = pd.to_numeric(df["quantity"], errors="coerce")
df["month_str"]  = df["order_date"].dt.to_period("M").astype(str)

print("\n Null values after cleaning:")
print(df.isnull().sum())
print(f"\n Total records after cleaning: {len(df)}")

monthly_sales  = df.groupby("month_str")["revenue"].sum().sort_index()
top_customers  = df.groupby("name")["revenue"].sum().sort_values(ascending=False)
top_products   = df.groupby("product_name")["quantity"].sum().sort_values(ascending=False)
category_sales = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
city_revenue   = df.groupby("city")["revenue"].sum().sort_values(ascending=False)
repeat_cust    = df.groupby("name")["order_date"].count()
repeat_cust    = repeat_cust[repeat_cust > 1].sort_values(ascending=False)

print("\n" + "=" * 55)
print("  MONTHLY REVENUE")
print("=" * 55)
print(monthly_sales.to_string())
print("\n" + "=" * 55)
print("  TOP CUSTOMERS BY REVENUE")
print("=" * 55)
print(top_customers.to_string())
print("\n" + "=" * 55)
print("  TOP PRODUCTS BY UNITS SOLD")
print("=" * 55)
print(top_products.to_string())
print("\n" + "=" * 55)
print("  CATEGORY REVENUE")
print("=" * 55)
print(category_sales.to_string())
print("\n" + "=" * 55)
print("  CITY REVENUE")
print("=" * 55)
print(city_revenue.to_string())
print("\n" + "=" * 55)
print("  REPEAT CUSTOMERS")
print("=" * 55)
print(repeat_cust.to_string() if len(repeat_cust) > 0 else "No repeat customers found")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_sales.index, monthly_sales.values, marker="o", color="#2196F3", linewidth=2.5)
ax.fill_between(monthly_sales.index, monthly_sales.values, alpha=0.1, color="#2196F3")
ax.set_title("Monthly Revenue Trend", fontsize=15, fontweight="bold")
ax.set_xlabel("Month"); ax.set_ylabel("Revenue")
ax.yaxis.set_major_formatter(fmt)
plt.xticks(rotation=45); plt.tight_layout()
plt.savefig("plot_01_monthly_revenue.png", dpi=150)
plt.show()
print("Saved: plot_01_monthly_revenue.png")

fig, ax = plt.subplots(figsize=(10, 5))
top_customers.plot(kind="bar", ax=ax, color="#9C27B0", edgecolor="white")
ax.set_title("Customers by Total Revenue", fontsize=15, fontweight="bold")
ax.set_xlabel("Customer"); ax.set_ylabel("Revenue")
ax.yaxis.set_major_formatter(fmt)
plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.savefig("plot_02_top_customers.png", dpi=150)
plt.show()
print("Saved: plot_02_top_customers.png")

fig, ax = plt.subplots(figsize=(10, 5))
top_products.plot(kind="bar", ax=ax, color="#4CAF50", edgecolor="white")
ax.set_title("Top Products by Units Sold", fontsize=15, fontweight="bold")
ax.set_xlabel("Product"); ax.set_ylabel("Quantity Sold")
plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.savefig("plot_03_top_products.png", dpi=150)
plt.show()
print("Saved: plot_03_top_products.png")

fig, ax = plt.subplots(figsize=(7, 7))
category_sales.plot(kind="pie", ax=ax, autopct="%1.1f%%", startangle=140,
                    colors=sns.color_palette("pastel"))
ax.set_ylabel("")
ax.set_title("Revenue by Category", fontsize=15, fontweight="bold")
plt.tight_layout()
plt.savefig("plot_04_category_revenue.png", dpi=150)
plt.show()
print("Saved: plot_04_category_revenue.png")

fig, ax = plt.subplots(figsize=(10, 5))
city_revenue.plot(kind="barh", ax=ax, color="#FF5722", edgecolor="white")
ax.set_title("Revenue by City", fontsize=15, fontweight="bold")
ax.set_xlabel("Revenue"); ax.xaxis.set_major_formatter(fmt)
plt.tight_layout()
plt.savefig("plot_05_city_revenue.png", dpi=150)
plt.show()
print("Saved: plot_05_city_revenue.png")

pivot = df.pivot_table(values="revenue", index="category", columns="city",
                       aggfunc="sum", fill_value=0)
fig, ax = plt.subplots(figsize=(13, 5))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax, linewidths=0.5)
ax.set_title("Revenue Heatmap: Category vs City", fontsize=15, fontweight="bold")
plt.tight_layout()
plt.savefig("plot_06_heatmap.png", dpi=150)
plt.show()
print("Saved: plot_06_heatmap.png")

customer_agg = df.groupby("customer_id").agg(
    total_revenue  = ("revenue",    "sum"),
    total_quantity = ("quantity",   "sum"),
    total_orders   = ("order_date", "count")
).reset_index()

scaler   = StandardScaler()
X_scaled = scaler.fit_transform(customer_agg[["total_revenue", "total_quantity", "total_orders"]])

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
customer_agg["segment"] = kmeans.fit_predict(X_scaled)

seg_avg   = customer_agg.groupby("segment")["total_revenue"].mean().sort_values(ascending=False)
label_map = {
    seg_avg.index[0]: "High-Value",
    seg_avg.index[1]: "Medium-Value",
    seg_avg.index[2]: "Low-Value"
}
customer_agg["segment_label"] = customer_agg["segment"].map(label_map)

print("\n" + "=" * 55)
print("  CUSTOMER SEGMENTS (K-Means)")
print("=" * 55)
print(customer_agg[["customer_id", "total_revenue", "total_orders", "segment_label"]].to_string(index=False))
print("\n  Segment Summary (Averages):")
print(customer_agg.groupby("segment_label")[["total_revenue", "total_orders"]].mean().round(2))

colors = {"High-Value": "#F44336", "Medium-Value": "#FF9800", "Low-Value": "#4CAF50"}
fig, ax = plt.subplots(figsize=(9, 6))
for label, group in customer_agg.groupby("segment_label"):
    ax.scatter(group["total_orders"], group["total_revenue"],
               label=label, color=colors[label], s=130, edgecolors="white", zorder=3)
ax.set_title("Customer Segmentation (K-Means)", fontsize=15, fontweight="bold")
ax.set_xlabel("Total Orders"); ax.set_ylabel("Total Revenue")
ax.yaxis.set_major_formatter(fmt); ax.legend()
plt.tight_layout()
plt.savefig("plot_07_segmentation.png", dpi=150)
plt.show()
print("Saved: plot_07_segmentation.png")

fig, ax = plt.subplots(figsize=(6, 6))
seg_counts = customer_agg["segment_label"].value_counts()
seg_counts.plot(kind="pie", ax=ax, autopct="%1.1f%%", startangle=140,
                colors=["#F44336", "#FF9800", "#4CAF50"])
ax.set_ylabel(""); ax.set_title("Customer Segment Distribution", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("plot_08_segment_pie.png", dpi=150)
plt.show()
print("Saved: plot_08_segment_pie.png")

seg_counts = customer_agg["segment_label"].value_counts()

print("\n" + "=" * 60)
print("     CUSTOMER BEHAVIOR ANALYSIS — FINAL INSIGHTS")
print("=" * 60)
print(f"\n  Total Revenue          : Rs.{df['revenue'].sum():,.0f}")
print(f"  Total Transactions     : {len(df)}")
print(f"  Unique Customers       : {df['customer_id'].nunique()}")
print(f"  Unique Products        : {df['product_name'].nunique()}")
print(f"  Avg Revenue per Order  : Rs.{df.groupby('order_date')['revenue'].sum().mean():,.0f}")
print(f"\n  Top Customer           : {top_customers.idxmax()}  —  Rs.{top_customers.max():,.0f}")
print(f"  Best Month             : {monthly_sales.idxmax()}  —  Rs.{monthly_sales.max():,.0f}")
print(f"  Best Category          : {category_sales.idxmax()}  —  Rs.{category_sales.max():,.0f}")
print(f"  Top City               : {city_revenue.idxmax()}  —  Rs.{city_revenue.max():,.0f}")
print(f"  Best Selling Product   : {top_products.idxmax()}  —  {top_products.max()} units")
print(f"\n  High-Value Customers   : {seg_counts.get('High-Value', 0)}")
print(f"  Medium-Value Customers : {seg_counts.get('Medium-Value', 0)}")
print(f"  Low-Value Customers    : {seg_counts.get('Low-Value', 0)}")
print("\n  8 plots saved in current folder.")
print("=" * 60)
