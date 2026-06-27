# Week 2 — Python Data Processing & Analytics with NumPy
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of August 31, 2026 · Online / Asynchronous*

---

## Learning objectives
By the end of this week you will be able to:
1. Explain why **NumPy arrays** are the foundation of every AI/ML library (Pandas, scikit-learn, PyTorch all build on them).
2. Create, reshape, and inspect arrays; understand `shape`, `dtype`, `ndim`, and `axis`.
3. Replace Python loops with **vectorized** operations and understand why they are dramatically faster.
4. Use **broadcasting** to combine arrays of different shapes without writing loops.
5. **Index, slice, and mask** arrays to select exactly the data you want.
6. Run **axis-based aggregations** (sum, mean, std) and simple statistics over real datasets.

> **Time budget:** ~10 hours this week (lecture + slides + videos + Lab A2).

---

## 1. Why NumPy?
Last week we used plain Python lists. Lists are flexible, but for **numerical data at scale** they are slow and clumsy. Every AI library you will touch this semester — Pandas, scikit-learn, PyTorch, TensorFlow — represents data as **N-dimensional arrays of numbers**. NumPy is the package that defines that array type (`ndarray`) and the math that runs on it.

Three reasons NumPy matters for AI:
- **Speed:** array math runs in optimized C, often 10–100× faster than a Python loop.
- **Vectorization:** you write `a + b` instead of looping element by element — closer to the math notation.
- **Memory layout:** a contiguous block of one `dtype`, which is exactly what GPUs and ML libraries expect.

```python
import numpy as np
a = np.array([1, 2, 3, 4])
print(a, a.dtype, a.shape)   # [1 2 3 4] int64 (4,)
```

---

## 2. Creating arrays
You rarely type arrays by hand. NumPy gives you constructors:

```python
import numpy as np

np.array([[1, 2, 3], [4, 5, 6]])  # from a Python list-of-lists
np.zeros((2, 3))                   # all zeros, shape 2×3
np.ones(4)                         # [1. 1. 1. 1.]
np.arange(0, 10, 2)                # [0 2 4 6 8]
np.linspace(0, 1, 5)               # 5 evenly spaced points 0..1
np.random.default_rng(0).random((2, 2))  # reproducible random
```

### 2.1 Inspecting an array
Every array has attributes you will check constantly:
- `arr.shape` — the size along each dimension, e.g. `(3, 4)`.
- `arr.ndim` — number of dimensions (1 = vector, 2 = matrix).
- `arr.dtype` — element type (`int64`, `float64`, `bool`, …).
- `arr.size` — total number of elements.

### 2.2 Reshaping
The same data can be viewed in different shapes:

```python
a = np.arange(12)          # shape (12,)
b = a.reshape(3, 4)        # shape (3, 4) — no data copied
c = a.reshape(2, -1)       # -1 means "figure out this dimension"
```

This matters in ML: a 28×28 image (784 pixels) is often **flattened** to a length-784 vector with `reshape(-1)`.

---

## 3. Vectorization — stop writing loops
A **vectorized** operation applies to the whole array at once. Compare:

```python
# Slow, Pythonic loop
out = []
for x in range(1_000_000):
    out.append(x * 2)

# Fast, vectorized — runs in C
import numpy as np
out = np.arange(1_000_000) * 2
```

The second version is both shorter *and* much faster. Arithmetic (`+ - * / **`), comparisons (`>`, `==`), and math functions (`np.sqrt`, `np.exp`, `np.sin`) all work element-wise:

```python
a = np.array([1.0, 4.0, 9.0])
np.sqrt(a)          # [1. 2. 3.]
a > 3               # [False  True  True]
a * 10 + 1          # [11. 41. 91.]
```

You will benchmark this in the notebook with `%timeit` and *see* the speedup.

---

## 4. Broadcasting
**Broadcasting** lets NumPy combine arrays of different shapes by virtually "stretching" the smaller one. This is how you add a scalar to every element, or a row vector to every row of a matrix — with no loop.

