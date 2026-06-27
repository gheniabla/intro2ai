"""Build slides.pptx for Week 7. Run: python build_slides.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from slidegen import build_deck

slides = [
    {"type": "title", "title": "Week 7 — ML Review & Midterm",
     "subtitle": "CSCI 250 — Introduction to Artificial Intelligence · Fall 2026"},

    {"type": "bullets", "title": "This Week", "bullets": [
        "Consolidate Weeks 1–6 into one map of the ML workflow",
        "Work through the study guide + review/solutions notebook",
        "Take the practice midterm under exam conditions",
        "Sit the Midterm Exam — Sat Oct 11, 5:30–11:59 PM PT",
        ("Midterm is AI-restricted: no Claude/Gemini/Copilot during the exam", 1)]},

    {"type": "section", "title": "Midterm Logistics"},
    {"type": "bullets", "title": "Know Before You Start", "bullets": [
        "Date: Saturday, October 11, 2026 — 5:30 to 11:59 PM Pacific (Canvas)",
        "Coverage: Weeks 1–6 (reviewed in Week 7) — Python → NumPy → Pandas → ML → NN",
        "Format: multiple-choice, short-answer, read-the-code, brief concepts",
        ("AI-restricted — treat it like a proctored, closed-AI exam", 1),
        ("Practice midterm mirrors the format — take it AI-free first", 1)]},

    {"type": "section", "title": "The Big Map"},
    {"type": "code", "title": "How Weeks 1–6 Fit Together",
     "code": "raw data\n"
             "  -> load & clean        (NumPy / Pandas)\n"
             "  -> explore & visualize (Matplotlib)\n"
             "  -> split train / test\n"
             "  -> fit a model         (scikit-learn)\n"
             "  -> evaluate            (right metric!)\n"
             "  -> improve             (avoid over/underfitting)\n"
             "  -> (Week 6) neural network when needed",
     "caption": "Most exam questions are: 'which step is this?' or 'which tool/metric belongs here?'"},

    {"type": "two_col", "title": "Weeks 1–3: Python & Data",
     "left_title": "Python + NumPy",
     "left": ["types, comprehensions, f-strings", "keys via Colab Secrets (never hard-code)",
              "ndarray, vectorization, broadcasting", "axis=0 vs axis=1"],
     "right_title": "Pandas + Matplotlib",
     "right": ["DataFrame, .loc/.iloc, filtering", "groupby().agg(), missing values",
               "line / scatter / bar / histogram", "pick the right chart"]},
    {"type": "two_col", "title": "Weeks 4–5: ML & Supervised Learning",
     "left_title": "Intro & workflow",
     "left": ["AI ⊃ ML ⊃ DL ⊃ GenAI", "supervised / unsupervised / RL",
              "fit() then predict()", "train/test split → generalization"],
     "right_title": "Regression & classification",
     "right": ["linear reg → MAE / MSE / R²", "logistic, k-NN, decision trees",
               "accuracy / precision / recall / F1", "confusion matrix; over/underfit"]},
    {"type": "two_col", "title": "Week 6: Neural-Net Foundations",
     "left_title": "Core machinery",
     "left": ["perceptron: z = w·x + b", "layers: input / hidden / output",
              "loss: MSE / cross-entropy", "gradient descent: w ← w − lr·grad; backprop"],
     "right_title": "Activations & the LLM bridge",
     "right": ["ReLU (hidden), sigmoid (binary)", "softmax → class distribution",
               "CNNs (images) · Transformers (sequences)", "the foundation under LLMs"]},

    {"type": "section", "title": "High-Yield & Self-Check"},
    {"type": "bullets", "title": "Memorize These", "bullets": [
        "Overfitting = low train error, high test error; never tune on test",
        "Precision = TP/(TP+FP); Recall = TP/(TP+FN)",
        "Accuracy misleads on imbalanced data — use precision/recall/F1",
        "Regression → MAE/MSE/R²;  Classification → acc/prec/recall/F1 + confusion matrix",
        ("softmax = next-token step in an LLM; lr = gradient-descent step size", 1)]},
    {"type": "code", "title": "Can You Answer These? (no AI)",
     "code": "1. mutable or not: list, tuple, dict, str?\n"
             "2. shape of [[1,2,3]] + [[10],[20]]  (broadcasting)?\n"
             "3. what does df.groupby('city')['sales'].mean() return?\n"
             "4. train acc 0.99, test acc 0.62 -> what's wrong?\n"
             "5. which activation gives a multi-class distribution?",
     "caption": "Worked answers in 01_review_solutions.ipynb"},

    {"type": "closing", "title": "This Week — To Do", "bullets": [
        "Study the guide in document.md; target your weak spots",
        "Run 01_review_solutions.ipynb (worked solutions, Weeks 1–6)",
        "Take 02_practice_midterm.ipynb under exam conditions — no AI",
        "Sit the Midterm: Sat Oct 11, 5:30–11:59 PM PT (AI-restricted)"]},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "slides.pptx")
    build_deck(slides, out)
    print("wrote", out)
