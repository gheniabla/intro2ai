"""Build Week 6 sample-code notebooks. Run: python build_code.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from nbgen import build_notebook

HERE = os.path.dirname(__file__)
CODE = os.path.join(HERE, "code")
os.makedirs(CODE, exist_ok=True)

# ---------------------------------------------------------------- notebook 1
tiny_net = [
    ("md", "# Week 6 · Notebook 1 — Build a Tiny Neural Network\n"
           "**CSCI 250 — Introduction to Artificial Intelligence · Fall 2026**\n\n"
           "We train a small 2-layer classifier on a simple **two-moons** dataset and "
           "watch the loss go down. This is the exact machinery — neurons, layers, "
           "activations, loss, gradient descent, backprop — that scales up to LLMs.\n\n"
           "> **Runs in Colab.** If PyTorch will not import we fall back to a "
           "from-scratch **NumPy** network so you still see the forward/backward loop."),

    ("md", "## 0. Setup\n"
           "PyTorch is preinstalled in Colab. The import is guarded so this notebook "
           "still runs (NumPy fallback) if torch is unavailable."),
    ("code", "import numpy as np\n"
             "try:\n"
             "    import torch\n"
             "    import torch.nn as nn\n"
             "    HAS_TORCH = True\n"
             "    print('PyTorch', torch.__version__, '— using PyTorch path')\n"
             "except Exception as e:\n"
             "    HAS_TORCH = False\n"
             "    print('PyTorch not available -> NumPy fallback. (', e, ')')"),

    ("md", "## 1. A simple dataset (two interleaving moons)\n"
           "Two classes that a straight line *cannot* separate — so we need a hidden "
           "layer with a nonlinear activation. We make the data with plain NumPy so "
           "there are no extra dependencies."),
    ("code", "rng = np.random.default_rng(0)\n\n"
             "def make_moons(n=400, noise=0.20):\n"
             "    n2 = n // 2\n"
             "    t = np.linspace(0, np.pi, n2)\n"
             "    # outer moon\n"
             "    x0 = np.c_[np.cos(t), np.sin(t)]\n"
             "    # inner moon, shifted\n"
             "    x1 = np.c_[1 - np.cos(t), 0.5 - np.sin(t)]\n"
             "    X = np.vstack([x0, x1]) + noise * rng.standard_normal((2 * n2, 2))\n"
             "    y = np.r_[np.zeros(n2), np.ones(n2)].astype(int)\n"
             "    idx = rng.permutation(len(y))\n"
             "    return X[idx].astype('float32'), y[idx]\n\n"
             "X, y = make_moons()\n"
             "print('X', X.shape, 'y', y.shape, 'classes', np.unique(y))"),
    ("code", "import matplotlib.pyplot as plt\n"
             "plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', s=12)\n"
             "plt.title('Two moons — not linearly separable'); plt.show()"),

    ("md", "## 2a. Train with PyTorch\n"
           "A `Sequential` model = a hidden `Linear` layer + `ReLU`, then a 2-class "
           "output. `CrossEntropyLoss` applies softmax internally. The loop is the "
           "universal recipe: **forward → loss → backward (backprop) → step**."),
    ("code", "def train_torch(X, y, hidden=16, lr=0.05, epochs=200):\n"
             "    Xt = torch.tensor(X)\n"
             "    yt = torch.tensor(y, dtype=torch.long)\n"
             "    model = nn.Sequential(\n"
             "        nn.Linear(2, hidden), nn.ReLU(),\n"
             "        nn.Linear(hidden, 2),\n"
             "    )\n"
             "    loss_fn = nn.CrossEntropyLoss()\n"
             "    opt = torch.optim.Adam(model.parameters(), lr=lr)\n"
             "    history = []\n"
             "    for epoch in range(epochs):\n"
             "        opt.zero_grad()\n"
             "        logits = model(Xt)         # forward\n"
             "        loss = loss_fn(logits, yt)\n"
             "        loss.backward()            # backprop (autograd)\n"
             "        opt.step()                 # gradient-descent update\n"
             "        history.append(loss.item())\n"
             "    acc = (model(Xt).argmax(1) == yt).float().mean().item()\n"
             "    return model, history, acc\n\n"
             "if HAS_TORCH:\n"
             "    model, history, acc = train_torch(X, y)\n"
             "    print(f'final loss={history[-1]:.4f}  train accuracy={acc:.2%}')"),

    ("md", "## 2b. NumPy fallback — the same network, by hand\n"
           "If torch is missing, we implement one hidden layer + ReLU + softmax and "
           "**code the backward pass ourselves** so you can see every gradient. Same "
           "five ideas, no framework."),
    ("code", "def softmax(z):\n"
             "    z = z - z.max(axis=1, keepdims=True)\n"
             "    e = np.exp(z)\n"
             "    return e / e.sum(axis=1, keepdims=True)\n\n"
             "def train_numpy(X, y, hidden=16, lr=0.1, epochs=400):\n"
             "    n, d = X.shape; K = 2\n"
             "    W1 = 0.5 * rng.standard_normal((d, hidden)); b1 = np.zeros(hidden)\n"
             "    W2 = 0.5 * rng.standard_normal((hidden, K)); b2 = np.zeros(K)\n"
             "    Y = np.eye(K)[y]                      # one-hot targets\n"
             "    history = []\n"
             "    for epoch in range(epochs):\n"
             "        # ---- forward ----\n"
             "        Z1 = X @ W1 + b1; A1 = np.maximum(0, Z1)   # ReLU\n"
             "        Z2 = A1 @ W2 + b2; P = softmax(Z2)\n"
             "        loss = -np.mean(np.sum(Y * np.log(P + 1e-9), axis=1))\n"
             "        history.append(loss)\n"
             "        # ---- backward (chain rule) ----\n"
             "        dZ2 = (P - Y) / n\n"
             "        dW2 = A1.T @ dZ2; db2 = dZ2.sum(0)\n"
             "        dA1 = dZ2 @ W2.T; dZ1 = dA1 * (Z1 > 0)     # ReLU grad\n"
             "        dW1 = X.T @ dZ1; db1 = dZ1.sum(0)\n"
             "        # ---- gradient-descent update ----\n"
             "        W1 -= lr * dW1; b1 -= lr * db1\n"
             "        W2 -= lr * dW2; b2 -= lr * db2\n"
             "    acc = (softmax((np.maximum(0, X @ W1 + b1)) @ W2 + b2).argmax(1) == y).mean()\n"
             "    return (W1, b1, W2, b2), history, acc\n\n"
             "if not HAS_TORCH:\n"
             "    params, history, acc = train_numpy(X, y)\n"
             "    print(f'final loss={history[-1]:.4f}  train accuracy={acc:.2%}')"),

    ("md", "## 3. Watch the loss go down\n"
           "Whichever path ran, `history` holds the loss at every epoch. A falling "
           "curve means gradient descent is working."),
    ("code", "plt.plot(history)\n"
             "plt.xlabel('epoch'); plt.ylabel('loss')\n"
             "plt.title('Training loss — gradient descent at work'); plt.show()"),

    ("md", "## 4. Experiment (do this for the midterm prep)\n"
           "Rerun training while changing one thing at a time and note the effect:\n"
           "1. **Learning rate** — try 0.001, 0.05, 0.5. What breaks?\n"
           "2. **Hidden size** — try 2, 8, 64. Does accuracy change?\n"
           "3. **Epochs** — too few = underfit; very many = does it help?\n\n"
           "Write 3–4 sentences on what you observed."),
    ("code", "# Your experiments here\n"),
]
build_notebook(tiny_net, os.path.join(CODE, "01_tiny_neural_net.ipynb"))

# ---------------------------------------------------------------- notebook 2
tour = [
    ("md", "# Week 6 · Notebook 2 — CNNs & Sequences: A Quick Tour\n"
           "**CSCI 250 · Fall 2026**\n\n"
           "Dense layers treat every input independently. Two specialized ideas add "
           "structure: **convolution** for images and **sequence models** for ordered "
           "data (the lineage that leads to the Transformer behind every LLM).\n\n"
           "> No training here — just intuition you can run."),

    ("md", "## 1. Convolution: a filter sliding over an image\n"
           "A CNN learns small **filters** that slide across an image. Here we apply a "
           "fixed *vertical-edge* filter to a tiny synthetic image and see it light up "
           "the edge — exactly what a CNN's first layer learns to do."),
    ("code", "import numpy as np\n"
             "import matplotlib.pyplot as plt\n\n"
             "# tiny 8x8 image: left half dark, right half bright (a vertical edge)\n"
             "img = np.zeros((8, 8)); img[:, 4:] = 1.0\n\n"
             "# a 3x3 vertical-edge detector (Sobel-like)\n"
             "kernel = np.array([[-1, 0, 1],\n"
             "                   [-2, 0, 2],\n"
             "                   [-1, 0, 1]], dtype=float)\n\n"
             "def convolve2d(x, k):\n"
             "    kh, kw = k.shape\n"
             "    out = np.zeros((x.shape[0]-kh+1, x.shape[1]-kw+1))\n"
             "    for i in range(out.shape[0]):\n"
             "        for j in range(out.shape[1]):\n"
             "            out[i, j] = np.sum(x[i:i+kh, j:j+kw] * k)\n"
             "    return out\n\n"
             "feat = convolve2d(img, kernel)\n"
             "fig, ax = plt.subplots(1, 2, figsize=(7, 3))\n"
             "ax[0].imshow(img, cmap='gray'); ax[0].set_title('input image')\n"
             "ax[1].imshow(np.abs(feat), cmap='magma'); ax[1].set_title('edge feature map')\n"
             "plt.show()"),
    ("md", "The filter responds strongly right where the edge is. Stack many such "
           "filters across many layers and a CNN goes from edges → textures → objects. "
           "**Same neurons/weights, arranged to share parameters across the image.**"),

    ("md", "## 2. Sequences: predicting the next item\n"
           "Sequence models read ordered data one step at a time (RNN/LSTM) or all at "
           "once (Transformer). The training objective is the heart of an LLM: **given "
           "what came before, predict the next item.** Here is that objective on a toy "
           "number sequence using a simple frequency table — no deep net needed to see "
           "the idea."),
    ("code", "seq = list('AABABBAABABBAABABB')   # a repeating pattern\n"
             "from collections import defaultdict, Counter\n"
             "nxt = defaultdict(Counter)\n"
             "for a, b in zip(seq, seq[1:]):\n"
             "    nxt[a][b] += 1\n\n"
             "def predict_next(prev):\n"
             "    counts = nxt[prev]\n"
             "    total = sum(counts.values())\n"
             "    return {k: round(v/total, 2) for k, v in counts.items()}\n\n"
             "for c in 'AB':\n"
             "    print(f\"after '{c}'  -> next-item probabilities {predict_next(c)}\")"),
    ("md", "Those probabilities are a baby version of an LLM's **softmax over the "
           "vocabulary**. A real Transformer conditions on the *whole* context with "
           "**attention** instead of just the previous character — but the goal "
           "(probability of the next token) is identical."),

    ("md", "## 3. Optional: a real CNN layer in PyTorch\n"
           "If torch is available, here is one true `Conv2d` layer applied to our "
           "image — the framework version of the convolution we coded above. Guarded "
           "so the notebook still runs without torch."),
    ("code", "try:\n"
             "    import torch, torch.nn as nn\n"
             "    conv = nn.Conv2d(1, 1, kernel_size=3, bias=False)\n"
             "    with torch.no_grad():\n"
             "        conv.weight.copy_(torch.tensor(kernel).float().view(1, 1, 3, 3))\n"
             "    x = torch.tensor(img).float().view(1, 1, 8, 8)\n"
             "    out = conv(x).detach().numpy()[0, 0]\n"
             "    print('Conv2d output shape:', out.shape)\n"
             "    plt.imshow(np.abs(out), cmap='magma'); plt.title('nn.Conv2d feature map'); plt.show()\n"
             "except Exception as e:\n"
             "    print('PyTorch not available — skipping (the NumPy version above already showed the idea).', e)"),

    ("md", "## Takeaway\n"
           "CNNs and Transformers are not new math — they are the **same neurons, "
           "layers, activations, loss, and gradient descent** from Notebook 1, arranged "
           "for images and sequences. That is the foundation under the LLMs we use for "
           "the rest of CSCI 250."),
]
build_notebook(tour, os.path.join(CODE, "02_cnn_and_sequence_tour.ipynb"))

print("wrote Week 6 notebooks to", CODE)
