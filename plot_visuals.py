import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd

# Create visuals directory if it doesn't exist
os.makedirs("data/visuals", exist_ok = True)

df = pd.read_csv("data/epl_standings.csv")

# Prepare title odds chart
title_df = df[["team", "1"]].sort_values("1", ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(data=title_df, y="team", x="1", palette="Blues_d")
plt.title("Top 10 Teams - Title Win Probability")
plt.xlabel("Chance to Finish 1st (%)")
plt.ylabel("Team")
plt.tight_layout()
title_plot_path = "data/visuals/title_odds.png"
plt.savefig(title_plot_path)
plt.close()

# Prepare volatility chart: standard deviation across positions
position_cols = [str(i) for i in range(1, 21)]
volatility_df = df.copy()
volatility_df["volatility"] = df[position_cols].std(axis=1)
volatility_df = volatility_df.sort_values("volatility", ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(data=volatility_df, x="volatility", y="team", palette="Reds_r")
plt.title("Top 10 Most Volatile Teams (Finish Position Std Dev)")
plt.xlabel("Standard Deviation of Position")
plt.ylabel("Team")
plt.tight_layout()
volatility_plot_path = "data/visuals/volatility_chart.png"
plt.savefig(volatility_plot_path)
plt.close()

# Return paths
title_plot_path, volatility_plot_path
