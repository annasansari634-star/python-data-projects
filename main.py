import pandas as pd
import matplotlib.pyplot as plt

# Load your actual matches.csv file
df = pd.read_csv('matches.csv')

# Check first few rows and column names
print("--- Data Preview ---")
print(df.head())

print("\n--- Columns in your dataset ---")
print(df.columns)

# Check column names
print(df.columns.tolist())
# 1. Load the matches dataset from the local folder
df = pd.read_csv('matches.csv')

print("--- Data Preview ---")
print(df.head())

# 2. Toss winner vs Match winner analysis
df['toss_winner_match_winner'] = df['toss_winner'] == df['winner']
toss_analysis = df['toss_winner_match_winner'].value_counts()
print("\n--- Toss Winner vs Match Winner ---")
print(toss_analysis)

# 3. Top teams by total wins
team_wins = df['winner'].value_counts().head(10)
print("\n--- Top Teams by Wins ---")
print(team_wins)

# 4. Visualizations using Matplotlib
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Bar chart for team wins
axes[0].bar(team_wins.index, team_wins.values, color='#ff6f61')
axes[0].set_title('Top Teams by Matches Won')
axes[0].set_xlabel('Team')
axes[0].set_ylabel('Wins')
axes[0].tick_params(axis='x', rotation=45)

# Plot 2: Season-wise match trend (if 'season' column exists)
if 'season' in df.columns:
    season_trends = df['season'].value_counts().sort_index()
    axes[1].plot(season_trends.index.astype(str), season_trends.values, marker='o', color='b', linewidth=2)
    axes[1].set_title('Matches per Season')
    axes[1].set_xlabel('Season')
    axes[1].set_ylabel('Number of Matches')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(True)

plt.tight_layout()
plt.show()