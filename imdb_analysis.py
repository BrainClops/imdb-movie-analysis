"""
IMDb Top 1000 Movies - Data Cleaning & Analysis
------------------------------------------------
Dataset: IMDb Top 1000 (from Kaggle)
Goal: Clean the raw data and pull out some interesting insights
      like top genres, rating trends over the years, top directors, etc.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# IMDb style theme - black background with gold/yellow accents
plt.rcParams["figure.facecolor"] = "#000000"
plt.rcParams["axes.facecolor"] = "#141414"
plt.rcParams["savefig.facecolor"] = "#000000"
plt.rcParams["axes.edgecolor"] = "#F5C518"
plt.rcParams["axes.labelcolor"] = "white"
plt.rcParams["text.color"] = "white"
plt.rcParams["xtick.color"] = "white"
plt.rcParams["ytick.color"] = "white"
plt.rcParams["axes.titlecolor"] = "#F5C518"
plt.rcParams["grid.color"] = "#333333"

IMDB_GOLD = "#F5C518"

# ---------------------------
# STEP 1: Load the data
# ---------------------------
df = pd.read_csv("imdb_top_1000.csv")
print("Original shape:", df.shape)
print(df.head())

# ---------------------------
# STEP 2: Clean the data
# ---------------------------

# Released_Year has some weird values, converting to numeric
df["Released_Year"] = pd.to_numeric(df["Released_Year"], errors="coerce")

# Runtime is like "142 min" -> need only the number
df["Runtime"] = df["Runtime"].str.replace(" min", "").astype(int)

# Gross has commas like "28,341,469" -> remove commas, convert to number
df["Gross"] = df["Gross"].str.replace(",", "")
df["Gross"] = pd.to_numeric(df["Gross"], errors="coerce")

# Genre column has multiple genres separated by comma eg "Crime, Drama"
# taking just the first genre for simplicity
df["Main_Genre"] = df["Genre"].apply(lambda x: x.split(",")[0].strip())

# dropping rows where year is missing (very few)
df = df.dropna(subset=["Released_Year"])

print("\nAfter cleaning:")
print(df.info())

# ---------------------------
# STEP 3: Analysis
# ---------------------------

# 3.1 Which genre appears the most?
genre_counts = df["Main_Genre"].value_counts().head(10)
print("\nTop 10 Genres:\n", genre_counts)

plt.figure(figsize=(10, 6))
sns.barplot(x=genre_counts.values, y=genre_counts.index, color=IMDB_GOLD)
plt.title("Top 10 Genres in IMDb Top 1000")
plt.xlabel("Number of Movies")
plt.ylabel("Genre")
plt.tight_layout()
plt.savefig("top_genres.png")
plt.close()

# 3.2 Average rating by decade
df["Decade"] = (df["Released_Year"] // 10 * 10).astype(int)
rating_by_decade = df.groupby("Decade")["IMDB_Rating"].mean()
print("\nAverage rating by decade:\n", rating_by_decade)

plt.figure(figsize=(10, 6))
rating_by_decade.plot(kind="line", marker="o", color=IMDB_GOLD, linewidth=2, markersize=8, markerfacecolor="white")
plt.title("Average IMDb Rating by Decade")
plt.xlabel("Decade")
plt.ylabel("Average Rating")
plt.tight_layout()
plt.savefig("rating_by_decade.png")
plt.close()

# 3.3 Top 10 directors with most movies in the list
top_directors = df["Director"].value_counts().head(10)
print("\nTop 10 Directors:\n", top_directors)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_directors.values, y=top_directors.index, color=IMDB_GOLD)
plt.title("Directors with Most Movies in IMDb Top 1000")
plt.xlabel("Number of Movies")
plt.ylabel("Director")
plt.tight_layout()
plt.savefig("top_directors.png")
plt.close()

# 3.4 Does runtime affect rating?
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="Runtime", y="IMDB_Rating", alpha=0.6, color=IMDB_GOLD)
plt.title("Runtime vs IMDb Rating")
plt.xlabel("Runtime (minutes)")
plt.ylabel("IMDb Rating")
plt.tight_layout()
plt.savefig("runtime_vs_rating.png")
plt.close()

# 3.5 Highest grossing movies
top_gross = df.sort_values("Gross", ascending=False).head(10)[["Series_Title", "Gross", "IMDB_Rating"]]
print("\nTop 10 Highest Grossing Movies:\n", top_gross)

plt.figure(figsize=(10, 6))
sns.barplot(x="Gross", y="Series_Title", data=top_gross, color=IMDB_GOLD)
plt.title("Top 10 Highest Grossing Movies")
plt.xlabel("Gross Earnings (USD)")
plt.ylabel("Movie")
plt.tight_layout()
plt.savefig("top_grossing.png")
plt.close()

print("\nAll charts saved! Check the folder for the PNG files.")
