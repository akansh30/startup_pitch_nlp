import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# loading the scored CSV file
df = pd.read_csv("results/deck_scores.csv")

# Cleaning deck names for display
df['Deck Name'] = df['Deck Name'].apply(lambda x: x.replace("-", "\n"))

# 1. BAR CHART: Total Score per Deck
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Deck Name', y='Total Score', palette='viridis')
plt.title('Total Score per Pitch Deck')
plt.ylabel('Total Score')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("output_visualization/total_score_barplot.png")
plt.show()


# 2. RADAR CHART: Top 3 Decks
from math import pi

categories = ['Problem', 'Market Size', 'Traction', 'Team', 'Business Model', 'Moat / Vision']
N = len(categories)

top3 = df.sort_values(by='Total Score', ascending=False).head(3)

plt.figure(figsize=(6, 6))
for i, row in top3.iterrows():
    values = row[categories].tolist()
    values += values[:1]
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    plt.polar(angles, values, label=row['Deck Name'])

plt.xticks([n / float(N) * 2 * pi for n in range(N)], categories)
plt.title('Radar Chart of Top 3 Decks')
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
plt.savefig("output_visualization/radar_top3.png",bbox_inches='tight')
plt.show()


# 3. HEATMAP: Score Correlations 
plt.figure(figsize=(8, 6))
sns.heatmap(df[categories + ['Total Score']].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Between Scores")
plt.tight_layout()
plt.savefig("output_visualization/score_correlation_heatmap.png", bbox_inches='tight')
plt.show()
