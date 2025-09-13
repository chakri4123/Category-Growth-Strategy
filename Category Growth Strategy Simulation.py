# Category Growth Strategy Simulation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import pandasql as ps

# -----------------------------
# Step 1: Create dummy dataset
# -----------------------------
np.random.seed(42)
categories = ["Apparel", "Electronics", "Home", "Beauty"]
regions = ["North", "South", "East", "West"]

data = {
    "order_id": np.arange(1, 501),
    "customer_id": np.random.randint(1000, 2000, 500),
    "category": np.random.choice(categories, 500, p=[0.4, 0.25, 0.2, 0.15]),
    "price": np.random.randint(200, 2000, 500),
    "discount": np.random.choice([0, 0.05, 0.1, 0.2], 500),
    "quantity": np.random.randint(1, 5, 500),
    "region": np.random.choice(regions, 500)
}
df = pd.DataFrame(data)
df.to_csv("sales_data.csv", index=False)

print(df.head())

# -----------------------------
# Step 2: Customer segmentation
# -----------------------------
df["net_sales"] = df["price"] * df["quantity"] * (1 - df["discount"])
segment = df.groupby("category")["net_sales"].sum().reset_index()
sns.barplot(x="category", y="net_sales", data=segment)
plt.title("Category Revenue Contribution")
plt.show()

# -----------------------------
# Step 3: Pricing Simulation
# -----------------------------
df["new_price"] = df["price"] * 0.9  # simulate 10% discount
df["new_sales"] = df["new_price"] * df["quantity"]
old_revenue = df["net_sales"].sum()
new_revenue = df["new_sales"].sum()

print(f"Old Revenue: {old_revenue:,.0f}")
print(f"New Revenue (with promo): {new_revenue:,.0f}")
print(f"Conversion improvement: {(new_revenue - old_revenue)/old_revenue * 100:.2f}%")

# -----------------------------
# Step 4: SQL queries
# -----------------------------
query = """
SELECT category, region, SUM(net_sales) as total_sales
FROM df
GROUP BY category, region
ORDER BY total_sales DESC
"""
result = ps.sqldf(query, locals())
print(result.head())

# -----------------------------
# Step 5: Visualization
# -----------------------------
plt.figure(figsize=(8,5))
sns.boxplot(x="category", y="price", data=df)
plt.title("Price Distribution by Category")
plt.show()