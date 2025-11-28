# pandas Cheatsheet (Beginner-Friendly)

This file collects simple pandas patterns you will use in this project.

You can update it as you learn more.

## Import pandas and Read CSV

```python
import pandas as pd

df = pd.read_csv("data/books.csv")
```

## Quick Overview

```python
df.head()
df.info()
df.describe()
```

## Selecting Columns

```python
df["title"]
df[["title", "average_rating"]]
```

## Filtering Rows

```python
high_rated = df[df["average_rating"] >= 4.0]
```

## Grouping and Aggregation

```python
avg_rating_by_author = (
    df.groupby("authors")["average_rating"]
      .mean()
      .sort_values(ascending=False)
)
```

## Simple Plot (if matplotlib is installed)

```python
import matplotlib.pyplot as plt

df["average_rating"].hist(bins=20)
plt.xlabel("Average Rating")
plt.ylabel("Count of Books")
plt.show()
```

Use these snippets as starting points in your notebooks and customize them for your analysis.
