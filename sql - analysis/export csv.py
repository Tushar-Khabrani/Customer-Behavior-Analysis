import pandas as pd
import mysql.connector
import os

conn = mysql.connector.connect(
    host     = "localhost",
    user     = "root",
    password = "Tush@rK104",  
    database = "customer_behavior"
)

print("✅ MySQL Connected!")

output_folder = "csv_exports"
os.makedirs(output_folder, exist_ok=True)

tables = ["customers", "products", "orders", "order_items"]

for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    filepath = os.path.join(output_folder, f"{table}.csv")
    df.to_csv(filepath, index=False)
    print(f"✅ Exported: {filepath}  ({len(df)} rows)")

query = """
    SELECT
        c.customer_id,
        c.name,
        c.city,
        DATE(o.order_date)      AS order_date,
        p.product_name,
        p.category,
        p.price,
        oi.quantity,
        (p.price * oi.quantity) AS revenue
    FROM orders o
    JOIN customers   c  ON o.customer_id  = c.customer_id
    JOIN order_items oi ON o.order_id     = oi.order_id
    JOIN products    p  ON oi.product_id  = p.product_id
    ORDER BY o.order_date
"""
df_joined = pd.read_sql(query, conn)
filepath = os.path.join(output_folder, "customer_data.csv")
df_joined.to_csv(filepath, index=False)
print(f"✅ Exported: {filepath}  ({len(df_joined)} rows)  ← Ye analytical dataset hai")

conn.close()

print("\n🎉 Done! Saare CSV files yahan save hue:")
print(f"   📁 {os.path.abspath(output_folder)}/")
for f in os.listdir(output_folder):
    print(f"      └─ {f}")