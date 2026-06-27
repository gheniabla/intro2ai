# Week 3 — Data Visualization: Pandas & Matplotlib
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of September 7, 2026 · Online / Asynchronous*

> **Holiday note:** Monday Sep 7 is **Labor Day** (campus closed). The module still opens this week and A3 is due Sunday 11:59 PM PT.

---

## Learning objectives
By the end of this week you will be able to:
1. Use **Pandas** `DataFrame` and `Series` to load, inspect, and clean tabular data.
2. **Select** data by label (`.loc`) and position (`.iloc`), and filter rows with boolean conditions.
3. **Group and aggregate** with `groupby` to answer "per-category" questions.
4. Detect and handle **missing data** (`isna`, `dropna`, `fillna`).
5. Build core **Matplotlib** charts: **line, bar, scatter, histogram** — and know when to use each.
6. Apply all of the above to the **A–Z Handwritten Digits/Letters** dataset and *see* what the pixels look like.

> **Time budget:** ~10 hours this week (lecture + slides + videos + Lab A3).

---

## 1. From NumPy arrays to Pandas DataFrames
Last week every column was just a position in a NumPy array. **Pandas** adds **labels**: named columns and an index. A `DataFrame` is a table (think a spreadsheet or SQL table); each column is a `Series`. Under the hood it is still NumPy — so everything you learned last week still applies.

```python
import pandas as pd
df = pd.DataFrame({
    "name":  ["Ada", "Alan", "Grace"],
    "score": [91, 78, 88],
    "hours": [6.0, 3.5, 5.0],
})
df.head()      # first rows
df.shape       # (rows, columns)
df.info()      # dtypes + non-null counts
df.describe()  # count/mean/std/min/quartiles/max per numeric column
```

`head()`, `info()`, and `describe()` are the first three things you run on **any** new dataset.

---

## 2. Reading data & inspecting it
Most real data arrives as CSV. Pandas reads it in one line:

```python
df = pd.read_csv("data.csv")
df.columns        # the column labels
df.dtypes         # type of each column
df["score"]       # a single column (a Series)
df[["name", "score"]]   # several columns (a DataFrame)
```

In Colab you can read straight from a URL, or upload a file with the file panel.

---

## 3. Selecting and filtering
Two label-aware accessors do most of the work:
- **`.loc[rows, cols]`** — select by **label**.
- **`.iloc[rows, cols]`** — select by **integer position**.

```python
df.loc[0]                       # row with index label 0
df.loc[:, "score"]              # the score column
df.iloc[0:3, 0:2]               # first 3 rows, first 2 cols (by position)

# Boolean filtering — the everyday workhorse
df[df["score"] >= 85]                       # high scorers
df[(df["score"] >= 85) & (df["hours"] < 6)] # combine with & / |
```

### 3.1 Creating columns
```python
df["passed"] = df["score"] >= 80          # new boolean column
df["per_hour"] = df["score"] / df["hours"]# vectorized, like NumPy
```

---

## 4. Group, aggregate, and summarize
`groupby` answers **"per-category"** questions — the heart of analytics. Split the rows into groups, apply an aggregation, combine the results.

```python
df.groupby("passed")["score"].mean()      # average score, passed vs not
df.groupby("team").agg(
    avg_score=("score", "mean"),
    n=("score", "size"),
)
df["team"].value_counts()                 # how many rows per category
```

---

## 5. Missing data
Real datasets have holes. Pandas marks them as `NaN`. You must **find** them and **decide** what to do.

```python
df.isna().sum()              # count missing per column
df.dropna()                  # drop rows with ANY missing value
df.dropna(subset=["score"])  # only where 'score' is missing
df["score"].fillna(df["score"].mean())   # fill with the column mean
```

There is no single "right" choice — dropping loses data, filling invents it. Always state what you did and why.

---

## 6. Matplotlib — four charts you will use constantly
Matplotlib is the base plotting library; Pandas plots call it under the hood. Pick the chart by the **question** you are asking.

| Chart | Use it when… | Code |
|---|---|---|
| **Line** | a value changes over an ordered axis (time, steps) | `plt.plot(x, y)` |
| **Bar** | comparing a quantity across categories | `plt.bar(cats, vals)` |
| **Scatter** | looking for a relationship between two numbers | `plt.scatter(x, y)` |
| **Histogram** | seeing the distribution / spread of one variable | `plt.hist(vals, bins=20)` |

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(6, 4))
plt.scatter(df["hours"], df["score"])
plt.xlabel("hours studied")
plt.ylabel("exam score")
plt.title("Hours vs Score")
plt.show()
```

**Always label your axes and add a title.** An unlabeled chart is not a result.

---

## 7. Putting it together: the A–Z Handwritten dataset
The motivating dataset this week is **A–Z Handwritten Data** (`A_Z-HandwrittenData.csv`). Each row is one handwritten character: the **first column is a label** (0–25 → A–Z) and the remaining **784 columns are pixel intensities** of a 28×28 grayscale image (0 = black, 255 = white).

This is your first taste of the data shape behind image ML:
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("A_Z-HandwrittenData.csv", header=None)
labels = df.iloc[:, 0].values            # 0..25
pixels = df.iloc[:, 1:].values           # (n, 784)

# show ONE character: reshape its 784 pixels back to 28x28
img = pixels[0].reshape(28, 28)
plt.imshow(img, cmap="gray")
plt.title("label = " + chr(ord("A") + labels[0]))
plt.axis("off")
plt.show()

# how many examples of each letter? -> a bar chart
counts = pd.Series(labels).value_counts().sort_index()
plt.bar([chr(ord("A") + i) for i in counts.index], counts.values)
plt.title("Examples per letter")
plt.show()
```
You will use Pandas to load and slice, NumPy `reshape` (from Week 2!) to turn a row into an image, and Matplotlib to display it. The notebook does all of this on a small sample so it runs fast in Colab.

---

## 8. Reading & videos
- **chapter2.ipynb** and **chapter3.ipynb** (Canvas) — the prior Pandas + visualization walkthroughs.
- **A_Z-HandwrittenData.csv.zip** (Canvas) — this week's dataset.
- Pandas **"10 minutes to pandas"** (pandas.pydata.org) — required skim.
- Matplotlib **"Pyplot tutorial"** (matplotlib.org).
- Video: "Pandas in 10 minutes" (linked in Canvas).

---

## 9. Lab — Assignment A3 (due Sunday 11:59 PM PT)
**Goal:** load, clean, group, and visualize a real dataset.

1. Open `code/01_pandas_basics.ipynb`, run all cells, and complete the **5 exercises** (selection, filtering, a new column, a `groupby`, and handling missing values).
2. Open `code/02_visualization_AZ.ipynb`. Load the A–Z handwritten dataset (a small sample is fetched for you), then:
   - display a 3×3 grid of handwritten characters with their labels,
   - make a **bar chart** of how many examples each letter has,
   - make a **histogram** of average pixel brightness per image.
3. Write 100–150 words: what does the per-letter bar chart tell you about whether this dataset is **balanced**, and why would imbalance matter for training a model later?
4. **(Optional sidebar)** Ask **Claude** or **Gemini** to suggest one additional chart that would reveal something about the dataset, then build it.
5. **Submit:** both completed notebooks (or Colab share links) + your write-up. Include a one-line **AI Use** disclosure.

*A3 is graded for correctness on the exercises (see syllabus).*

---

## Key terms
**DataFrame**, **Series**, **index**, **`.loc` / `.iloc`**, **boolean filter**, **`groupby`**, **aggregation**, **`NaN` / missing data**, **histogram**, **scatter / bar / line plot**.
