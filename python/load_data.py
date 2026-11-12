import pandas as pd 
import matplotlib.pyplot as plt
file_path = r"C:\Users\thomas\OneDrive\Pictures\ourjobready\data\online_retail.csv"

df = pd.read_csv(file_path, encoding="latin1")

print("dataset loaded successfully!")

print("dataset shape:")
print(df.shape)

print("first 5 rows:")
print(df.head())

print("dataset information:")
df.info()

print("column names:")
print(df.columns)


print("\nmissing values:")
print(df.isnull().sum())

print("\nStatistical summery:")
print(df.describe())

print("\nnumber of countries:")
print(df["Country"].nunique())

print("\n country list:")
print(df["Country"].unique())

print("\n missing values percentage:")
print((df.isnull().sum()/len(df)*100).round(2))


print("\n duplicate rows:")
print(df.duplicated().sum())

print("\n negative quantity records:")
print((df["Quantity"]<0).sum())

print("\n negative price records:")
print((df["UnitPrice"] < 0).sum())

print("duplicate records:")
print(df[df.duplicated()].head(10))

print("\n negative quantity examples")
print(df[df["Quantity"]<0])


# Create a cleaned copy
clean_df = df.copy()

# 1. Remove duplicate rows
clean_df = clean_df.drop_duplicates()

# 2. Convert InvoiceDate into datetime
clean_df["InvoiceDate"] = pd.to_datetime(
    clean_df["InvoiceDate"],
    format="%d-%m-%Y %H:%M"
)

# 3. Check the cleaned dataset
print("\n--- CLEANING RESULTS ---")

print("Original rows:", len(df))
print("Rows after removing duplicates:", len(clean_df))

print("\nMissing values:")
print(clean_df.isnull().sum())

print("\nData types:")
print(clean_df.dtypes)

print("\nDataset shape:")
print(clean_df.shape)


# Create revenue column
clean_df["Revenue"] = clean_df["Quantity"] * clean_df["UnitPrice"]

# Display first 10 records
print("\n--- REVENUE COLUMN ---")
print(clean_df[["Quantity", "UnitPrice", "Revenue"]].head(10))

# Calculate total recorded revenue
total_revenue = clean_df["Revenue"].sum()

print("\nTotal recorded revenue:")
print(round(total_revenue, 2))


# Create revenue column
clean_df["Revenue"] = clean_df["Quantity"] * clean_df["UnitPrice"]

# Display first 10 records
print("\n--- REVENUE COLUMN ---")
print(clean_df[["Quantity", "UnitPrice", "Revenue"]].head(10))

# Calculate total recorded revenue
total_revenue = clean_df["Revenue"].sum()

print("\nTotal recorded revenue:")
print(round(total_revenue, 2))


# Filter positive-quantity sales
sales_df = clean_df[clean_df["Quantity"] > 0]

# Calculate total positive-sales revenue
positive_revenue = sales_df["Revenue"].sum()

print("Positive sales revenue:", round(positive_revenue, 2))


# Filter positive sales
sales_df = clean_df[
    (clean_df["Quantity"] > 0) &
    (clean_df["UnitPrice"] >= 0)
].copy()

# Calculate sales KPIs
total_revenue = clean_df["Revenue"].sum()
positive_revenue = sales_df["Revenue"].sum()
total_transactions = len(clean_df)
total_invoices = clean_df["InvoiceNo"].nunique()
total_customers = clean_df["CustomerID"].nunique()
total_products = clean_df["StockCode"].nunique()

# Display results
print("\n========== SALES KPI REPORT ==========")

print("Total recorded net revenue:", round(total_revenue, 2))
print("Positive sales revenue:", round(positive_revenue, 2))
print("Total transaction records:", total_transactions)
print("Unique invoices:", total_invoices)
print("Unique customers:", total_customers)
print("Unique products:", total_products)


# =====================================
# 1. COUNTRY-WISE REVENUE
# =====================================

country_analysis = (
    sales_df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- TOP 10 COUNTRIES ---")
print(country_analysis.head(10))


# =====================================
# 2. MONTHLY REVENUE
# =====================================

sales_df["SalesMonth"] = (
    sales_df["InvoiceDate"].dt.to_period("M")
)

monthly_analysis = (
    sales_df.groupby("SalesMonth")["Revenue"]
    .sum()
    .sort_index()
)

print("\n--- MONTHLY REVENUE ---")
print(monthly_analysis)


# =====================================
# 3. TOP 10 PRODUCTS
# =====================================

product_analysis = (
    sales_df.groupby(["StockCode", "Description"])["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n--- TOP 10 PRODUCTS ---")
print(product_analysis)


# =====================================
# 4. TOP 10 CUSTOMERS
# =====================================

customer_analysis = (
    sales_df.dropna(subset=["CustomerID"])
    .groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n--- TOP 10 CUSTOMERS ---")
print(customer_analysis)

# CUSTOMER BEHAVIOUR ANALYSIS
customer_data = sales_df.dropna(subset=["CustomerID"])

customer_behaviour = (
    customer_data.groupby("CustomerID")
    .agg(
        Total_Orders=("InvoiceNo", "nunique"),
        Total_Quantity=("Quantity", "sum"),
        Total_Revenue=("Revenue", "sum")
    )
)

# Average revenue per order
customer_behaviour["Average_Order_Value"] = (
    customer_behaviour["Total_Revenue"] /
    customer_behaviour["Total_Orders"]
)

# Sort by total revenue
customer_behaviour = customer_behaviour.sort_values(
    by="Total_Revenue",
    ascending=False
)

print("\n--- CUSTOMER BEHAVIOUR ---")
print(customer_behaviour.head(10))

# Overall customer behaviour summary
print("\n--- CUSTOMER SUMMARY ---")
print(customer_behaviour.describe().round(2))


# =====================================
# PYTHON DATA VISUALISATION
# =====================================

# 1. Monthly Revenue Trend
plt.figure(figsize=(12, 5))
monthly_analysis.plot(kind="line", marker="o")

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# 2. Top 10 Countries
plt.figure(figsize=(12, 5))
country_analysis.head(10).sort_values().plot(kind="barh")

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue (£)")
plt.ylabel("Country")
plt.tight_layout()
plt.show()


# 3. Top 10 Physical Products
physical_sales = sales_df[
    ~sales_df["StockCode"].isin(["DOT", "POST", "M"])
]

top_products = (
    physical_sales.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))
top_products.sort_values().plot(kind="barh")

plt.title("Top 10 Physical Products by Revenue")
plt.xlabel("Revenue (£)")
plt.ylabel("Product")
plt.tight_layout()
plt.show()


# 4. Top 10 Customers
plt.figure(figsize=(12, 5))
customer_analysis.sort_values().plot(kind="barh")

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Revenue (£)")
plt.ylabel("Customer ID")
plt.tight_layout()
plt.show()


from pathlib import Path

# Create output folder
output_folder = Path(__file__).parent / "outputs"
output_folder.mkdir(exist_ok=True)

# Export analysis results
country_analysis.to_frame("Revenue").to_csv(
    output_folder / "country_revenue.csv"
)

monthly_analysis.to_frame("Revenue").to_csv(
    output_folder / "monthly_revenue.csv"
)

top_products.to_frame("Revenue").to_csv(
    output_folder / "top_products.csv"
)

customer_analysis.to_frame("Revenue").to_csv(
    output_folder / "top_customers.csv"
)

customer_behaviour.to_csv(
    output_folder / "customer_behaviour.csv"
)

sales_df.to_csv(
    output_folder / "cleaned_retail_data.csv",
    index=False
)

print("\nAll analysis files exported successfully!")


