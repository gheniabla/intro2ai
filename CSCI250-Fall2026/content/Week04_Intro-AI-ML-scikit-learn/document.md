# Week 4 — Introduction to AI & ML with scikit-learn
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of September 14, 2026 · Online / Asynchronous*

---

## Learning objectives
By the end of this week you will be able to:
1. Distinguish **AI**, **Machine Learning (ML)**, **Deep Learning (DL)**, and **Generative AI (GenAI)**, and place them in historical context.
2. Describe the **end-to-end ML workflow**: data → features → train → evaluate → predict.
3. Explain the difference between **supervised**, **unsupervised**, and **reinforcement** learning.
4. Use **scikit-learn** estimators with the universal **`fit` / `predict`** API.
5. Split data correctly with **`train_test_split`** and avoid the classic mistake of evaluating on training data.

> **Time budget:** ~10 hours this week (lecture + slides + videos + notebooks + **Lab A4**). Run both notebooks; they're also the launchpad for A5 next week.

---

## 1. AI vs ML vs DL vs GenAI
These terms are nested, not interchangeable.

- **Artificial Intelligence (AI)** — the broad goal of building systems that perform tasks we associate with human intelligence (reasoning, perception, language). Includes everything below, plus older rule-based "expert systems."
- **Machine Learning (ML)** — a subset of AI where systems **learn patterns from data** instead of being explicitly programmed with rules. This is our focus for Weeks 4–7.
- **Deep Learning (DL)** — a subset of ML using **multi-layer neural networks**. Powers modern vision and language. We dive in during Week 6.
- **Generative AI (GenAI)** — DL models (especially **Large Language Models**) that **generate** new content: text, images, code. The back half of the course.

```
AI  ⊃  ML  ⊃  DL  ⊃  GenAI / LLMs
```

### A 60-second history
- **1950s–60s:** Symbolic AI, the Turing Test, the perceptron.
- **1980s:** Expert systems; first "AI winter" follows when they don't scale.
- **1990s–2000s:** Statistical ML rises — decision trees, SVMs, **scikit-learn**-style methods.
- **2012:** Deep learning breaks out (AlexNet wins ImageNet).
- **2017:** The **Transformer** architecture ("Attention Is All You Need").
- **2022–present:** GenAI goes mainstream — ChatGPT, Claude, Gemini, image generators.

---

## 2. Three kinds of machine learning
- **Supervised learning** — learn from **labeled** examples `(X, y)`. Predict a label for new `X`. *Regression* (numeric `y`) and *classification* (categorical `y`). **Weeks 4–5.**
- **Unsupervised learning** — no labels; find structure (clustering, dimensionality reduction).
- **Reinforcement learning** — an agent learns by trial and error via rewards.

Most of this course's classic-ML portion is **supervised**.

---

## 3. The end-to-end ML workflow
Every supervised ML project follows the same loop:

1. **Get data** — a table of rows (samples) and columns (features), plus a target.
2. **Explore & clean** — handle missing values, understand distributions (Weeks 2–3 skills!).
3. **Split** — hold out a **test set** you never train on.
4. **Features** — choose/transform the input columns (`X`).
5. **Train (`fit`)** — the estimator learns parameters from `X_train, y_train`.
6. **Evaluate** — measure performance on the **held-out test set**.
7. **Predict (`predict`)** — use the trained model on new data.
8. **Iterate** — try different features/models, repeat.

> **The cardinal rule:** never judge a model on data it was trained on. That tells you how well it *memorized*, not how well it *generalizes*.

---

## 4. scikit-learn basics
**scikit-learn** (`sklearn`) is the standard Python library for classic ML. Its genius is a **uniform API**: nearly every model is an *estimator* with the same methods.

