# Week 5 — Regression & Classification (Supervised Learning)
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of September 21, 2026 · Online / Asynchronous*

---

## Learning objectives
By the end of this week you will be able to:
1. Build **regression** models (linear regression) and read their error with **MAE** and **RMSE**.
2. Build **classification** models (**logistic regression**, **k-NN**, **decision trees**).
3. Evaluate classifiers with **accuracy, precision, recall, F1**, and a **confusion matrix** — and know when accuracy lies.
4. Use a **train / validation / test** split and explain **overfitting** vs **underfitting**.
5. Apply **regularization** and basic hyperparameter tuning to improve generalization.
6. Complete **Assignment A5** end-to-end on a real dataset.

> **Time budget:** ~10 hours this week (lecture + slides + videos + notebooks + **Lab A5**).

---

## 1. Regression: predicting a number
**Regression** predicts a continuous target `y` (a price, a temperature, disease progression).

### 1.1 Linear regression
Fits a line/hyperplane: `ŷ = w·x + b`. sklearn learns the weights `w` and bias `b` for you.
```python
from sklearn.linear_model import LinearRegression
reg = LinearRegression().fit(X_train, y_train)
preds = reg.predict(X_test)
```

### 1.2 Regression metrics
You cannot use "accuracy" for numbers. Instead measure **how far off** predictions are:
- **MAE** (Mean Absolute Error) — average absolute miss. Same units as `y`, easy to explain.
- **RMSE** (Root Mean Squared Error) — squares errors first, so it **punishes big misses harder**. Same units as `y`.
- **R²** — fraction of variance explained (1.0 = perfect, 0 = no better than predicting the mean).
```python
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
mae  = mean_absolute_error(y_test, preds)
rmse = root_mean_squared_error(y_test, preds)
r2   = r2_score(y_test, preds)
```
*Rule of thumb:* RMSE ≥ MAE always; a big gap means a few large errors are dominating.

---

## 2. Classification: predicting a category
**Classification** predicts a discrete label (spam/not-spam, which species, which digit).

### 2.1 Three workhorse classifiers
- **Logistic regression** — despite the name, a **classifier**. Outputs class probabilities; great linear baseline.
- **k-Nearest Neighbors (k-NN)** — label a point by majority vote of its `k` closest neighbors. No "training," just memorize-then-vote. Sensitive to feature scale.
- **Decision tree** — a flowchart of yes/no questions. Easy to interpret; **overfits** if grown too deep.

All three share the same `fit`/`predict` API from Week 4.
```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
```

---

## 3. Classification metrics — when accuracy lies
**Accuracy** = fraction correct. Fine when classes are balanced; **misleading when they are not.** If 99% of email is not-spam, a model that always says "not-spam" is 99% accurate and useless.

Better tools, built from the **confusion matrix** (TP, FP, TN, FN):
- **Precision** = TP / (TP + FP) — *of the items I flagged positive, how many were actually positive?* (cost of false alarms).
- **Recall** = TP / (TP + FN) — *of the actual positives, how many did I catch?* (cost of misses).
- **F1** = harmonic mean of precision & recall — one number balancing both.
```python
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report)
print(classification_report(y_test, preds))
```
A **confusion matrix** shows exactly *which* classes get confused for which — far more informative than a single number.

---

## 4. Train / validation / test, and overfitting
### 4.1 Three splits
- **Train** — fit the model.
- **Validation** — tune choices (which model? which hyperparameters?) without touching test.
- **Test** — touched **once**, at the very end, for an honest final score.

When data is small, use **cross-validation** instead of a fixed validation set:
```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X_train, y_train, cv=5)
print(scores.mean(), "±", scores.std())
```

### 4.2 Overfitting vs underfitting
- **Overfitting** — model memorizes training noise; **great on train, poor on test.** (e.g. a very deep tree.)
- **Underfitting** — model too simple to capture the pattern; poor on both. (e.g. a line for a curve.)
- The tell-tale sign of overfitting: a **large gap** between train and test scores.

### 4.3 Regularization
**Regularization** penalizes model complexity to fight overfitting. Note the two parameters point in **opposite directions**:
- `LogisticRegression` uses **`C`** — the *inverse* strength, so **smaller `C` = stronger regularization**.
- `Ridge` / `Lasso` use **`alpha`** — the direct strength, so **larger `alpha` = stronger regularization**.
- Decision tree: limit `max_depth`, `min_samples_leaf`.
- k-NN: increase `k` (smoother boundary).
```python
LogisticRegression(C=0.1)           # smaller C  = stronger regularization
Ridge(alpha=10.0)                   # larger alpha = stronger regularization
DecisionTreeClassifier(max_depth=3) # shallower tree = less overfitting
```

---

## 5. Putting it together
The workflow from Week 4, now with real model choice and honest evaluation:
1. Split into train/test (and validate via cross-validation).
2. Try a few models with the shared API.
3. Compare with the **right metric** for the task.
4. Tune for the **train↔test gap**, not just raw score.
5. Report the final test score **once**.

---

## 6. Reading & videos
- *scikit-learn* user guide: "Supervised learning" and "Model evaluation" sections.
- *Machine Learning Systems* (mlsysbook.ai) — evaluation & overfitting chapters.
- Video: "Precision, Recall, and the Confusion Matrix" (linked in Canvas).
- Google ML Crash Course — "Classification" and "Regularization" modules.

---

## 7. Lab — Assignment A5 (due Sunday 11:59 PM PT)
**Goal:** train, evaluate, and compare supervised models on a real sklearn dataset.

1. Open `code/01_regression.ipynb`. Fit linear regression on **diabetes**; report **MAE, RMSE, R²**; add `Ridge` and compare. Plot predicted vs actual.
2. Open `code/02_classification.ipynb`. On a classification dataset, train **logistic regression, k-NN, and a decision tree**; print a **classification report** and **confusion matrix** for each.
3. **Overfitting study:** vary decision-tree `max_depth` (e.g. 1→15), plot **train vs test** accuracy, and identify where overfitting begins.
4. Write a 200-word analysis: which model won, by which metric, and *why* — and where you saw overfitting.
5. **Submit:** completed notebooks (or Colab links) + the analysis. Include a one-line **AI Use** note.

*A5 is graded (see syllabus rubric: correctness, evaluation, and analysis).*

---

## Key terms
**regression**, **classification**, **linear / logistic regression**, **k-NN**, **decision tree**, **MAE**, **RMSE**, **R²**, **accuracy**, **precision**, **recall**, **F1**, **confusion matrix**, **train/validation/test**, **cross-validation**, **overfitting / underfitting**, **regularization**, **hyperparameter**.
