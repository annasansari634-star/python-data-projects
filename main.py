import pandas as pd
df = pd.read_csv('expenses.csv')
df['date'] = pd.to_datetime(df['date'])

category_wise = df.groupby('category')['amount'].sum().sort_values(ascending=False)
print("--- Category-wise Total Expense ---")
print(category_wise)

df['month'] = df['date'].dt.to_period('M')
monthly_wise = df.groupby('month')['amount'].sum()
print("\n--- Monthly Total Expense ---")
print(monthly_wise)

import matplotlib.pyplot as plt

# 1. grouping data for the charts
# category totals for pie chart
category_totals = df.groupby('category')['amount'].sum()

# monthly totals for line trend
df['month_str'] = df['date'].dt.strftime('%Y-%m') # simple month format like 2026-01
monthly_totals = df.groupby('month_str')['amount'].sum()

# 2. setting up the figure size
plt.figure(figsize=(14, 6))

# --- Plot 1: Pie chart for category breakdown ---
plt.subplot(1, 2, 1) # 1 row, 2 columns, first plot
plt.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
plt.title('Where does the money go?')

# --- Plot 2: Line chart for monthly trend ---
plt.subplot(1, 2, 2) # 1 row, 2 columns, second plot
plt.plot(monthly_totals.index, monthly_totals.values, marker='o', color='purple', linewidth=2)
plt.title('Monthly Expense Trend')
plt.xlabel('Month')
plt.ylabel('Total Amount')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)

# show both plots together
plt.tight_layout()
plt.show()