### 4.1 The estimator API
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()      # 1. instantiate
model.fit(X_train, y_train)     # 2. learn from data
preds = model.predict(X_test)   # 3. predict on new data
score = model.score(X_test, y_test)  # 4. built-in metric
```
Swap `LinearRegression` for `KNeighborsClassifier`, `DecisionTreeClassifier`, etc. — **the four lines barely change.** That consistency is why sklearn is the teaching standard.

### 4.2 Bundled datasets
sklearn ships toy datasets so you can practice with zero setup:
```python
from sklearn.datasets import load_iris
data = load_iris()
X, y = data.data, data.target   # X: (150, 4) features, y: (150,) labels
print(data.feature_names)       # the 4 flower measurements
print(data.target_names)        # ['setosa' 'versicolor' 'virginica']
```
Others we use: `load_diabetes` (regression), `make_classification` (synthetic).

### 4.3 `train_test_split`
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
```
- `test_size=0.2` — hold out 20% for testing.
- `random_state=42` — reproducible split (any fixed int works).
- `stratify=y` — keep class proportions balanced in both splits (for classification).

### 4.4 A complete tiny example
```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

clf = KNeighborsClassifier(n_neighbors=3)
clf.fit(X_train, y_train)
print("test accuracy:", clf.score(X_test, y_test))
```
That is a full supervised-ML pipeline in 8 lines. Week 5 unpacks the models and metrics.

---

## 5. Where GenAI fits
The LLMs you called in Week 1 (Claude, Gemini) are **deep learning** models trained on enormous text corpora. They are still "machine learning" — they learned patterns from data — just at a vastly larger scale and with a generative objective. Understanding the classic workflow here makes the GenAI weeks click: *data, training, evaluation, and generalization are the same ideas, scaled up.*

---

## 6. Reading & videos
- *scikit-learn* "Getting Started" guide (scikit-learn.org) — required skim.
- *Machine Learning Systems* (mlsysbook.ai) — the "ML workflow" chapter.
- Video: "But what is machine learning?" (linked in Canvas).
- Google ML Crash Course — "Framing" and "First Steps with TF/sklearn" intro (linked in Canvas).

---

## 7. Lab — Assignment A4 (6 pts · due Sunday Sep 20, 11:59 PM PT)
**Goal:** run a complete supervised-ML workflow in scikit-learn — **load → split → fit → evaluate → predict** — and internalize the cardinal rule: never judge a model on data it trained on. Full spec and rubric: `assignments/A4.md`.

This week's two notebooks map directly to the A4 tasks:
1. **Workflow (`code/01_ml_workflow.ipynb`).** Run all sections end-to-end, then **explain the cardinal rule in your own words** (Section 6): why is the score on the *training* set misleading? Reproduce the demonstration that train accuracy looks better than test accuracy.
2. **The estimator API (`code/02_sklearn_basics.ipynb`).** Complete the **"Try it yourself"** section: load `iris` with `train_test_split` (`test_size=0.2`, `random_state=42`, `stratify=y`), fit a `KNeighborsClassifier`, and report **test accuracy** via `model.score(...)`.
3. **Swap the model.** Re-run the same four-line pipeline with a different estimator (e.g., `DecisionTreeClassifier`); report both test accuracies and note that the API barely changed.
4. **Why split?** In 2–3 sentences explain what `train_test_split` does and what `random_state` and `stratify` are for.
5. **Stretch:** Switch to regression — load `diabetes`, fit `LinearRegression`, report `.score()` (R²); one sentence on how evaluating regression differs from classification.

**Submit on Canvas:** both completed notebooks (or Colab links with outputs), your cardinal-rule explanation, the two accuracies, the split explanation, the stretch result, and a one-line **AI-Use** note. Correctness-graded — you may revise once after feedback.

---

## Key terms
**AI**, **machine learning**, **deep learning**, **generative AI**, **supervised / unsupervised / reinforcement learning**, **estimator**, **`fit` / `predict`**, **feature**, **label / target**, **train/test split**, **generalization**, **scikit-learn**.
