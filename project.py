# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Data Ingestion
# Load CSV files into pandas DataFrames
customers = pd.read_csv('customers.csv')
transactions = pd.read_csv('transactions.csv')
products = pd.read_csv('products.csv')

# Step 2: Data Cleaning
# Merge data into a single DataFrame
data = pd.merge(transactions, customers, on='customer_id')
data = pd.merge(data, products, on='product_id')

# Handle missing values
data.fillna(0, inplace=True)

# Correct data types if necessary
data['transaction_date'] = pd.to_datetime(data['transaction_date'])

# Step 3: Data Manipulation
# Group data by customer ID to calculate total spending and purchase frequency
customer_spending = data.groupby('customer_id').agg(
    total_spent=('transaction_amount', 'sum'),
    purchase_count=('transaction_id', 'count')
).reset_index()

# Identify high-value customers based on spending
high_value_customers = customer_spending[customer_spending['total_spent'] > 500]

# Step 4: Data Visualization
# Visualize total sales by region
sales_by_region = data.groupby('region')['transaction_amount'].sum().reset_index()

plt.figure(figsize=(8, 6))
sns.barplot(x='region', y='transaction_amount', data=sales_by_region)
plt.title('Total Sales by Region')
plt.xlabel('Region')
plt.ylabel('Total Sales')
plt.show()

# Visualize customer purchase patterns over time
data['month'] = data['transaction_date'].dt.to_period('M')
monthly_sales = data.groupby('month')['transaction_amount'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(x='month', y='transaction_amount', data=monthly_sales)
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.show()

# Save high-value customers to a CSV
high_value_customers.to_csv('high_value_customers.csv', index=False)
