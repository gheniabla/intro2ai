"""Build slides.pptx for Week 3. Run: python build_slides.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from slidegen import build_deck

slides = [
    {"type": "title", "title": "Week 3 — Data Visualization: Pandas & Matplotlib",
     "subtitle": "CSCI 250 — Introduction to Artificial Intelligence · Fall 2026"},

    {"type": "bullets", "title": "This Week", "bullets": [
        "Pandas DataFrames & Series — labeled tabular data",
        "Select & filter: .loc, .iloc, boolean conditions",
        "groupby — answer 'per-category' questions",
        "Handle missing data (isna / dropna / fillna)",
        "Matplotlib: line, bar, scatter, histogram",
        "See the A–Z handwritten dataset as images",
        ("Mon Sep 7 is Labor Day — A3 still due Sunday", 1)]},

    {"type": "section", "title": "Pandas: Labeled Data"},
    {"type": "bullets", "title": "DataFrame = Table on Top of NumPy", "bullets": [
        "DataFrame = rows + named columns; a column is a Series",
        "Still NumPy underneath — Week 2 skills carry over",
        "head() — peek at the first rows",
        "info() — dtypes + non-null counts",
        "describe() — summary stats per numeric column"]},
    {"type": "code", "title": "Load & Inspect",
     "code": "import pandas as pd\n"
             "df = pd.read_csv('data.csv')\n"
             "df.head()        # first rows\n"
             "df.shape         # (rows, columns)\n"
             "df.info()        # dtypes + non-null counts\n"
             "df.describe()    # mean/std/min/max per column",
     "caption": "head / info / describe — run these first on ANY dataset"},

    {"type": "section", "title": "Select, Filter, Group"},
    {"type": "code", "title": "Selecting & Filtering",
     "code": "df.loc[:, 'score']            # by label\n"
             "df.iloc[0:3, 0:2]            # by position\n\n"
             "df[df['score'] >= 85]                        # filter\n"
             "df[(df['score'] >= 85) & (df['hours'] < 6)]  # & / |\n\n"
             "df['passed'] = df['score'] >= 80   # new column",
     "caption": ".loc = labels, .iloc = positions, [] = boolean filter"},
    {"type": "code", "title": "Group & Missing Data",
     "code": "df.groupby('team')['score'].mean()   # per-category\n"
             "df['team'].value_counts()            # rows per group\n\n"
             "df.isna().sum()                      # missing per column\n"
             "df.dropna(subset=['score'])          # drop missing\n"
             "df['score'].fillna(df['score'].mean())  # or fill",
     "caption": "Dropping loses data; filling invents it — say what you did"},

    {"type": "section", "title": "Matplotlib"},
    {"type": "two_col", "title": "Pick the Chart by the Question",
     "left_title": "Relationship / spread",
     "left": ["scatter — two numbers related?", "histogram — distribution of one"],
     "right_title": "Compare / trend",
     "right": ["bar — across categories", "line — change over an ordered axis"]},
    {"type": "code", "title": "A–Z Handwritten Digits",
     "code": "df = pd.read_csv('A_Z-HandwrittenData.csv', header=None)\n"
             "labels = df.iloc[:, 0].values     # 0..25 -> A..Z\n"
             "pixels = df.iloc[:, 1:].values    # (n, 784)\n\n"
             "img = pixels[0].reshape(28, 28)   # Week-2 reshape!\n"
             "plt.imshow(img, cmap='gray')\n"
             "plt.title(chr(ord('A') + labels[0])); plt.show()",
     "caption": "Pandas loads, NumPy reshapes, Matplotlib shows the letter"},

    {"type": "closing", "title": "This Week — To Do", "bullets": [
        "Read the document + 10-minutes-to-pandas",
        "Run 01_pandas_basics.ipynb (5 exercises)",
        "Run 02_visualization_AZ.ipynb — grid, bar chart, histogram",
        "Write the 'is the dataset balanced?' note",
        "Submit Lab A3 by Sunday 11:59 PM PT"]},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "slides.pptx")
    build_deck(slides, out)
    print("wrote", out)
