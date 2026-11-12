import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the dataset
df = pd.read_csv('Mumbai_weather.csv')

print("--- Data Loaded Successfully ---")
print(df.head())

# 2. Data Cleaning & Preprocessing
# Convert DATE column to datetime format (format is DD-MM-YYYY based on preview)
df['DATE'] = pd.to_datetime(df['DATE'], format='%d-%m-%Y')

# Sort by date and set as index
df = df.sort_values('DATE')
df.set_index('DATE', inplace=True)

# Handle missing values if any
df['T2M'] = df['T2M'].ffill()

# 3. Calculate Rolling Average (30-day smoothing for clear temperature trends)
df['Temp_Rolling_30d'] = df['T2M'].rolling(window=30).mean()

# 4. Visualizations (Multi-line trend dashboard)
plt.figure(figsize=(14, 6))

# Plot daily temperature vs 30-day rolling average
plt.plot(df.index, df['T2M'], label='Daily Temperature (T2M)', color='#a6c8e0', alpha=0.5)
plt.plot(df.index, df['Temp_Rolling_30d'], label='30-Day Rolling Average', color='#d9534f', linewidth=2)

plt.title('Mumbai Weather Trend Dashboard (Temperature Analysis)')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()