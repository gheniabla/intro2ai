"""Build Week 3 sample-code notebooks. Run: python build_code.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from nbgen import build_notebook

HERE = os.path.dirname(__file__)
CODE = os.path.join(HERE, "code")
os.makedirs(CODE, exist_ok=True)

# ---------------------------------------------------------------- notebook 1
pandas_basics = [
    ("md", "# Week 3 · Notebook 1 — Pandas Basics\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "Pandas adds **labels** on top of NumPy: named columns and an index. "
           "Run each cell, then complete the **5 exercises** at the bottom (for A3)."),
    ("md", "## 0. Setup\nPandas is pre-installed in Colab; this line is for local runs."),
    ("code", "!pip -q install pandas"),
    ("code", "import pandas as pd\n"
             "import numpy as np\n"
             "print('pandas', pd.__version__)"),
    ("md", "## 1. Build a DataFrame & inspect it\n"
           "`head` / `info` / `describe` are the first things to run on any dataset."),
    ("code", "df = pd.DataFrame({\n"
             "    'name':  ['Ada', 'Alan', 'Grace', 'Linus', 'Katherine', 'Guido'],\n"
             "    'team':  ['A', 'B', 'A', 'B', 'A', 'B'],\n"
             "    'score': [91, 78, 88, 64, 95, 72],\n"
             "    'hours': [6.0, 3.5, 5.0, 2.0, 6.5, 3.0],\n"
             "})\n"
             "print(df.shape)\n"
             "df.head()"),
    ("code", "df.info()"),
    ("code", "df.describe()"),
    ("md", "## 2. Select columns and rows\n"
           "`.loc` selects by **label**, `.iloc` by **integer position**."),
    ("code", "print(df['score'].head())          # one column = a Series\n"
             "print(df[['name', 'score']].head())# several columns\n"
             "print(df.loc[0])                   # row with index label 0\n"
             "print(df.iloc[0:3, 0:2])           # first 3 rows, first 2 cols"),
    ("md", "## 3. Filter rows with boolean conditions"),
    ("code", "print(df[df['score'] >= 85])\n"
             "print(df[(df['score'] >= 85) & (df['hours'] < 6)])"),
    ("md", "## 4. Create new columns (vectorized, like NumPy)"),
    ("code", "df['passed'] = df['score'] >= 80\n"
             "df['per_hour'] = (df['score'] / df['hours']).round(2)\n"
             "df"),
    ("md", "## 5. Group & aggregate — 'per-category' questions"),
    ("code", "print(df.groupby('team')['score'].mean())\n"
             "print(df.groupby('passed')['score'].agg(['mean', 'size']))\n"
             "print(df['team'].value_counts())"),
    ("md", "## 6. Missing data\nReal data has holes (`NaN`). Find them, then decide what to do."),
    ("code", "d2 = df.copy()\n"
             "d2.loc[1, 'score'] = np.nan        # poke a hole\n"
             "print('missing per column:\\n', d2.isna().sum())\n"
             "print('filled with mean:\\n',\n"
             "      d2['score'].fillna(d2['score'].mean()).round(1).tolist())"),
    ("md", "---\n## Exercises (complete these for A3)\n"
           "1. Select just the `name` and `team` columns for the first 4 rows using `.iloc`.\n"
           "2. Filter to students on team `'A'` who studied more than 5 hours.\n"
           "3. Add a column `grade` that is `'P'` where `passed` is True else `'F'`.\n"
           "4. Use `groupby` to get the **mean hours** and **count** per team.\n"
           "5. Make a copy, set two `hours` values to `NaN`, then (a) count the missing and (b) fill them with the median hours."),
    ("code", "# Your solutions here\n"),
]
build_notebook(pandas_basics, os.path.join(CODE, "01_pandas_basics.ipynb"))

# ---------------------------------------------------------------- notebook 2
viz_az = [
    ("md", "# Week 3 · Notebook 2 — Visualizing the A–Z Handwritten Dataset\n"
           "**CSCI 250 · Fall 2026**\n\n"
           "The **A–Z Handwritten** dataset: each row is one character — the **first column "
           "is a label** (0–25 → A–Z) and the remaining **784 columns** are the pixels of a "
           "28×28 grayscale image. We load with Pandas, reshape with NumPy (Week 2!), and "
           "display with Matplotlib."),
    ("md", "## 0. Setup"),
    ("code", "!pip -q install pandas numpy matplotlib"),
    ("code", "import numpy as np\n"
             "import pandas as pd\n"
             "import matplotlib.pyplot as plt"),
    ("md", "## 1. Get the data\n"
           "The full `A_Z-HandwrittenData.csv` (from Canvas) is large. To keep this notebook "
           "fast and self-contained we **synthesize a small sample with intentionally uneven "
           "per-letter counts** with the same structure (1 label column + 784 pixel columns). "
           "The imbalance is on purpose — spotting it is the point of this lesson. To use the **real** file instead, "
           "upload it and set `USE_REAL = True`."),
    ("code", "USE_REAL = False   # set True after uploading A_Z-HandwrittenData.csv\n\n"
             "if USE_REAL:\n"
             "    df = pd.read_csv('A_Z-HandwrittenData.csv', header=None)\n"
             "else:\n"
             "    rng = np.random.default_rng(0)\n"
             "    rows = []\n"
             "    for label in range(26):                 # A..Z\n"
             "        n = rng.integers(20, 60)             # uneven counts on purpose\n"
             "        for _ in range(n):\n"
             "            img = np.zeros((28, 28))\n"
             "            # draw a faint blob + the letter index as brightness, so letters differ\n"
             "            cx, cy = rng.integers(8, 20, size=2)\n"
             "            img[cy-3:cy+3, cx-3:cx+3] = 80 + label * 6 + rng.integers(0, 40)\n"
             "            img += rng.integers(0, 25, size=(28, 28))\n"
             "            rows.append([label] + img.clip(0, 255).reshape(-1).tolist())\n"
             "    df = pd.DataFrame(rows)\n"
             "print('shape:', df.shape)   # (n_samples, 785)\n"
             "df.iloc[:3, :6]"),
    ("md", "## 2. Split labels and pixels"),
    ("code", "labels = df.iloc[:, 0].values.astype(int)   # 0..25\n"
             "pixels = df.iloc[:, 1:].values.astype(float) # (n, 784)\n"
             "print('labels:', labels.shape, ' pixels:', pixels.shape)\n"
             "letter = lambda i: chr(ord('A') + int(i))"),
    ("md", "## 3. Show ONE character\nReshape its 784 pixels back to 28×28 (Week 2 `reshape`)."),
    ("code", "img = pixels[0].reshape(28, 28)\n"
             "plt.figure(figsize=(3, 3))\n"
             "plt.imshow(img, cmap='gray')\n"
             "plt.title('label = ' + letter(labels[0]))\n"
             "plt.axis('off')\n"
             "plt.show()"),
    ("md", "## 4. A 3×3 grid of characters"),
    ("code", "fig, axes = plt.subplots(3, 3, figsize=(6, 6))\n"
             "for ax, idx in zip(axes.ravel(), range(9)):\n"
             "    ax.imshow(pixels[idx].reshape(28, 28), cmap='gray')\n"
             "    ax.set_title(letter(labels[idx]))\n"
             "    ax.axis('off')\n"
             "plt.tight_layout()\n"
             "plt.show()"),
    ("md", "## 5. Bar chart — how many examples per letter?\n"
           "Is the dataset **balanced**? This is the key question for A3."),
    ("code", "counts = pd.Series(labels).value_counts().sort_index()\n"
             "plt.figure(figsize=(10, 4))\n"
             "plt.bar([letter(i) for i in counts.index], counts.values, color='teal')\n"
             "plt.xlabel('letter'); plt.ylabel('number of examples')\n"
             "plt.title('Examples per letter')\n"
             "plt.show()"),
    ("md", "## 6. Histogram — distribution of average brightness per image"),
    ("code", "brightness = pixels.mean(axis=1)   # Week-2 axis op: mean per row\n"
             "plt.figure(figsize=(8, 4))\n"
             "plt.hist(brightness, bins=30, color='steelblue', edgecolor='white')\n"
             "plt.xlabel('average pixel brightness'); plt.ylabel('count of images')\n"
             "plt.title('How bright is a typical character?')\n"
             "plt.show()"),
    ("md", "## 7. Scatter — does brightness relate to the letter index?\n"
           "A quick scatter to look for any relationship between two numbers."),
    ("code", "plt.figure(figsize=(8, 4))\n"
             "plt.scatter(labels, brightness, alpha=0.3)\n"
             "plt.xlabel('label (0=A .. 25=Z)'); plt.ylabel('avg brightness')\n"
             "plt.title('Brightness vs letter')\n"
             "plt.show()"),
    ("md", "## 8. Your turn (for A3)\n"
           "1. Print the **mean brightness per letter** using a Pandas `groupby`.\n"
           "2. Which letter has the **most** examples and which the **fewest**?\n"
           "3. In 100–150 words: is this dataset balanced, and why would imbalance matter "
           "when we train a classifier in a few weeks?"),
    ("code", "# Hint for #1:\n"
             "# tmp = pd.DataFrame({'label': labels, 'brightness': brightness})\n"
             "# print(tmp.groupby('label')['brightness'].mean())\n"),
    ("md", "## 9. (Optional) Ask an LLM for another chart idea\n"
           "Use **Claude** or **Gemini** to suggest one more chart that would reveal something "
           "about this dataset, then build it. Never paste an API key — use Colab Secrets."),
    ("code", "# Optional sidebar — uncomment and add your key via Colab Secrets (userdata.get).\n"
             "# import os\n"
             "# import google.generativeai as genai\n"
             "# from google.colab import userdata\n"
             "# genai.configure(api_key=userdata.get('GEMINI_API_KEY'))\n"
             "# model = genai.GenerativeModel('gemini-2.5-flash')\n"
             "# resp = model.generate_content(\n"
             "#     'I have a handwritten-letters dataset (label + 784 pixel columns). '\n"
             "#     'Suggest one Matplotlib chart that reveals data quality issues.')\n"
             "# print(resp.text)\n"),
]
build_notebook(viz_az, os.path.join(CODE, "02_visualization_AZ.ipynb"))

print("wrote Week 3 notebooks to", CODE)