```python
prices = np.array([10.0, 20.0, 30.0])
prices * 1.08            # add 8% tax to all → [10.8 21.6 32.4]

matrix = np.ones((3, 3))
row    = np.array([1, 2, 3])
matrix + row             # row added to EACH row of the matrix
```

The rule: NumPy compares shapes from the right; dimensions are compatible when they are **equal** or one of them is **1**. A common ML use is **standardizing** features — subtract the mean and divide by the std of each column:

```python
X = np.random.default_rng(0).random((100, 4))
X_std = (X - X.mean(axis=0)) / X.std(axis=0)   # broadcasting over rows
```

---

## 5. Indexing, slicing, and boolean masks
Selecting the right subset of data is half of data processing.

```python
a = np.arange(10)        # [0 1 2 3 4 5 6 7 8 9]
a[0], a[-1]              # first, last
a[2:5]                   # [2 3 4]   (slice)
a[::2]                   # [0 2 4 6 8] (every 2nd)

m = np.arange(12).reshape(3, 4)
m[1, 2]                  # row 1, col 2
m[:, 0]                  # whole first column
m[0:2, 1:3]              # sub-block
```

### 5.1 Boolean (mask) indexing — the workhorse
You can select elements with a condition. This is how you filter datasets:

```python
data = np.array([3, -1, 7, -5, 9])
data[data > 0]           # [3 7 9]   keep positives
data[data < 0] = 0       # clip negatives to 0 → [3 0 7 0 9]
np.where(data > 5, 1, 0) # 1 where >5 else 0
```

---

## 6. Axis operations & simple statistics
The single most important idea for analytics: **`axis`** tells an aggregation *which direction to collapse*.

```python
scores = np.array([[90, 80, 70],
                   [60, 75, 95]])
scores.sum()             # 470  — everything
scores.sum(axis=0)       # [150 155 165] — sum down each COLUMN
scores.sum(axis=1)       # [240 230]      — sum across each ROW
```

Think: `axis=0` collapses rows (gives you a per-column result), `axis=1` collapses columns (per-row result). The same applies to `mean`, `std`, `min`, `max`, `argmax`:

```python
scores.mean(axis=0)      # average per subject
scores.max(axis=1)       # best score per student
scores.argmax(axis=1)    # WHICH subject each student scored highest in
```

These five lines are the core of "analytics": load data into a 2-D array (rows = samples, columns = features) and summarize along an axis. That is exactly the shape ML models expect.

---

## 7. Reading & videos
- **chapter1.ipynb** (Canvas) — the prior NumPy walkthrough; our two notebooks modernize it.
- NumPy official **"Absolute Beginner's Guide"** (numpy.org) — required skim.
- *Machine Learning Systems* (mlsysbook.ai) — the "data engineering" chapter intro.
- Video: "NumPy in 1 hour" (linked in Canvas).

---

## 8. Lab — Assignment A2 (due Sunday 11:59 PM PT)
**Goal:** process and analyze a real dataset using only NumPy.

1. Open `code/01_numpy_basics.ipynb`, run every cell, and complete the **6 exercises** (creation, reshaping, vectorization, broadcasting, masking, axis ops).
2. Open `code/02_numpy_analytics.ipynb`. You will load a small CSV into a NumPy array and answer analytics questions (per-column means, filtering rows by a condition, finding the row with the max value) **without using any `for` loops over the data**.
3. Write a short note: pick one operation you replaced with vectorization and explain why the NumPy version is faster.
4. **(Optional sidebar)** Use **Claude** or **Gemini** to explain one NumPy line you found tricky, then verify the explanation by running the code. Paste the prompt + your verification.
5. **Submit:** both completed notebooks (or Colab share links) + your note. Include a one-line **AI Use** disclosure.

*A2 is graded for correctness on the exercises (see syllabus).*

---

## Key terms
**ndarray**, **shape**, **dtype**, **axis**, **vectorization**, **broadcasting**, **slicing**, **boolean mask**, **reshape**, **aggregation**.
