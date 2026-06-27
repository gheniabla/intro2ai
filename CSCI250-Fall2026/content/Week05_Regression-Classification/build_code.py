"""Build Week 5 sample-code notebooks. Run: python build_code.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from nbgen import build_notebook

HERE = os.path.dirname(__file__)
CODE = os.path.join(HERE, "code")
os.makedirs(CODE, exist_ok=True)

# ---------------------------------------------------------------- notebook 1
regression = [
    ("md", "# Week 5 · Notebook 1 — Regression\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "Predict a **number**. We fit linear regression on the **diabetes** dataset, read its error "
           "with **MAE / RMSE / R²**, add **Ridge** regularization, and plot predicted vs actual.\n\n"
           "> Runs in Google Colab. No API keys needed. Part of **Assignment A5**."),
    ("md", "## 0. Install"),
    ("code", "!pip -q install scikit-learn matplotlib"),
    ("md", "## 1. Load the diabetes dataset\n"
           "442 patients, 10 normalized health measurements, target = disease progression after one year."),
    ("code", "from sklearn.datasets import load_diabetes\n"
             "from sklearn.model_selection import train_test_split\n\n"
             "X, y = load_diabetes(return_X_y=True)\n"
             "X_train, X_test, y_train, y_test = train_test_split(\n"
             "    X, y, test_size=0.2, random_state=42)\n"
             "print('train:', X_train.shape, ' test:', X_test.shape)\n"
             "print('target range:', y.min(), '->', y.max())"),
    ("md", "## 2. Fit linear regression\n"
           "Same `fit` / `predict` API as Week 4 — the target is just continuous now."),
    ("code", "from sklearn.linear_model import LinearRegression\n\n"
             "reg = LinearRegression().fit(X_train, y_train)\n"
             "preds = reg.predict(X_test)\n"
             "# self-check: one prediction per test row\n"
             "assert len(preds) == len(y_test)\n"
             "print('first 5 predictions:', preds[:5].round(1))\n"
             "print('first 5 actuals    :', y_test[:5])"),
    ("md", "## 3. Regression metrics\n"
           "You can't use accuracy on numbers — measure **how far off** you are.\n"
           "- **MAE**: average absolute miss (same units as y).\n"
           "- **RMSE**: squares errors first, so big misses hurt more.\n"
           "- **R²**: fraction of variance explained (1.0 = perfect)."),
    ("code", "from sklearn.metrics import (mean_absolute_error,\n"
             "    root_mean_squared_error, r2_score)\n\n"
             "mae  = mean_absolute_error(y_test, preds)\n"
             "rmse = root_mean_squared_error(y_test, preds)\n"
             "r2   = r2_score(y_test, preds)\n"
             "# self-checks: errors are non-negative and RMSE >= MAE always\n"
             "assert mae >= 0 and rmse >= 0\n"
             "assert rmse >= mae - 1e-9\n"
             "print(f'MAE : {mae:.2f}')\n"
             "print(f'RMSE: {rmse:.2f}   (>= MAE always)')\n"
             "print(f'R^2 : {r2:.3f}')"),
    ("md", "## 4. Add regularization: Ridge\n"
           "**Ridge** is linear regression that penalizes large weights (`alpha` = strength). "
           "On noisy data it often generalizes a little better. Compare the two."),
    ("code", "from sklearn.linear_model import Ridge\n\n"
             "for alpha in [0.1, 1.0, 10.0]:\n"
             "    rdg = Ridge(alpha=alpha).fit(X_train, y_train)\n"
             "    p = rdg.predict(X_test)\n"
             "    print(f'Ridge(alpha={alpha:>4}):  '\n"
             "          f'RMSE={root_mean_squared_error(y_test, p):.2f}  '\n"
             "          f'R^2={r2_score(y_test, p):.3f}')"),
    ("md", "## 5. Plot predicted vs actual\n"
           "A perfect model lands on the diagonal. Spread around it = error."),
    ("code", "import matplotlib.pyplot as plt\n\n"
             "plt.figure(figsize=(5.5, 5.5))\n"
             "plt.scatter(y_test, preds, alpha=0.6, edgecolor='k')\n"
             "lims = [y_test.min(), y_test.max()]\n"
             "plt.plot(lims, lims, 'r--', label='perfect')\n"
             "plt.xlabel('actual'); plt.ylabel('predicted')\n"
             "plt.title('Diabetes — predicted vs actual'); plt.legend(); plt.show()"),
    ("md", "## 6. Reading the coefficients\n"
           "`reg.coef_` holds **one weight per feature**. A coefficient is the change in the "
           "predicted target for a **one-unit increase in that feature, holding the others "
           "fixed**. Read it two ways:\n"
           "- **Sign** — positive pushes progression **up**, negative pulls it **down**.\n"
           "- **Magnitude** — bigger `|coef|` = stronger pull. The diabetes features are already "
           "normalized to a common scale, so the magnitudes are directly comparable; the largest "
           "`|coef|` is the most influential feature *for this model*.\n\n"
           "Remember: this is **association, not causation**."),
    ("code", "import numpy as np\n"
             "from sklearn.datasets import load_diabetes\n\n"
             "names = load_diabetes().feature_names\n"
             "order = np.argsort(np.abs(reg.coef_))[::-1]   # largest |weight| first\n"
             "print('intercept:', round(reg.intercept_, 2))\n"
             "for i in order:\n"
             "    print(f'{names[i]:>4}: {reg.coef_[i]:+8.1f}')\n"
             "# self-check: one coefficient per input feature\n"
             "assert len(reg.coef_) == X_train.shape[1]\n"
             "print('\\nmost influential feature:', names[order[0]])"),
    ("md", "---\n## A5 — Part 1 tasks\n"
           "1. Report MAE, RMSE, and R² for plain LinearRegression (done above).\n"
           "2. Pick the best `Ridge` alpha by RMSE and state whether it beat LinearRegression.\n"
           "3. Print `reg.coef_` — which feature has the largest absolute weight?\n"
           "4. Write 2–3 sentences interpreting the predicted-vs-actual plot."),
    ("code", "# Your A5 Part 1 work here\n"),
]
build_notebook(regression, os.path.join(CODE, "01_regression.ipynb"))

# ---------------------------------------------------------------- notebook 2
classification = [
    ("md", "# Week 5 · Notebook 2 — Classification\n"
           "**CSCI 250 · Fall 2026**\n\n"
           "Predict a **category**. We train **logistic regression, k-NN, and a decision tree** on a "
           "two-class dataset, read **precision / recall / F1 / confusion matrix**, and run an "
           "**overfitting study** on tree depth.\n\n"
           "> Runs in Google Colab. No API keys needed. Part of **Assignment A5**."),
    ("md", "## 0. Install"),
    ("code", "!pip -q install scikit-learn matplotlib"),
    ("md", "## 1. Make a classification dataset\n"
           "`make_classification` builds a synthetic, slightly **imbalanced** problem — perfect for "
           "showing why accuracy alone can mislead."),
    ("code", "from sklearn.datasets import make_classification\n"
             "from sklearn.model_selection import train_test_split\n\n"
             "X, y = make_classification(\n"
             "    n_samples=1000, n_features=10, n_informative=5,\n"
             "    weights=[0.8, 0.2], random_state=42)   # 80/20 class imbalance\n"
             "X_train, X_test, y_train, y_test = train_test_split(\n"
             "    X, y, test_size=0.25, random_state=42, stratify=y)\n"
             "import numpy as np\n"
             "print('class balance (train):', np.bincount(y_train))"),
    ("md", "## 2. Train three classifiers\n"
           "Identical API; only the estimator class changes (Week 4's big idea)."),
    ("code", "from sklearn.linear_model import LogisticRegression\n"
             "from sklearn.neighbors import KNeighborsClassifier\n"
             "from sklearn.tree import DecisionTreeClassifier\n\n"
             "models = {\n"
             "    'logreg': LogisticRegression(max_iter=1000),\n"
             "    'knn   ': KNeighborsClassifier(n_neighbors=5),\n"
             "    'tree  ': DecisionTreeClassifier(max_depth=5, random_state=42),\n"
             "}\n"
             "for name, m in models.items():\n"
             "    m.fit(X_train, y_train)\n"
             "    acc = m.score(X_test, y_test)\n"
             "    assert 0.0 <= acc <= 1.0   # accuracy is always a fraction in [0, 1]\n"
             "    print(name, '-> accuracy', round(acc, 3))"),
    ("md", "## 2b. Feature scaling and k-NN — before vs after\n"
           "k-NN votes by **distance**, so a feature with a huge range can drown out the others. "
           "**StandardScaler** rescales every feature to mean 0, std 1 so each contributes fairly. "
           "We blow up one feature's scale to make the effect obvious, then compare the **same** "
           "k-NN with and without scaling. (A `Pipeline` fits the scaler on **train only** — no "
           "test leakage.)"),
    ("code", "from sklearn.preprocessing import StandardScaler\n"
             "from sklearn.pipeline import make_pipeline\n\n"
             "# exaggerate the scale problem: multiply ONE feature by 1000\n"
             "Xtr = X_train.copy(); Xte = X_test.copy()\n"
             "Xtr[:, 0] *= 1000; Xte[:, 0] *= 1000\n\n"
             "raw    = KNeighborsClassifier(n_neighbors=5).fit(Xtr, y_train)\n"
             "scaled = make_pipeline(StandardScaler(),\n"
             "                       KNeighborsClassifier(n_neighbors=5)).fit(Xtr, y_train)\n\n"
             "acc_raw    = raw.score(Xte, y_test)\n"
             "acc_scaled = scaled.score(Xte, y_test)\n"
             "print(f'k-NN WITHOUT scaling: {acc_raw:.3f}')\n"
             "print(f'k-NN WITH    scaling: {acc_scaled:.3f}')\n"
             "# self-check: both are valid accuracies, and scaling should not hurt here\n"
             "assert 0.0 <= acc_raw <= 1.0 and 0.0 <= acc_scaled <= 1.0\n"
             "assert acc_scaled >= acc_raw\n"
             "print('assert passed: scaling helped (or tied) for distance-based k-NN ✔')"),
    ("md", "Trees split one feature at a time, so they are **scale-invariant** — scaling won't "
           "change a decision tree's result. Standardize for **k-NN, SVMs, and neural nets**; "
           "you can skip it for tree-based models."),

    ("md", "## 3. Why accuracy isn't enough\n"
           "With 80/20 classes, even a lazy model scores ~0.8. **Precision/recall/F1** tell the real story. "
           "`classification_report` prints all three per class. Print it for **all three** models so you "
           "can compare them by **F1** (don't prejudge a winner)."),
    ("code", "from sklearn.metrics import classification_report, confusion_matrix\n\n"
             "for name, m in models.items():\n"
             "    print('=' * 56)\n"
             "    print(name.strip(), 'classification report')\n"
             "    print(classification_report(y_test, m.predict(X_test), digits=3))"),
    ("md", "## 4. The confusion matrix\n"
           "Rows = actual, columns = predicted. The off-diagonal cells are exactly your mistakes "
           "(false positives and false negatives). We show one model below — swap `clf` for any of "
           "the three and re-run to compare their mistakes."),
    ("code", "import matplotlib.pyplot as plt\n"
             "from sklearn.metrics import ConfusionMatrixDisplay\n\n"
             "clf = models['logreg']      # pick any model to inspect — not a prejudged 'best'\n"
             "preds = clf.predict(X_test)\n"
             "cm = confusion_matrix(y_test, preds)\n"
             "print(cm)\n"
             "ConfusionMatrixDisplay(cm, display_labels=[0, 1]).plot(cmap='Blues')\n"
             "plt.title('Confusion matrix (logistic regression)'); plt.show()"),
    ("md", "## 5. Overfitting study: decision-tree depth\n"
           "A deeper tree fits training data better — until it starts **memorizing noise**. Watch the "
           "**train↔test gap** open up. That gap is the signature of overfitting."),
    ("code", "depths = range(1, 16)\n"
             "train_acc, test_acc = [], []\n"
             "for d in depths:\n"
             "    t = DecisionTreeClassifier(max_depth=d, random_state=42).fit(X_train, y_train)\n"
             "    train_acc.append(t.score(X_train, y_train))\n"
             "    test_acc.append(t.score(X_test, y_test))\n\n"
             "plt.figure(figsize=(7, 4))\n"
             "plt.plot(depths, train_acc, 'o-', label='train')\n"
             "plt.plot(depths, test_acc,  's-', label='test')\n"
             "plt.xlabel('max_depth'); plt.ylabel('accuracy')\n"
             "plt.title('Decision tree: train vs test accuracy')\n"
             "plt.legend(); plt.grid(alpha=0.3); plt.show()"),
    ("md", "Where the two curves **diverge** is where overfitting begins: train keeps climbing toward "
           "1.0 while test plateaus or drops. The best `max_depth` is usually near the peak of the "
           "**test** curve — that is regularization by limiting complexity."),
    ("md", "## 6. Cross-validation: a more stable score\n"
           "A single split can be lucky. `cross_val_score` averages over 5 folds for a steadier estimate."),
    ("code", "from sklearn.model_selection import cross_val_score\n\n"
             "for name, m in models.items():\n"
             "    s = cross_val_score(m, X_train, y_train, cv=5, scoring='f1')\n"
             "    assert len(s) == 5 and (0.0 <= s).all() and (s <= 1.0).all()\n"
             "    print(f'{name}  F1 = {s.mean():.3f} +/- {s.std():.3f}')"),
    ("md", "---\n## A5 — Part 2 tasks\n"
           "1. Print a `classification_report` and confusion matrix for **all three** models.\n"
           "2. State which model wins by **F1** (not accuracy) and why F1 is the fairer metric here.\n"
           "3. From the overfitting plot, give the `max_depth` where overfitting begins.\n"
           "4. Write a 200-word analysis (combine with Part 1) for your A5 submission. Add an **AI Use** note."),
    ("code", "# Your A5 Part 2 work here\n"),
]
build_notebook(classification, os.path.join(CODE, "02_classification.ipynb"))

print("wrote Week 5 notebooks to", CODE)
