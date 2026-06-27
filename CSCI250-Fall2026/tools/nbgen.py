"""
nbgen.py — tiny Jupyter notebook builder for CSCI 250 sample code.

Build a .ipynb from a flat list of (kind, text) tuples where kind is
"md" (markdown) or "code". Keeps all weekly notebooks consistent and avoids
hand-writing notebook JSON.

    from nbgen import build_notebook
    build_notebook([
        ("md",   "# Week 1 — Python Review\nCSCI 250, Fall 2026"),
        ("code", "print('hello, AI')"),
    ], "code/01_python_review.ipynb")
"""
import json


def build_notebook(cells, outpath, kernel="python3"):
    nb = {
        "cells": [],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": kernel},
            "language_info": {"name": "python", "version": "3.11"},
            "colab": {"provenance": []},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    for kind, text in cells:
        src = text.split("\n")
        src = [ln + "\n" for ln in src[:-1]] + [src[-1]] if src else [""]
        if kind == "md":
            nb["cells"].append({"cell_type": "markdown", "metadata": {}, "source": src})
        elif kind == "code":
            nb["cells"].append({
                "cell_type": "code", "metadata": {}, "execution_count": None,
                "outputs": [], "source": src,
            })
        else:
            raise ValueError(f"Unknown cell kind: {kind}")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    return outpath


if __name__ == "__main__":
    build_notebook([("md", "# Self-test"), ("code", "print('ok')")], "_selftest.ipynb")
    print("wrote _selftest.ipynb")
