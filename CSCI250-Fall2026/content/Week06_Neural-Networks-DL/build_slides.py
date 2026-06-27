"""Build slides.pptx for Week 6. Run: python build_slides.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from slidegen import build_deck

slides = [
    {"type": "title", "title": "Week 6 — Neural Networks & Deep Learning Foundations",
     "subtitle": "CSCI 250 — Introduction to Artificial Intelligence · Fall 2026"},

    {"type": "bullets", "title": "This Week", "bullets": [
        "From classic ML to deep learning: neurons → layers",
        "Activations (ReLU / sigmoid / softmax) and why nonlinearity matters",
        "Loss, gradient descent, and backprop — intuition first",
        "Build & train a tiny network (PyTorch, NumPy fallback)",
        "Brief tour: vision (CNNs) + sequences (Transformers)",
        ("Framing: this is the foundation under LLMs", 1),
        ("No assignment — absorb fundamentals before the Week 7 midterm", 1)]},

    {"type": "section", "title": "One Neuron: The Perceptron"},
    {"type": "code", "title": "A Single Neuron",
     "code": "import numpy as np\n\n"
             "def neuron(x, w, b):\n"
             "    z = np.dot(w, x) + b        # weighted sum = w·x + b\n"
             "    return 1 / (1 + np.exp(-z)) # sigmoid activation\n\n"
             "neuron(np.array([1.0, 2.0]), w=np.array([0.5, -0.3]), b=0.1)",
     "caption": "Weights say how much each input matters; learning = finding good w and b"},
    {"type": "bullets", "title": "Layers — Stacking Neurons", "bullets": [
        "Input layer — your raw features (e.g., 784 pixels)",
        "Hidden layers — where features are LEARNED ('deep' = several)",
        "Output layer — the prediction",
        ("A dense layer is just:  H = activation(X @ W + b)", 1),
        ("Stacking bends the decision boundary into any shape", 1)]},

    {"type": "section", "title": "Activations, Loss & Learning"},
    {"type": "two_col", "title": "Activation Functions",
     "left_title": "Hidden layers",
     "left": ["ReLU: max(0, z)", "fast, avoids vanishing gradients", "the default choice"],
     "right_title": "Output layers",
     "right": ["sigmoid → (0,1) probability", "softmax → class distribution",
               "same softmax picks an LLM's next token"]},
    {"type": "code", "title": "Loss — How Wrong Are We?",
     "code": "def mse(y_pred, y_true):          # regression\n"
             "    return np.mean((y_pred - y_true) ** 2)\n\n"
             "def bce(p, y):                   # binary classification\n"
             "    p = np.clip(p, 1e-9, 1 - 1e-9)\n"
             "    return -np.mean(y*np.log(p) + (1-y)*np.log(1-p))",
     "caption": "Training an LLM = minimizing cross-entropy of next-token prediction"},
    {"type": "bullets", "title": "Gradient Descent + Backprop", "bullets": [
        "Predict → compute loss → find the gradient → step downhill",
        "Update rule:  w  ←  w − learning_rate × gradient",
        "Learning rate: too big overshoots, too small crawls",
        ("Backprop = chain rule, output → input, in one backward pass", 1),
        ("Frameworks (PyTorch autograd) compute gradients for you", 1)]},

    {"type": "section", "title": "Build It & Scale It"},
    {"type": "code", "title": "A Tiny Network in PyTorch",
     "code": "model = nn.Sequential(\n"
             "    nn.Linear(2, 16), nn.ReLU(),   # hidden layer\n"
             "    nn.Linear(16, 2),              # 2-class output\n"
             ")\n"
             "for epoch in range(200):           # the training loop\n"
             "    opt.zero_grad()\n"
             "    loss = loss_fn(model(X), y)    # forward\n"
             "    loss.backward()                # backprop\n"
             "    opt.step()                     # gradient step",
     "caption": "NumPy from-scratch fallback in the notebook if torch won't import",
     "code_size": 14},
    {"type": "two_col", "title": "A Quick Tour Beyond Dense Nets",
     "left_title": "Vision — CNNs",
     "left": ["A small filter slides over the image", "Detects edges → textures → shapes",
              "Weight sharing makes vision practical"],
     "right_title": "Sequences",
     "right": ["RNN/LSTM read one step at a time", "Transformer reads all at once (attention)",
               "The architecture behind every LLM"]},
    {"type": "bullets", "title": "The Bridge to LLMs", "bullets": [
        "An LLM is a very deep Transformer with billions of WEIGHTS",
        "Trained by gradient descent + backprop on next-token prediction",
        "Final softmax → probability of each possible next token",
        ("Every term here you learned this week — that's the point", 1)]},

    {"type": "closing", "title": "This Week — To Do", "bullets": [
        "Read the document + watch 3Blue1Brown's neural-network series",
        "Run 01_tiny_neural_net.ipynb and watch the loss fall",
        "Tweak learning rate / hidden size / epochs and observe",
        "Run 02_cnn_and_sequence_tour.ipynb",
        "No assignment — start reviewing Weeks 1–5 for the midterm"]},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "slides.pptx")
    build_deck(slides, out)
    print("wrote", out)
