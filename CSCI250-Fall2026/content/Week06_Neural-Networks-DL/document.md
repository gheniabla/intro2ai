# Week 6 — Neural Networks & Deep Learning Foundations
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of September 28, 2026 · Online / Asynchronous*

---

## Learning objectives
By the end of this week you will be able to:
1. Explain the **perceptron** and how stacking neurons into **layers** builds a neural network.
2. Describe the role of **activation functions** (ReLU, sigmoid, softmax) and why nonlinearity matters.
3. Define a **loss function** and explain how **gradient descent** and **backpropagation** train a network (intuition first, math second).
4. Build and train a **tiny neural network** on a simple dataset using PyTorch (with a NumPy fallback).
5. Take a guided tour of **convolutional networks** (vision) and **sequence models**, and see why this all is **the foundation under LLMs**.

> **Time budget:** ~10 hours this week (lecture + slides + videos + two notebooks + **Lab A6**). Absorb the deep-learning fundamentals here — they're the foundation under the LLM weeks and fair game on the Week 7 midterm.

---

## 1. Why this week is the hinge of the course
For five weeks we did "classic" machine learning with scikit-learn: linear/logistic regression, k-NN, decision trees. Those models are powerful, but they mostly draw **straight (or simple) decision boundaries** and need you to hand-design features.

**Deep learning** changes the game. A neural network *learns its own features* by stacking simple units into many layers. The same core idea — neurons, layers, activations, a loss, and gradient descent — scales all the way up to the **Large Language Models** (Claude, Gemini, Llama) we spend the rest of the semester using. When you hear "billions of parameters," those parameters are exactly the **weights** you will meet this week, just *a lot* more of them.

So: **everything in this week is the foundation under LLMs.** Master the small picture now and the big picture later will make sense.

---

## 2. The perceptron — one neuron
A single artificial neuron takes inputs `x`, multiplies each by a **weight** `w`, adds a **bias** `b`, and passes the sum through an **activation** function:

```
z = w1*x1 + w2*x2 + ... + wn*xn + b   # weighted sum (a dot product)
a = activation(z)                      # the neuron's output
```

In vector form this is just `z = w · x + b`. The weights say *how much each input matters*; the bias shifts the threshold. **Learning = finding good weights and biases.**

```python
import numpy as np

def neuron(x, w, b):
    z = np.dot(w, x) + b
    return 1 / (1 + np.exp(-z))   # sigmoid activation

print(neuron(np.array([1.0, 2.0]), w=np.array([0.5, -0.3]), b=0.1))
```

A single perceptron can only separate data with a straight line. Real problems (like XOR, or recognizing a digit) need **many neurons in many layers**.

---

## 3. Layers — stacking neurons
A **layer** is a group of neurons that all see the same inputs. We chain layers:

- **Input layer** — your raw features (e.g., 784 pixels of a digit image).
- **Hidden layers** — where features are *learned*; "deep" learning just means several hidden layers.
- **Output layer** — produces the prediction (one number for regression, one-per-class for classification).

A "fully connected" (dense) layer is a matrix multiply plus a bias, then an activation:

```
H = activation(X @ W + b)   # X: inputs, W: weight matrix, b: bias vector
```

Stacking these is what lets the network bend its decision boundary into any shape.

---

## 4. Activation functions — where the power comes from
Without a nonlinear activation, stacking layers collapses into a single linear layer (a line of lines is still a line). Activations add the **nonlinearity** that makes deep networks expressive.

| Activation | Formula | Where used |
|---|---|---|
| **ReLU** | `max(0, z)` | default for hidden layers — fast, avoids vanishing gradients |
| **Sigmoid** | `1 / (1 + e^-z)` | squashes to (0, 1) — binary output / probabilities |
| **Softmax** | `e^z_i / Σ e^z_j` | output layer for **multi-class** — turns scores into a probability distribution |

```python
def relu(z):    return np.maximum(0, z)
def sigmoid(z): return 1 / (1 + np.exp(-z))
def softmax(z):
    e = np.exp(z - z.max())     # subtract max for numerical stability
    return e / e.sum()
```

> The same **softmax** that picks a class here is what an LLM uses to pick the **next token** from its vocabulary.

---

## 5. Loss — measuring how wrong we are
The **loss function** turns "how good is this prediction?" into a single number we want to **minimize**.

- **Mean Squared Error (MSE)** — for regression: `mean((y_pred - y_true)^2)`.
- **Cross-entropy** — for classification: penalizes confident wrong answers heavily; pairs naturally with softmax/sigmoid.

```python
def mse(y_pred, y_true):
    return np.mean((y_pred - y_true) ** 2)

def binary_cross_entropy(p, y):
    p = np.clip(p, 1e-9, 1 - 1e-9)   # avoid log(0)
    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
```

Training an LLM is, at heart, minimizing the cross-entropy of predicting the next token over trillions of examples.

---

## 6. Gradient descent — how the network learns
We want the weights that make the loss smallest. **Gradient descent** is the recipe:

1. Make a prediction; compute the loss.
2. Compute the **gradient** — the direction in weight-space that *increases* loss fastest.
3. Step the weights a little in the **opposite** direction.
4. Repeat.

```
w  <-  w - learning_rate * gradient
```

The **learning rate** controls step size: too big and you overshoot; too small and training crawls. One pass over all the data is an **epoch**; in practice we update on small **batches** (mini-batch / stochastic gradient descent).

Think of the loss as a hilly landscape and the network as a hiker in fog, always stepping downhill.

---

