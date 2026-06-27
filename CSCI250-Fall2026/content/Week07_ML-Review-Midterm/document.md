# Week 7 — ML Review & Midterm
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of October 5, 2026 · Online / Asynchronous*

---

## Learning objectives
By the end of this week you will be able to:
1. **Consolidate** everything from Weeks 1–6 into one coherent map of the ML workflow.
2. Use this **study guide** to self-assess and target your weak spots.
3. Practice under exam-like conditions with the **sample/practice midterm**.
4. Check your work with the **review/solutions notebook** (`code/01_review_solutions.ipynb`).
5. Sit the **Midterm Exam** confidently.

> **Time budget:** ~10 hours: review the study guide, run the review notebook, take the practice midterm, then sit the real exam.

---

## 0. Midterm logistics (read first)
- **Midterm Exam date:** **Saturday, October 11, 2026**, available **5:30 PM – 11:59 PM Pacific** on Canvas.
- **AI-restricted:** the midterm is a **closed-AI** exam. You may **not** use Claude, Gemini, Claude Code, Copilot, or any AI assistant during the exam. This is an honor-code expectation; treat it like a proctored test.
- **Coverage:** Weeks 1–6 (Python → NumPy → Pandas/Matplotlib → ML intro → regression/classification → neural-network foundations).
- **Format:** a mix of multiple-choice, short-answer, "read this code / what does it print," and a few "explain in 2–3 sentences" conceptual items.
- The **practice midterm** below mirrors the format. It is also AI-restricted — take it on your own first, *then* check answers.

---

## 1. The big map: how Weeks 1–6 fit together
Everything this half of the course has been building **one pipeline**:

```
raw data  →  load & clean (NumPy/Pandas)  →  explore & visualize (Matplotlib)
          →  split train/test  →  choose & fit a model (scikit-learn)
          →  evaluate with the right metric  →  improve (avoid over/underfitting)
          →  (Week 6) replace the model with a neural network when needed
```

Keep this picture in your head — most exam questions are "which step is this?" or "which tool/metric belongs here?"

---

## 2. Week-by-week study guide

### Week 1 — Python & the AI dev environment
- **Core types:** `int/float/bool/str`, `list` (mutable), `tuple` (immutable), `dict` (key→value), `set` (unique).
- **Must know:** functions + type hints, list comprehensions, f-strings, `import`/`pip`.
- **Environment:** Colab, Git/GitHub, API keys via **Colab Secrets / env vars** (never hard-code), three model sources (Claude, Gemini, Ollama).
- *Likely Q:* what does a comprehension print; mutable vs immutable; where do API keys go.

### Week 2 — NumPy & data processing
- **ndarray**, `dtype`, `shape`; **vectorization** (no Python loops); **broadcasting**; indexing/slicing; boolean masks; axis-wise reductions (`arr.mean(axis=0)`).
- *Likely Q:* result `shape` after broadcasting; vectorized vs loop; `axis=0` vs `axis=1`.

### Week 3 — Pandas & Matplotlib
- **DataFrame / Series**; selection (`.loc`, `.iloc`); filtering; `groupby().agg()`; handling missing values (`dropna`, `fillna`).
- **Matplotlib:** line / scatter / bar / histogram; labels, titles, legend; when to use which plot.
- *Likely Q:* what a `groupby` returns; pick the right chart for a question.

### Week 4 — Intro to AI/ML & scikit-learn
- **AI ⊃ ML ⊃ DL**; **GenAI** as a subset of DL. Supervised vs unsupervised vs reinforcement.
- **End-to-end workflow** (the map above). scikit-learn API: `model.fit(X, y)` then `model.predict(X)`; **train/test split** and *why* (estimate generalization).
- *Likely Q:* define AI vs ML vs DL vs GenAI; why we hold out a test set.

### Week 5 — Regression & Classification (supervised)
- **Regression:** linear regression; metric **MAE / MSE / R²**.
- **Classification:** logistic regression, **k-NN**, **decision trees**; metrics **accuracy, precision, recall, F1, confusion matrix**.
- **Overfitting vs underfitting**; the role of train vs test error; precision vs recall trade-off.
- *Likely Q:* read a confusion matrix → compute accuracy/precision/recall; classification vs regression; spot overfitting.

### Week 6 — Neural network foundations
- **Perceptron:** `z = w·x + b`, then an activation. **Layers** (input/hidden/output); **deep** = many hidden layers.
- **Activations:** **ReLU** (hidden), **sigmoid** (binary prob), **softmax** (multi-class distribution). Nonlinearity is what makes depth useful.
- **Loss:** MSE (regression), **cross-entropy** (classification). **Gradient descent**: `w ← w − lr·grad`. **Backprop** = chain rule, one backward pass; frameworks autograd it.
- **Tour:** CNNs (image filters/convolution), sequence models → **Transformer/attention** = the architecture under LLMs.
- *Likely Q:* match activation to use; what backprop does; why nonlinearity matters; the LLM bridge.

---

## 3. High-yield concepts (memorize these)
- **Train/test split** exists to estimate **generalization**; never tune on the test set.
- **Overfitting** = low train error, high test error (model memorized noise). **Underfitting** = high error everywhere.
- **Precision** = TP/(TP+FP) ("of those I flagged positive, how many were right"). **Recall** = TP/(TP+FN) ("of the actual positives, how many did I catch").
- **Accuracy** misleads on **imbalanced** data — use precision/recall/F1.
- **Regression → MAE/MSE/R²; Classification → accuracy/precision/recall/F1 + confusion matrix.**
- **Softmax** turns scores into a probability distribution — the same step an LLM uses for the next token.
- **Gradient descent** minimizes the **loss**; the **learning rate** controls step size.

---

## 4. Quick self-check (answers in the review notebook)
1. mutable or immutable: `list`, `tuple`, `dict`, `str`?
2. `np.array([[1,2,3]]) + np.array([[10],[20]])` → what shape?
3. What does `df.groupby('city')['sales'].mean()` return?
4. Name the four-quadrant table used to evaluate a classifier.
5. Train accuracy 0.99, test accuracy 0.62 — what is wrong?
6. Which activation gives a multi-class probability distribution?
7. In `w ← w − lr·grad`, what does `lr` control?

---

## 5. Reading & videos
- Re-skim your own Week 1–6 documents and notebooks (the best review material).
- *Machine Learning Systems* (mlsysbook.ai) — the ML-workflow and evaluation chapters.
- Optional refresher: StatQuest "Confusion Matrix" and "Gradient Descent, Step-by-Step" (YouTube).

---

## 6. Lab / assignment — **Midterm Exam (Oct 11)**
There is no separate lab this week. Your deliverable is the **Midterm Exam**:
1. Work through this **study guide** and run `code/01_review_solutions.ipynb` (worked solutions across Weeks 1–6).
2. Take the **practice midterm** (`code/02_practice_midterm.ipynb`) under exam conditions — **no AI** — then check answers in the solutions notebook.
3. Sit the **real Midterm** on **Saturday, Oct 11, 5:30–11:59 PM PT** on Canvas. **AI tools are not permitted** during the exam.

*The midterm is graded; the practice materials are not, but they are the best predictor of how you'll do.*

---

## Key terms
**ML workflow**, **train/test split**, **generalization**, **overfitting / underfitting**, **vectorization / broadcasting**, **DataFrame / groupby**, **supervised / unsupervised**, **regression vs classification**, **MAE / R²**, **accuracy / precision / recall / F1**, **confusion matrix**, **perceptron / layer / activation**, **ReLU / sigmoid / softmax**, **loss / cross-entropy**, **gradient descent / backprop**, **AI-restricted exam**.
