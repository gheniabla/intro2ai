"""Build slides.pptx for Week 2. Run: python build_slides.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from slidegen import build_deck

slides = [
    {"type": "title", "title": "Week 2 — Data Processing & Analytics with NumPy",
     "subtitle": "CSCI 250 — Introduction to Artificial Intelligence · Fall 2026"},

    {"type": "bullets", "title": "This Week", "bullets": [
        "Why NumPy is the foundation of every ML library",
        "Create, reshape & inspect N-dimensional arrays",
        "Vectorization — replace slow Python loops",
        "Broadcasting — combine arrays of different shapes",
        "Indexing, slicing & boolean masks",
        "Axis operations & simple statistics"]},

    {"type": "section", "title": "Why NumPy?"},
    {"type": "bullets", "title": "Arrays Power All of AI", "bullets": [
        "Pandas, scikit-learn, PyTorch all build on the ndarray",
        "Speed: array math runs in C — 10–100× faster than loops",
        "Vectorization: write 'a + b', not an element loop",
        "One dtype, contiguous memory — what GPUs/ML expect",
        ("Data shape: rows = samples, columns = features", 1)]},
    {"type": "code", "title": "Creating & Inspecting Arrays",
     "code": "import numpy as np\n"
             "a = np.arange(12)          # [0 1 ... 11]\n"
             "m = a.reshape(3, 4)        # view as 3x4, no copy\n"
             "print(m.shape, m.ndim, m.dtype, m.size)\n"
             "np.zeros((2, 3)); np.ones(4); np.linspace(0, 1, 5)",
     "caption": "shape / ndim / dtype / size — check these constantly"},

    {"type": "section", "title": "Vectorization & Broadcasting"},
    {"type": "two_col", "title": "Stop Writing Loops",
     "left_title": "Slow: Python loop",
     "left": ["out = []", "for x in range(N):", ("out.append(x * 2)", 1)],
     "right_title": "Fast: vectorized",
     "right": ["out = np.arange(N) * 2", "runs in C", "shorter AND faster"]},
    {"type": "code", "title": "Broadcasting",
     "code": "prices = np.array([10., 20., 30.])\n"
             "prices * 1.08            # +8% tax to all\n\n"
             "X = np.random.default_rng(0).random((100, 4))\n"
             "X_std = (X - X.mean(axis=0)) / X.std(axis=0)\n"
             "# subtract/divide per-column mean & std -> standardize",
     "caption": "Shapes align from the right; a dim of 1 stretches"},

    {"type": "section", "title": "Selecting & Summarizing"},
    {"type": "code", "title": "Indexing, Slicing & Masks",
     "code": "m = np.arange(12).reshape(3, 4)\n"
             "m[1, 2]          # row 1, col 2\n"
             "m[:, 0]          # whole first column\n"
             "m[0:2, 1:3]      # sub-block\n\n"
             "data = np.array([3, -1, 7, -5, 9])\n"
             "data[data > 0]      # [3 7 9] keep positives\n"
             "data[data < 0] = 0  # clip negatives to 0",
     "caption": "Boolean masks are how you filter a dataset"},
    {"type": "code", "title": "Axis Operations",
     "code": "scores = np.array([[90, 80, 70],\n"
             "                   [60, 75, 95]])\n"
             "scores.sum(axis=0)   # [150 155 165] per COLUMN\n"
             "scores.sum(axis=1)   # [240 230]     per ROW\n"
             "scores.mean(axis=0)  # average per subject\n"
             "scores.argmax(axis=1)# best subject per student",
     "caption": "axis=0 collapses rows; axis=1 collapses columns"},

    {"type": "closing", "title": "This Week — To Do", "bullets": [
        "Read the document + skim NumPy Beginner's Guide",
        "Run 01_numpy_basics.ipynb (6 exercises)",
        "Run 02_numpy_analytics.ipynb — analyze a CSV, no loops",
        "Write your vectorization note",
        "Submit Lab A2 by Sunday 11:59 PM PT"]},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "slides.pptx")
    build_deck(slides, out)
    print("wrote", out)
