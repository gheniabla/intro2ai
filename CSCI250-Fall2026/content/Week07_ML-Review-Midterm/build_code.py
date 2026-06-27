"""Build Week 7 review + practice-midterm notebooks. Run: python build_code.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from nbgen import build_notebook

HERE = os.path.dirname(__file__)
CODE = os.path.join(HERE, "code")
os.makedirs(CODE, exist_ok=True)

# ---------------------------------------------------------------- notebook 1
review = [
    ("md", "# Week 7 · Notebook 1 — Review & Worked Solutions (Weeks 1–6)\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "Run each section to refresh a week and check your understanding. These are "
           "the **worked answers** to the study guide's self-checks and the practice "
           "midterm. Use them *after* you have tried the questions yourself.\n\n"
           "> Standard data-science stack — preinstalled in Colab. scikit-learn import "
           "is guarded so the notebook still runs if it is missing."),

    ("md", "## Setup"),
    ("code", "import numpy as np\n"
             "import pandas as pd\n"
             "import matplotlib.pyplot as plt\n"
             "try:\n"
             "    import sklearn\n"
             "    HAS_SK = True\n"
             "    print('scikit-learn', sklearn.__version__)\n"
             "except Exception as e:\n"
             "    HAS_SK = False\n"
             "    print('scikit-learn missing -> NumPy fallbacks used.', e)"),

    ("md", "## Week 1 — Python\n"
           "**Q:** mutable or immutable? **A:** `list` and `dict` are *mutable*; "
           "`tuple` and `str` are *immutable*."),
    ("code", "examples = {'list': [1, 2], 'tuple': (1, 2), 'dict': {'a': 1}, 'str': 'hi'}\n"
             "examples['list'].append(3)          # works (mutable)\n"
             "try:\n"
             "    examples['tuple'][0] = 99        # TypeError (immutable)\n"
             "except TypeError as e:\n"
             "    print('tuple is immutable:', e)\n"
             "print(examples['list'])\n"
             "print({w: len(w) for w in 'the quick brown fox'.split()})  # comprehension"),

    ("md", "## Week 2 — NumPy & broadcasting\n"
           "**Q:** shape of `[[1,2,3]] + [[10],[20]]`? **A:** `(1,3)` broadcasts with "
           "`(2,1)` to **`(2,3)`**."),
    ("code", "a = np.array([[1, 2, 3]])     # shape (1, 3)\n"
             "b = np.array([[10], [20]])    # shape (2, 1)\n"
             "out = a + b                   # broadcasts to (2, 3)\n"
             "print(out, out.shape)\n"
             "print('column means (axis=0):', out.mean(axis=0))\n"
             "print('row means (axis=1):   ', out.mean(axis=1))"),

    ("md", "## Week 3 — Pandas groupby & a plot\n"
           "**Q:** what does `df.groupby('city')['sales'].mean()` return? "
           "**A:** a `Series` indexed by city, holding each city's mean sales."),
    ("code", "df = pd.DataFrame({\n"
             "    'city': ['SD', 'SD', 'LA', 'LA', 'LA'],\n"
             "    'sales': [10, 14, 9, 7, 20],\n"
             "})\n"
             "by_city = df.groupby('city')['sales'].mean()\n"
             "print(by_city)\n"
             "by_city.plot(kind='bar', title='Mean sales by city'); plt.show()"),

    ("md", "## Week 4 — train/test split & the sklearn API\n"
           "**Q:** why hold out a test set? **A:** to estimate **generalization** to "
           "unseen data; tuning on the test set leaks information and inflates scores."),
    ("code", "rng = np.random.default_rng(0)\n"
             "X = rng.standard_normal((100, 1))\n"
             "y = (3 * X[:, 0] + 0.5 + 0.3 * rng.standard_normal(100))\n"
             "if HAS_SK:\n"
             "    from sklearn.model_selection import train_test_split\n"
             "    from sklearn.linear_model import LinearRegression\n"
             "    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=0)\n"
             "    model = LinearRegression().fit(Xtr, ytr)     # fit\n"
             "    print('test R^2:', round(model.score(Xte, yte), 3))  # predict+evaluate\n"
             "else:\n"
             "    # NumPy least-squares fallback\n"
             "    A = np.c_[X, np.ones(len(X))]\n"
             "    coef, *_ = np.linalg.lstsq(A, y, rcond=None)\n"
             "    print('slope, intercept ~', np.round(coef, 3))"),

    ("md", "## Week 5 — classification metrics from a confusion matrix\n"
           "**Q:** read a confusion matrix → accuracy/precision/recall.\n"
           "With `TP=40, FP=10, FN=5, TN=45`:  accuracy=(40+45)/100=**0.85**, "
           "precision=40/(40+10)=**0.80**, recall=40/(40+5)≈**0.89**."),
    ("code", "TP, FP, FN, TN = 40, 10, 5, 45\n"
             "accuracy  = (TP + TN) / (TP + FP + FN + TN)\n"
             "precision = TP / (TP + FP)\n"
             "recall    = TP / (TP + FN)\n"
             "f1 = 2 * precision * recall / (precision + recall)\n"
             "print(f'accuracy={accuracy:.2f}  precision={precision:.2f} '\n"
             "      f'recall={recall:.2f}  F1={f1:.2f}')\n"
             "print('Reminder: accuracy misleads on imbalanced data -> prefer precision/recall/F1.')"),

    ("md", "## Week 5 — overfitting in one picture\n"
           "**Q:** train acc 0.99, test acc 0.62 — what is wrong? **A:** **overfitting** "
           "— the model memorized the training data (incl. noise) and fails to generalize."),
    ("code", "# Fit polynomials of rising degree; watch train error fall but test error rise.\n"
             "rng = np.random.default_rng(1)\n"
             "xt = np.sort(rng.uniform(-1, 1, 20)); yt = np.sin(3*xt) + 0.1*rng.standard_normal(20)\n"
             "xv = np.linspace(-1, 1, 100); yv = np.sin(3*xv)\n"
             "for deg in [1, 3, 12]:\n"
             "    c = np.polyfit(xt, yt, deg)\n"
             "    tr = np.mean((np.polyval(c, xt) - yt)**2)\n"
             "    te = np.mean((np.polyval(c, xv) - yv)**2)\n"
             "    print(f'degree {deg:2d}: train MSE={tr:.3f}  test MSE={te:.3f}')\n"
             "print('High degree: tiny train error, large test error = overfitting.')"),

    ("md", "## Week 6 — activations & the softmax/next-token idea\n"
           "**Q:** which activation gives a multi-class probability distribution? "
           "**A:** **softmax** (the same step an LLM uses to pick the next token)."),
    ("code", "def relu(z):    return np.maximum(0, z)\n"
             "def sigmoid(z): return 1 / (1 + np.exp(-z))\n"
             "def softmax(z):\n"
             "    e = np.exp(z - z.max())\n"
             "    return e / e.sum()\n\n"
             "scores = np.array([2.0, 1.0, 0.1])     # raw class scores (logits)\n"
             "print('relu   :', relu(np.array([-2., 0., 3.])))\n"
             "print('sigmoid:', np.round(sigmoid(np.array([-2., 0., 2.])), 3))\n"
             "print('softmax:', np.round(softmax(scores), 3), ' sums to', softmax(scores).sum())"),

    ("md", "## Week 6 — the gradient-descent update\n"
           "**Q:** in `w ← w − lr·grad`, what is `lr`? **A:** the **learning rate** — the "
           "step size. Too large overshoots/diverges; too small trains slowly."),
    ("code", "# Minimize f(w) = (w - 3)^2  (min at w=3). grad = 2*(w-3).\n"
             "w, lr = 0.0, 0.1\n"
             "for step in range(15):\n"
             "    grad = 2 * (w - 3)\n"
             "    w = w - lr * grad\n"
             "print('converged w ~', round(w, 3), '(target 3.0)')"),

    ("md", "---\n# Worked answers to the Practice Midterm (`02_practice_midterm.ipynb`)\n"
           "Try every item on your own first. These are the worked answers — **no surprises**: "
           "every part of the practice midterm has a solution here."),

    ("md", "## Practice Midterm — Part A (multiple choice)\n"
           "- **A1 = (c) tuple** — tuples are immutable; list/dict/set are mutable.\n"
           "- **A2 = (c) (2,3)** — `(1,3)` broadcasts with `(2,1)` to `(2,3)`.\n"
           "- **A3 = (b) estimate generalization** — the test set stands in for unseen data.\n"
           "- **A4 = (b) overfitting** — high train acc, low test acc = memorized noise.\n"
           "- **A5 = (c) softmax** — turns scores into a multi-class probability distribution."),
    ("code", "# Verify A2 (the broadcast shape) and A5 (softmax sums to 1).\n"
             "a = np.array([[1, 2, 3]]); b = np.array([[10], [20]])\n"
             "print('A2 shape:', (a + b).shape)            # (2, 3)\n"
             "def softmax(z):\n"
             "    e = np.exp(z - z.max()); return e / e.sum()\n"
             "print('A5 softmax sums to:', round(float(softmax(np.array([2., 1., .1])).sum()), 3))"),

    ("md", "## Practice Midterm — Part B (short answer)\n"
           "- **B1.** **AI ⊃ ML ⊃ DL ⊃ GenAI**: AI is the broad goal of intelligent behavior; "
           "ML learns patterns from data; DL is ML with multi-layer neural nets; GenAI is DL that "
           "*generates* content (text/images/code), e.g. LLMs.\n"
           "- **B2.** **Regression** predicts a continuous number (metric: MAE or R²); "
           "**classification** predicts a discrete label (metric: accuracy or F1).\n"
           "- **B3.** **Precision** = of the items I flagged positive, how many were actually positive. "
           "**Recall** = of the actual positives, how many did I catch.\n"
           "- **B4.** Without a **nonlinear** activation, stacked linear layers collapse into a single "
           "linear layer — no matter how many you stack, you can only draw a straight boundary. "
           "Nonlinearity (e.g. ReLU) lets the network bend the boundary into any shape.\n"
           "- **B5.** **Backprop** computes the gradient of the loss w.r.t. every weight (the chain rule, "
           "in one backward pass); the **optimizer** then nudges each weight in the downhill direction "
           "(`w ← w − lr·grad`)."),

    ("md", "## Practice Midterm — Part C (read the code: what does it print?)\n"
           "Predicted outputs below; run the cell to confirm."),
    ("code", "x = np.arange(6).reshape(2, 3)\n"
             "print('C1 x.sum(axis=0) ->', x.sum(axis=0).tolist())   # [3, 5, 7]  (down columns)\n"
             "print('C2 x.sum(axis=1) ->', x.sum(axis=1).tolist())   # [3, 12]    (across rows)\n"
             "df = pd.DataFrame({'g': ['a', 'a', 'b'], 'v': [1, 3, 10]})\n"
             "print('C3 groupby mean ->', df.groupby('g')['v'].mean().to_dict())  # {'a': 2.0, 'b': 10.0}\n"
             "print('C4 f(6) ->', [i*i for i in range(6) if i % 2 == 1])          # [1, 9, 25]"),

    ("md", "## Practice Midterm — Part D (compute by hand, then verify)\n"
           "**D1.** With `TP=30, FP=20, FN=10, TN=40`: accuracy=(30+40)/100=**0.70**, "
           "precision=30/(30+20)=**0.60**, recall=30/(30+10)=**0.75**, "
           "F1=2·0.60·0.75/(0.60+0.75)≈**0.67**.\n\n"
           "**D2.** For `f(w)=(w-5)²` with `w0=0`, `lr=0.1`: grad=2·(0−5)=**−10**, so the first "
           "update `w ← 0 − 0.1·(−10) = 1.0` moves **toward** 5 (gradient descent always steps downhill)."),
    ("code", "# D1\n"
             "TP, FP, FN, TN = 30, 20, 10, 40\n"
             "accuracy  = (TP + TN) / (TP + FP + FN + TN)\n"
             "precision = TP / (TP + FP)\n"
             "recall    = TP / (TP + FN)\n"
             "f1 = 2 * precision * recall / (precision + recall)\n"
             "print(f'D1  accuracy={accuracy:.2f}  precision={precision:.2f} '\n"
             "      f'recall={recall:.2f}  F1={f1:.2f}')   # 0.70 0.60 0.75 0.67\n\n"
             "# D2\n"
             "w, lr = 0.0, 0.1\n"
             "grad = 2 * (w - 5)\n"
             "print('D2  first grad =', grad, ' w after one step =', w - lr * grad, '(toward 5)')"),

    ("md", "## Practice Midterm — Part E (concept)\n"
           "**E1 (model answer).** An LLM is a **very deep neural network** (a Transformer) whose "
           "behavior is set by billions of **weights** organized into **layers** — the same weights and "
           "layers from Week 6, just far more of them. It is trained by **gradient descent** + "
           "**backprop** to **minimize cross-entropy** on next-token prediction, and its final **softmax** "
           "turns scores over the vocabulary into the probability of each possible next token. Every one "
           "of those terms is exactly what you built by hand this half of the course — that is why neural "
           "networks are the foundation under LLMs."),

    ("md", "## You're ready\n"
           "If every cell above made sense, you have the Weeks 1–6 core. Now take the "
           "**practice midterm** (`02_practice_midterm.ipynb`) on your own — **no AI** — "
           "then come back here to check anything you missed."),
]
build_notebook(review, os.path.join(CODE, "01_review_solutions.ipynb"))

# ---------------------------------------------------------------- notebook 2
practice = [
    ("md", "# Week 7 · Notebook 2 — Practice Midterm (AI-RESTRICTED)\n"
           "**CSCI 250 · Fall 2026**\n\n"
           "> **Take this on your own. Do NOT use Claude, Gemini, Claude Code, Copilot, "
           "or any AI assistant** — the real midterm (Sat Oct 11, 5:30–11:59 PM PT) is "
           "AI-restricted, so practice the way you'll be tested.\n\n"
           "Write your answers in the blank cells. Then open "
           "`01_review_solutions.ipynb` to check the worked answers. Covers Weeks 1–6."),

    ("md", "## Part A — Multiple choice (pick one)\n"
           "**A1.** Which Python type is **immutable**?  (a) list  (b) dict  (c) tuple  (d) set\n\n"
           "**A2.** `np.array([[1,2,3]]) + np.array([[10],[20]])` has shape:  "
           "(a) (1,3)  (b) (2,1)  (c) (2,3)  (d) error\n\n"
           "**A3.** You hold out a test set in order to:  (a) train faster  "
           "(b) estimate generalization  (c) increase accuracy  (d) avoid imports\n\n"
           "**A4.** Train acc 0.98, test acc 0.60 indicates:  (a) underfitting  "
           "(b) overfitting  (c) data leakage fixed  (d) perfect model\n\n"
           "**A5.** Which activation yields a multi-class probability distribution?  "
           "(a) ReLU  (b) sigmoid  (c) softmax  (d) tanh"),
    ("md", "### Your answers to Part A\n"
           "A1=  A2=  A3=  A4=  A5="),

    ("md", "## Part B — Short answer (1–3 sentences each)\n"
           "**B1.** Define AI vs ML vs DL vs GenAI and how they nest.\n\n"
           "**B2.** What is the difference between **regression** and **classification**? "
           "Give one metric for each.\n\n"
           "**B3.** In one sentence each, what do **precision** and **recall** measure?\n\n"
           "**B4.** Why does a neural network need a **nonlinear activation** between "
           "layers?\n\n"
           "**B5.** In plain English, what does **backpropagation** compute, and what "
           "does the optimizer do with it?"),
    ("md", "### Your answers to Part B\n*(type here)*"),

    ("md", "## Part C — Read the code: what does it print?\n"
           "Predict the output **before** running. Then run to check."),
    ("code", "import numpy as np\n"
             "x = np.arange(6).reshape(2, 3)\n"
             "print(x.sum(axis=0))   # C1: predict first\n"
             "print(x.sum(axis=1))   # C2: predict first"),
    ("code", "import pandas as pd\n"
             "df = pd.DataFrame({'g': ['a','a','b'], 'v': [1, 3, 10]})\n"
             "print(df.groupby('g')['v'].mean().to_dict())   # C3: predict first"),
    ("code", "def f(n):\n"
             "    return [i*i for i in range(n) if i % 2 == 1]\n"
             "print(f(6))   # C4: predict first"),

    ("md", "## Part D — Compute by hand, then verify\n"
           "**D1.** A classifier gives `TP=30, FP=20, FN=10, TN=40`. Compute "
           "**accuracy, precision, recall, F1** by hand, then check with the cell below."),
    ("code", "TP, FP, FN, TN = 30, 20, 10, 40\n"
             "# Fill in, then run to check your hand calculation:\n"
             "accuracy  = (TP + TN) / (TP + FP + FN + TN)\n"
             "precision = TP / (TP + FP)\n"
             "recall    = TP / (TP + FN)\n"
             "f1 = 2 * precision * recall / (precision + recall)\n"
             "print(round(accuracy,2), round(precision,2), round(recall,2), round(f1,2))"),
    ("md", "**D2.** Gradient descent minimizes `f(w) = (w-5)**2` with `w0=0`, `lr=0.1`. "
           "What is `grad` at the first step, and is the first update toward or away "
           "from 5? (grad = 2*(w-5).) Verify below."),
    ("code", "w, lr = 0.0, 0.1\n"
             "grad = 2 * (w - 5)\n"
             "w_next = w - lr * grad\n"
             "print('first grad =', grad, ' w after one step =', w_next)"),

    ("md", "## Part E — Concept (2–3 sentences)\n"
           "**E1.** Explain why we say neural networks are *the foundation under LLMs*. "
           "Reference at least three terms from Week 6 (e.g., weights, layers, softmax, "
           "gradient descent, cross-entropy)."),
    ("md", "### Your answer to Part E\n*(type here)*"),

    ("md", "---\n## Done?\n"
           "Check your work in `01_review_solutions.ipynb`. Note every item you missed "
           "and re-read that week's section in `document.md` before **Saturday Oct 11**.\n\n"
           "**Reminder: the real midterm is AI-restricted.**"),
]
build_notebook(practice, os.path.join(CODE, "02_practice_midterm.ipynb"))

print("wrote Week 7 notebooks to", CODE)
