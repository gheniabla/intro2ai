"""Build Week 4 sample-code notebooks. Run: python build_code.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from nbgen import build_notebook

HERE = os.path.dirname(__file__)
CODE = os.path.join(HERE, "code")
os.makedirs(CODE, exist_ok=True)

# ---------------------------------------------------------------- notebook 1
ml_workflow = [
    ("md", "# Week 4 · Notebook 1 — The End-to-End ML Workflow\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "AI vs ML vs DL vs GenAI in one picture, then a real supervised-learning "
           "pipeline on the classic **Iris** dataset: *data → split → train → evaluate → predict.*\n\n"
           "> Runs in Google Colab. No API keys needed."),
    ("md", "## 0. Install\n"
           "scikit-learn and matplotlib are preinstalled in Colab; this is here for a clean local run."),
    ("code", "!pip -q install scikit-learn matplotlib"),
    ("md", "## 1. The big picture: AI ⊃ ML ⊃ DL ⊃ GenAI\n"
           "- **AI** — the broad goal of intelligent behavior.\n"
           "- **ML** — learning patterns from data (this week).\n"
           "- **DL** — ML with multi-layer neural networks (Week 6).\n"
           "- **GenAI / LLMs** — DL that *generates* content (back half of the course).\n\n"
           "Everything below is a special case of the thing above it."),
    ("md", "## 2. Get data\n"
           "We use **Iris**: 150 flowers, 4 measurements each, 3 species. A tidy table is "
           "the starting point of every supervised ML project."),
    ("code", "from sklearn.datasets import load_iris\n"
             "import pandas as pd\n\n"
             "iris = load_iris(as_frame=True)\n"
             "df = iris.frame                       # features + 'target' column\n"
             "print('shape:', df.shape)\n"
             "print('features:', iris.feature_names)\n"
             "print('classes :', list(iris.target_names))\n"
             "df.head()"),
    ("md", "## 3. Explore\n"
           "Always look before you model. Class balance and feature ranges matter."),
    ("code", "print(df['target'].value_counts().sort_index())   # 50 of each — balanced\n"
             "df.describe().round(2)"),
    ("code", "import matplotlib.pyplot as plt\n\n"
             "# Two features colored by species — already fairly separable\n"
             "plt.figure(figsize=(6, 4))\n"
             "plt.scatter(df['petal length (cm)'], df['petal width (cm)'],\n"
             "            c=df['target'], cmap='viridis', edgecolor='k')\n"
             "plt.xlabel('petal length (cm)'); plt.ylabel('petal width (cm)')\n"
             "plt.title('Iris — petal length vs width'); plt.show()"),
    ("md", "## 4. Split: hold out a test set\n"
           "The single most important habit in ML: **never evaluate on data you trained on.** "
           "`stratify=y` keeps the 3 classes balanced in both splits."),
    ("code", "from sklearn.model_selection import train_test_split\n\n"
             "X, y = iris.data, iris.target\n"
             "X_train, X_test, y_train, y_test = train_test_split(\n"
             "    X, y, test_size=0.2, random_state=42, stratify=y)\n"
             "print('train:', X_train.shape, ' test:', X_test.shape)"),
    ("md", "## 5. Train (fit) and 6. Evaluate\n"
           "A k-Nearest-Neighbors classifier: predict a flower's species from its 3 closest neighbors."),
    ("code", "from sklearn.neighbors import KNeighborsClassifier\n\n"
             "clf = KNeighborsClassifier(n_neighbors=3)\n"
             "clf.fit(X_train, y_train)                 # learn\n"
             "acc = clf.score(X_test, y_test)           # evaluate on held-out data\n"
             "print(f'test accuracy: {acc:.3f}')"),
    ("md", "### The cardinal rule, demonstrated\n"
           "Accuracy on the *training* set is optimistic — it measures memorization, not generalization."),
    ("code", "print(f'train accuracy: {clf.score(X_train, y_train):.3f}  (optimistic!)')\n"
             "print(f'test  accuracy: {clf.score(X_test,  y_test):.3f}  (what we report)')"),
    ("md", "## 7. Predict on new data\n"
           "Hand the trained model a brand-new flower measurement."),
    ("code", "# Build the new sample as a DataFrame with the SAME column names the model\n"
             "# was fit on — this avoids sklearn's 'feature names' warning.\n"
             "new_flower = pd.DataFrame([[5.1, 3.5, 1.4, 0.2]],\n"
             "                          columns=iris.feature_names)  # sepal/petal length & width\n"
             "pred = clf.predict(new_flower)[0]\n"
             "print('predicted species:', iris.target_names[pred])"),
    ("md", "## 8. Iterate\n"
           "Try `n_neighbors=1`, `5`, `15`. Does test accuracy change? You just did your "
           "first hyperparameter tuning — formalized next week.\n\n"
           "**Takeaway:** a working supervised model is ~8 lines. Week 5 unpacks *which* model and *which* metric."),
    ("code", "# Your experiment: loop over a few k values and print test accuracy\n"
             "for k in [1, 3, 5, 15]:\n"
             "    m = KNeighborsClassifier(n_neighbors=k).fit(X_train, y_train)\n"
             "    print(f'k={k:>2}  test acc={m.score(X_test, y_test):.3f}')"),
]
build_notebook(ml_workflow, os.path.join(CODE, "01_ml_workflow.ipynb"))

# ---------------------------------------------------------------- notebook 2
sklearn_basics = [
    ("md", "# Week 4 · Notebook 2 — scikit-learn Basics\n"
           "**CSCI 250 · Fall 2026**\n\n"
           "The thing that makes scikit-learn easy: **one consistent API.** Almost every model is "
           "an *estimator* with `.fit()` and `.predict()`. Learn it once, reuse it everywhere.\n\n"
           "> Runs in Google Colab. No API keys needed."),
    ("md", "## 0. Install"),
    ("code", "!pip -q install scikit-learn matplotlib"),
    ("md", "## 1. The estimator pattern\n"
           "Every supervised estimator follows the same four steps:\n"
           "1. **instantiate** the model, 2. **fit** on training data, "
           "3. **predict** on new data, 4. **score** it."),
    ("code", "from sklearn.datasets import load_iris\n"
             "from sklearn.model_selection import train_test_split\n"
             "from sklearn.linear_model import LogisticRegression\n\n"
             "X, y = load_iris(return_X_y=True)\n"
             "X_train, X_test, y_train, y_test = train_test_split(\n"
             "    X, y, test_size=0.2, random_state=42, stratify=y)\n\n"
             "model = LogisticRegression(max_iter=1000)   # 1. instantiate\n"
             "model.fit(X_train, y_train)                 # 2. fit\n"
             "preds = model.predict(X_test)               # 3. predict\n"
             "print('first 5 predictions:', preds[:5])\n"
             "print('test accuracy     :', round(model.score(X_test, y_test), 3))  # 4. score"),
    ("md", "## 2. The API barely changes between models\n"
           "Swap the estimator class; the rest of your code is identical. That is the whole point."),
    ("code", "from sklearn.tree import DecisionTreeClassifier\n"
             "from sklearn.neighbors import KNeighborsClassifier\n\n"
             "for name, est in [('logreg', LogisticRegression(max_iter=1000)),\n"
             "                  ('tree  ', DecisionTreeClassifier(random_state=42)),\n"
             "                  ('knn   ', KNeighborsClassifier(n_neighbors=5))]:\n"
             "    est.fit(X_train, y_train)\n"
             "    print(name, '-> test accuracy', round(est.score(X_test, y_test), 3))"),
    ("md", "## 3. Understanding train_test_split\n"
           "It shuffles, then slices. The arguments matter:\n"
           "- `test_size` — fraction held out for testing.\n"
           "- `random_state` — fixes the shuffle so results are reproducible.\n"
           "- `stratify=y` — preserves class proportions (important for classification)."),
    ("code", "import numpy as np\n\n"
             "# Without a fixed random_state, the split (and the score) changes each run.\n"
             "for rs in [0, 1, 2]:\n"
             "    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=rs, stratify=y)\n"
             "    m = KNeighborsClassifier(n_neighbors=5).fit(Xtr, ytr)\n"
             "    print(f'random_state={rs}: test acc={m.score(Xte, yte):.3f}')"),
    ("md", "## 4. A different task: regression\n"
           "Same API, numeric target. The **diabetes** dataset predicts disease progression from "
           "10 health measurements. Here `.score()` returns R² instead of accuracy."),
    ("code", "from sklearn.datasets import load_diabetes\n"
             "from sklearn.linear_model import LinearRegression\n\n"
             "Xd, yd = load_diabetes(return_X_y=True)\n"
             "Xtr, Xte, ytr, yte = train_test_split(Xd, yd, test_size=0.2, random_state=42)\n\n"
             "reg = LinearRegression()\n"
             "reg.fit(Xtr, ytr)\n"
             "print('first 3 predictions:', reg.predict(Xte)[:3].round(1))\n"
             "print('R^2 on test set    :', round(reg.score(Xte, yte), 3))"),
    ("md", "## 5. Generative AI is ML too\n"
           "The Claude/Gemini calls from Week 1 are deep-learning models trained the same way in "
           "spirit: data in, parameters learned, evaluated on held-out examples — just enormously larger. "
           "Mastering this small API makes the big models far less mysterious."),
    ("md", "---\n## Try it yourself\n"
           "1. Change `LogisticRegression` to `DecisionTreeClassifier` in section 1 — note how few lines change.\n"
           "2. In section 3, try `test_size=0.5`. Does accuracy get more or less stable?\n"
           "3. For the diabetes regressor, print `reg.coef_` — which of the 10 features has the largest weight?"),
    ("code", "# Your experiments here\n"),
]
build_notebook(sklearn_basics, os.path.join(CODE, "02_sklearn_basics.ipynb"))

print("wrote Week 4 notebooks to", CODE)
