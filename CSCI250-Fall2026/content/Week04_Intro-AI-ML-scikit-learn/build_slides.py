"""Build slides.pptx for Week 4. Run: python build_slides.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from slidegen import build_deck

slides = [
    {"type": "title", "title": "Week 4 — Intro to AI & ML with scikit-learn",
     "subtitle": "CSCI 250 — Introduction to Artificial Intelligence · Fall 2026"},

    {"type": "bullets", "title": "This Week", "bullets": [
        "Frame AI vs ML vs DL vs GenAI (and a little history)",
        "Walk the end-to-end ML workflow: data → train → evaluate",
        "Meet scikit-learn: estimators, fit/predict",
        "Split data safely with train_test_split",
        ("No graded assignment — but run both notebooks for A5 next week", 1)]},

    {"type": "section", "title": "AI vs ML vs DL vs GenAI"},
    {"type": "bullets", "title": "Nested, Not Interchangeable", "bullets": [
        "AI — broad goal: machines doing 'intelligent' tasks",
        ("ML — systems that learn patterns from data (our focus)", 1),
        ("DL — ML using multi-layer neural networks (Week 6)", 1),
        ("GenAI / LLMs — DL that generates text, images, code", 1),
        "Mental model:  AI ⊃ ML ⊃ DL ⊃ GenAI"]},
    {"type": "bullets", "title": "A 60-Second History", "bullets": [
        "1950s–60s — symbolic AI, Turing Test, the perceptron",
        "1980s — expert systems, then the first 'AI winter'",
        "1990s–2000s — statistical ML: trees, SVMs, scikit-learn era",
        "2012 — deep learning breaks out (AlexNet)",
        "2017 — the Transformer; 2022+ — GenAI goes mainstream"]},

    {"type": "two_col", "title": "Three Kinds of ML",
     "left_title": "This course's focus",
     "left": ["Supervised: learn from labeled (X, y)",
              "Regression → numeric y",
              "Classification → categorical y"],
     "right_title": "Also out there",
     "right": ["Unsupervised: find structure, no labels",
               "Reinforcement: learn from rewards"]},

    {"type": "section", "title": "The End-to-End ML Workflow"},
    {"type": "bullets", "title": "The Same Loop Every Time", "bullets": [
        "1. Get data — rows = samples, columns = features",
        "2. Explore & clean (your Week 2–3 skills)",
        "3. Split — hold out a test set you NEVER train on",
        "4. Features — choose/transform inputs (X)",
        "5. Train (fit) → 6. Evaluate → 7. Predict → 8. Iterate",
        ("Cardinal rule: never judge a model on its training data", 1)]},

    {"type": "section", "title": "scikit-learn Basics"},
    {"type": "code", "title": "The Universal Estimator API",
     "code": "from sklearn.linear_model import LinearRegression\n"
             "model = LinearRegression()      # 1. instantiate\n"
             "model.fit(X_train, y_train)     # 2. learn\n"
             "preds = model.predict(X_test)   # 3. predict\n"
             "model.score(X_test, y_test)     # 4. built-in metric",
     "caption": "Swap in any estimator (k-NN, trees, ...) — these 4 lines barely change"},
    {"type": "code", "title": "Load Data + Split Safely",
     "code": "from sklearn.datasets import load_iris\n"
             "from sklearn.model_selection import train_test_split\n\n"
             "X, y = load_iris(return_X_y=True)   # (150, 4),  (150,)\n"
             "X_train, X_test, y_train, y_test = train_test_split(\n"
             "    X, y, test_size=0.2, random_state=42, stratify=y)",
     "caption": "test_size holds out 20%; random_state = reproducible; stratify keeps class balance"},
    {"type": "code", "title": "A Full Pipeline in 8 Lines",
     "code": "from sklearn.neighbors import KNeighborsClassifier\n\n"
             "clf = KNeighborsClassifier(n_neighbors=3)\n"
             "clf.fit(X_train, y_train)\n"
             "print('test accuracy:', clf.score(X_test, y_test))",
     "caption": "Week 5 unpacks the models and the metrics behind that score"},

    {"type": "bullets", "title": "Where GenAI Fits", "bullets": [
        "Claude & Gemini are deep-learning models — still 'ML'",
        "They learned patterns from data, just at massive scale",
        "Same ideas: data, training, evaluation, generalization",
        ("This workflow is the foundation for the GenAI weeks", 1)]},

    {"type": "closing", "title": "This Week — To Do", "bullets": [
        "Read the scikit-learn 'Getting Started' guide",
        "Run 01_ml_workflow.ipynb (AI/ML framing + workflow)",
        "Run 02_sklearn_basics.ipynb (fit/predict + split)",
        "Post one takeaway in the Week 4 discussion",
        "No graded assignment — get ready for A5"]},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "slides.pptx")
    build_deck(slides, out)
    print("wrote", out)