## 7. Backpropagation — gradients, efficiently
**Backpropagation** is just the **chain rule** from calculus, applied layer by layer from the output back to the input. It computes every weight's share of the blame for the loss in one efficient backward pass.

You almost never write backprop by hand — frameworks like **PyTorch** do **automatic differentiation** (autograd) for you. Intuition to keep:

- **Forward pass:** inputs flow forward, producing a prediction and a loss.
- **Backward pass:** the error flows backward, producing a gradient for every weight.
- The optimizer (e.g., SGD, Adam) then nudges every weight.

That's the entire training loop, whether the network has 50 parameters or 50 billion.

---

## 8. Build a tiny network (PyTorch, with a NumPy fallback)
This week's first notebook (`code/01_tiny_neural_net.ipynb`) builds a 2-layer classifier on a simple **moons** dataset:

```python
import torch, torch.nn as nn

model = nn.Sequential(
    nn.Linear(2, 16), nn.ReLU(),     # hidden layer with ReLU
    nn.Linear(16, 2),                # 2-class output (logits -> softmax in the loss)
)
loss_fn = nn.CrossEntropyLoss()
opt = torch.optim.Adam(model.parameters(), lr=0.05)

for epoch in range(200):             # the training loop
    opt.zero_grad()
    logits = model(X)                # forward
    loss = loss_fn(logits, y)
    loss.backward()                  # backprop (autograd)
    opt.step()                       # gradient-descent update
```

If `torch` will not import (some Colab/local setups), the notebook falls back to a **from-scratch NumPy network** so you can still see the forward/backward loop with your own eyes. Same five ideas, no magic.

---

## 9. A quick tour: vision (CNNs) and sequences
Dense layers treat every input independently. Two specialized architectures add useful structure:

- **Convolutional Neural Networks (CNNs)** — for **images**. A small filter slides across the image detecting edges, then textures, then shapes. This *weight sharing* makes vision practical. (Notebook 2 shows the convolution idea on a tiny image.)
- **Sequence models** — for **ordered data** (text, audio, time series). **RNNs/LSTMs** read one step at a time; the **Transformer** (2017) reads the whole sequence at once using **attention**, and is the architecture behind every modern LLM.

You do not need to master CNNs or Transformers this week — just recognize them as *the same neurons-layers-activations-loss-gradient-descent machinery* arranged for a particular kind of data.

---

## 10. The bridge to LLMs
Put it together and you can read the LLM story:

- An LLM is a **very deep neural network** (a Transformer) with billions of **weights**.
- It is trained by **gradient descent + backprop** to **minimize cross-entropy** on next-token prediction.
- Its final **softmax** layer turns scores over the vocabulary into the probability of each possible next token; **temperature** (Week 8) reshapes that distribution.

Every term in those three sentences is something you learned this week. That is why we frame Week 6 as the foundation under everything that follows.

---

## 11. Reading & videos
- *Machine Learning Systems* (mlsysbook.ai) — the deep-learning primer chapter.
- 3Blue1Brown, **"But what is a neural network?"** (YouTube) — the best visual intuition; watch chapters 1–4.
- PyTorch **"Learn the Basics"** tutorial (pytorch.org) — skim the *Build the Neural Network* and *Optimization* pages.
- Optional: Andrej Karpathy, **"The spelled-out intro to neural networks and backpropagation"** (micrograd).

---

## 12. Lab — Assignment A6 (6 pts · due Sunday Oct 4, 11:59 PM PT)
**Goal:** build, train, and evaluate a **tiny neural network**, watch the **loss go down** as it learns, and connect the pieces (neurons, layers, activations, loss, gradient descent) to the foundation under modern LLMs. Full spec and rubric: `assignments/A6.md`.

This week's two notebooks map directly to the A6 tasks:
1. **Train the net (`code/01_tiny_neural_net.ipynb`).** Run the **two-moons** dataset and train the network (Section 2a PyTorch, or the **2b NumPy fallback** if you can't install PyTorch). Report the **final test accuracy**.
2. **Watch it learn.** Run Section 3 and include the **loss curve**; in 2–3 sentences explain what the falling curve means and what the **learning rate** controls.
3. **Experiment (Section 4).** Change **one** thing — hidden units, learning rate, or epochs — re-train, and report how test accuracy and the loss curve changed (helped or hurt?).
4. **Activations matter.** In your own words (2–3 sentences), explain why a network needs a **nonlinear** activation (e.g., ReLU) — what happens if you stack linear layers with no activation?
5. **Tour & connect (`code/02_cnn_and_sequence_tour.ipynb`).** Skim it and write one sentence on how the **softmax** that picks a class here relates to how an LLM picks the **next token**.
6. **Stretch:** Run a second experiment (a different knob) and briefly compare which setting generalized best.

**Submit on Canvas:** the completed `01_tiny_neural_net.ipynb` (and your notes from `02_...`) with outputs and the loss curve visible, your final accuracy, loss-curve explanation, experiment result, activation explanation, stretch comparison, and a one-line **AI-Use** note. Correctness-graded — you may revise once after feedback. (If PyTorch won't install, use the NumPy fallback and document any blockers — effort counts.)

These fundamentals are also fair game on the **Week 7 midterm** (Oct 11).

---

## Key terms
**neuron / perceptron**, **weight**, **bias**, **layer (input/hidden/output)**, **activation (ReLU, sigmoid, softmax)**, **nonlinearity**, **loss (MSE, cross-entropy)**, **gradient descent**, **learning rate**, **epoch / batch**, **backpropagation**, **autograd**, **CNN / convolution**, **RNN / Transformer / attention**, **parameter**.
