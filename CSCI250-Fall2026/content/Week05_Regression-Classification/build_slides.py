"""Build slides.pptx for Week 5. Run: python build_slides.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
from slidegen import build_deck

slides = [
    {"type": "title", "title": "Week 5 — Regression & Classification",
     "subtitle": "CSCI 250 — Introduction to Artificial Intelligence · Fall 2026"},

    {"type": "bullets", "title": "This Week", "bullets": [
        "Regression (predict a number) + its error metrics",
        "Classification: logistic regression, k-NN, decision trees",
        "Metrics that matter: precision, recall, F1, confusion matrix",
        "Train / validation / test, overfitting & regularization",
        ("Lab: Assignment A5 — train, evaluate, compare models", 1)]},

    {"type": "section", "title": "Regression — Predicting a Number"},
    {"type": "code", "title": "Linear Regression + Metrics",
     "code": "from sklearn.linear_model import LinearRegression\n"
             "from sklearn.metrics import (mean_absolute_error,\n"
             "    root_mean_squared_error, r2_score)\n\n"
             "reg = LinearRegression().fit(X_train, y_train)\n"
             "p = reg.predict(X_test)\n"
             "print('MAE :', mean_absolute_error(y_test, p))\n"
             "print('RMSE:', root_mean_squared_error(y_test, p))\n"
             "print('R^2 :', r2_score(y_test, p))",
     "caption": "MAE = avg miss · RMSE punishes big misses · R² = variance explained"},
    {"type": "two_col", "title": "Reading Regression Error",
     "left_title": "MAE",
     "left": ["Average absolute miss", "Same units as y", "Easy to explain"],
     "right_title": "RMSE",
     "right": ["Squares errors first", "Punishes big misses", "RMSE ≥ MAE always"]},

    {"type": "section", "title": "Classification — Predicting a Category"},
    {"type": "two_col", "title": "Three Workhorse Classifiers",
     "left_title": "Linear baseline",
     "left": ["Logistic regression",
              "Outputs class probabilities",
              "Strong, fast, interpretable"],
     "right_title": "Instance & rule based",
     "right": ["k-NN: vote of k neighbors",
               "Decision tree: yes/no flowchart",
               "Trees overfit if too deep"]},

    {"type": "bullets", "title": "When Accuracy Lies", "bullets": [
        "Accuracy = fraction correct — fine only if classes are balanced",
        "99% not-spam? 'always not-spam' = 99% accurate and useless",
        "Precision = of flagged positives, how many were right",
        "Recall = of actual positives, how many we caught",
        ("F1 = harmonic mean of precision & recall (one number)", 1)]},
    {"type": "code", "title": "Classifier Metrics in sklearn",
     "code": "from sklearn.metrics import (classification_report,\n"
             "                             confusion_matrix)\n\n"
             "clf.fit(X_train, y_train)\n"
             "p = clf.predict(X_test)\n"
             "print(classification_report(y_test, p))\n"
             "print(confusion_matrix(y_test, p))",
     "caption": "Confusion matrix shows WHICH classes get confused — not just how many"},

    {"type": "section", "title": "Generalization: Train / Val / Test"},
    {"type": "bullets", "title": "Three Splits, One Rule", "bullets": [
        "Train — fit the model",
        "Validation — tune model & hyperparameters",
        "Test — touched ONCE, at the end, for an honest score",
        ("Small data? Use cross_val_score(model, X, y, cv=5) instead", 1)]},
    {"type": "two_col", "title": "Overfit vs Underfit",
     "left_title": "Overfitting",
     "left": ["Memorizes training noise",
              "Great on train, poor on test",
              "Big train↔test gap"],
     "right_title": "Underfitting",
     "right": ["Too simple for the pattern",
               "Poor on BOTH train & test",
               "e.g. a line for a curve"]},
    {"type": "code", "title": "Regularization Fights Overfitting",
     "code": "# smaller C = stronger regularization\n"
             "LogisticRegression(C=0.1)\n\n"
             "# shallower tree = less overfitting\n"
             "DecisionTreeClassifier(max_depth=3)\n\n"
             "# larger k = smoother boundary\n"
             "KNeighborsClassifier(n_neighbors=15)",
     "caption": "Tune for the train↔test GAP, not just the raw score"},

    {"type": "closing", "title": "This Week — To Do", "bullets": [
        "Read sklearn 'Supervised learning' + 'Model evaluation'",
        "Run 01_regression.ipynb (MAE / RMSE / R², Ridge)",
        "Run 02_classification.ipynb (logreg, k-NN, tree + metrics)",
        "Do the overfitting study (vary tree max_depth)",
        "Submit Lab A5 by Sunday 11:59 PM PT"]},
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "slides.pptx")
    build_deck(slides, out)
    print("wrote", out)
