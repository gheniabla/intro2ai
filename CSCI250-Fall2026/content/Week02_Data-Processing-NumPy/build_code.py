"""Build Week 2 sample-code notebooks. Run: python build_code.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from nbgen import build_notebook

HERE = os.path.dirname(__file__)
CODE = os.path.join(HERE, "code")
os.makedirs(CODE, exist_ok=True)

# ---------------------------------------------------------------- notebook 1
numpy_basics = [
    ("md", "# Week 2 · Notebook 1 — NumPy Basics\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "NumPy is the array library every ML tool is built on. Run each cell, "
           "then complete the **6 exercises** at the bottom (for A2)."),
    ("md", "## 0. Setup\nNumPy is pre-installed in Colab; this line is here for local runs."),
    ("code", "!pip -q install numpy"),
    ("code", "import numpy as np\n"
             "print('numpy', np.__version__)"),
    ("md", "## 1. Creating arrays"),
    ("code", "a = np.array([[1, 2, 3], [4, 5, 6]])\n"
             "print(a)\n"
             "print('zeros:\\n', np.zeros((2, 3)))\n"
             "print('arange:', np.arange(0, 10, 2))\n"
             "print('linspace:', np.linspace(0, 1, 5))"),
    ("md", "## 2. Inspecting an array\n"
           "Every array has `shape`, `ndim`, `dtype`, `size` — check these constantly."),
    ("code", "print('shape', a.shape)\n"
             "print('ndim ', a.ndim)\n"
             "print('dtype', a.dtype)\n"
             "print('size ', a.size)"),
    ("md", "## 3. Reshaping\nThe same data, viewed in a new shape. `-1` means 'infer this dimension'."),
    ("code", "v = np.arange(12)\n"
             "print(v.reshape(3, 4))\n"
             "print('flatten back:', v.reshape(3, 4).reshape(-1))"),
    ("md", "## 4. Vectorization — and why it is faster\n"
           "Element-wise math runs in C. Use `%timeit` to *see* the speedup."),
    ("code", "N = 1_000_000\n"
             "py = %timeit -o -q [x * 2 for x in range(N)]\n"
             "nm = %timeit -o -q np.arange(N) * 2\n"
             "print(f'python loop: {py.best:.4f}s   numpy: {nm.best:.6f}s')"),
    ("code", "a = np.array([1.0, 4.0, 9.0])\n"
             "print('sqrt :', np.sqrt(a))\n"
             "print('>3   :', a > 3)\n"
             "print('*10+1:', a * 10 + 1)"),
    ("md", "## 5. Broadcasting\nCombine different shapes with no loop — e.g. add a row to every row."),
    ("code", "matrix = np.ones((3, 3))\n"
             "row = np.array([1, 2, 3])\n"
             "print(matrix + row)         # row added to each row\n"
             "prices = np.array([10., 20., 30.])\n"
             "print('with tax:', prices * 1.08)"),
    ("md", "## 6. Indexing, slicing & boolean masks"),
    ("code", "m = np.arange(12).reshape(3, 4)\n"
             "print('m[1,2]   =', m[1, 2])\n"
             "print('col 0    =', m[:, 0])\n"
             "print('subblock =\\n', m[0:2, 1:3])\n\n"
             "data = np.array([3, -1, 7, -5, 9])\n"
             "print('positives:', data[data > 0])\n"
             "data[data < 0] = 0\n"
             "print('clipped  :', data)"),
    ("md", "## 7. Axis operations\n"
           "`axis=0` collapses rows (per-column result); `axis=1` collapses columns (per-row)."),
    ("code", "scores = np.array([[90, 80, 70],\n"
             "                   [60, 75, 95]])\n"
             "print('per subject (axis=0):', scores.mean(axis=0))\n"
             "print('per student (axis=1):', scores.mean(axis=1))\n"
             "print('best subject idx    :', scores.argmax(axis=1))"),
    ("md", "---\n## Exercises (complete these for A2)\n"
           "1. Create a 4×4 array of the numbers 1..16 (use `arange` + `reshape`).\n"
           "2. From that array, slice out the center 2×2 block.\n"
           "3. Make `temps_c = np.array([0, 20, 37, 100])` and convert to Fahrenheit **vectorized** (no loop).\n"
           "4. Given `x = np.arange(-5, 6)`, use a boolean mask to keep only values whose absolute value is ≥ 3.\n"
           "5. Standardize the columns of `np.random.default_rng(1).random((6, 3))` (subtract column mean, divide by column std) using broadcasting.\n"
           "6. For a 5×3 array of random integers, print the column means, the row maxima, and the index of the largest value in each row."),
    ("code", "# Your solutions here\n"),
]
build_notebook(numpy_basics, os.path.join(CODE, "01_numpy_basics.ipynb"))

# ---------------------------------------------------------------- notebook 2
numpy_analytics = [
    ("md", "# Week 2 · Notebook 2 — NumPy Analytics on a Dataset\n"
           "**CSCI 250 · Fall 2026**\n\n"
           "Load a small CSV into a NumPy array and answer analytics questions "
           "**without any `for` loops over the data**. This is the shape ML expects: "
           "rows = samples, columns = features."),
    ("md", "## 0. Setup"),
    ("code", "!pip -q install numpy"),
    ("code", "import numpy as np"),
    ("md", "## 1. Make a tiny dataset (so the notebook is self-contained)\n"
           "Columns: **hours_studied, prior_gpa, attendance, exam_score**."),
    ("code", "csv_text = '''hours_studied,prior_gpa,attendance,exam_score\n"
             "2.0,2.8,0.60,55\n"
             "4.5,3.1,0.85,72\n"
             "1.0,2.5,0.40,48\n"
             "6.0,3.6,0.95,88\n"
             "3.0,3.0,0.75,65\n"
             "5.5,3.8,0.90,91\n"
             "0.5,2.2,0.30,40\n"
             "4.0,3.3,0.80,78'''\n"
             "with open('students.csv', 'w') as f:\n"
             "    f.write(csv_text)\n"
             "print('wrote students.csv')"),
    ("md", "## 2. Load with `np.genfromtxt`\n"
           "We skip the header row and read the four numeric columns into a 2-D array."),
    ("code", "data = np.genfromtxt('students.csv', delimiter=',', skip_header=1)\n"
             "cols = ['hours_studied', 'prior_gpa', 'attendance', 'exam_score']\n"
             "print('shape:', data.shape)\n"
             "print(data)"),
    ("md", "## 3. Per-column means (axis aggregation)"),
    ("code", "means = data.mean(axis=0)\n"
             "for name, mu in zip(cols, means):\n"
             "    print(f'{name:14s} mean = {mu:.3f}')"),
    ("md", "## 4. Filter rows by a condition (boolean mask)\n"
           "Which students scored above the class average exam score? No loops."),
    ("code", "exam = data[:, 3]\n"
             "above = data[exam > exam.mean()]\n"
             "print('rows above average exam score:')\n"
             "print(above)"),
    ("md", "## 5. Find the top student (argmax)"),
    ("code", "best_idx = data[:, 3].argmax()\n"
             "print('top student row index:', best_idx)\n"
             "print('their record         :', data[best_idx])"),
    ("md", "## 6. Standardize the features (broadcasting)\n"
           "Subtract each column's mean and divide by its std — what models usually want."),
    ("code", "X = data[:, :3]                      # feature columns\n"
             "X_std = (X - X.mean(axis=0)) / X.std(axis=0)\n"
             "print('standardized feature means (~0):', X_std.mean(axis=0).round(3))\n"
             "print('standardized feature stds  (~1):', X_std.std(axis=0).round(3))"),
    ("md", "## 7. Correlation: does studying track the exam score?\n"
           "A quick `np.corrcoef` between hours_studied and exam_score."),
    ("code", "r = np.corrcoef(data[:, 0], data[:, 3])[0, 1]\n"
             "print(f'corr(hours_studied, exam_score) = {r:.3f}')"),
    ("md", "## 8. Your analytics (for A2)\n"
           "Answer **without loops**:\n"
           "1. What is the highest and lowest `prior_gpa`? (use `max` / `min`)\n"
           "2. How many students had attendance ≥ 0.80? (mask + `sum`)\n"
           "3. Which feature is most correlated with `exam_score`?\n"
           "4. Add a new column = `hours_studied * attendance` using broadcasting and `np.column_stack`."),
    ("code", "# Your analytics here\n"),
    ("md", "## 9. (Optional) Ask an LLM to explain a line\n"
           "Use **Claude** or **Gemini** to explain one NumPy line you found tricky, then "
           "**verify** by running it. Never paste an API key — use Colab Secrets."),
    ("code", "# Optional sidebar — uncomment and add your key via Colab Secrets (userdata.get).\n"
             "# import os, anthropic\n"
             "# from google.colab import userdata\n"
             "# os.environ['ANTHROPIC_API_KEY'] = userdata.get('ANTHROPIC_API_KEY')\n"
             "# client = anthropic.Anthropic()\n"
             "# msg = client.messages.create(\n"
             "#     model='claude-sonnet-4-6', max_tokens=300,\n"
             "#     messages=[{'role': 'user',\n"
             "#                'content': 'Explain what (X - X.mean(axis=0)) / X.std(axis=0) does in NumPy.'}])\n"
             "# print(msg.content[0].text)\n"),
]
build_notebook(numpy_analytics, os.path.join(CODE, "02_numpy_analytics.ipynb"))

print("wrote Week 2 notebooks to", CODE)
