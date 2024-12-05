from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# from ragas import evaluate
# from ragas.embeddings import LangchainEmbeddingsWrapper
# from ragas.llms import LangchainLLMWrapper
# from ragas.metrics import answer_relevancy, faithfulness, context_recall, context_precision
from dotenv import load_dotenv
import os

# from datasets import Dataset
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import time
from pathlib import Path

from difflib import get_close_matches

diagnosis_label_key = {
    0: "Barretts Esophagus or esophageal cell changes",
    1: "Chronic Non-Steroidal Anti Inflammatory (NSAID) use or GI prophylaxis NSAID use",
    2: "Severe esophagitis including bleeding esophagitis or esophageal ulcer",
    3: "History of gastrointestinal bleeding, gastric ulcer, upper GI bleed, or peptic ulcer hemorrhage",
    4: "Peptic Ulcer Disease or Gastroduodenal ulcer treated for 2 - 12 weeks caused from H Pylori infection or NSAID use without bleeding",
    5: "Upper GI Symptoms such as reflux, difficulty swallowing, nausea, or vomiting without endoscopy - asymptomatic for 3 consecutive days",
    6: "ICU Stress Ulcer Prophylaxis",
    7: "Completed Heliobacter Pylori (H. Pylori) infection treated for 14 days with combination therapy",
    8: "Mild to moderate esophagitis or esophageal inflammation",
    9: "Treated Gastroesophageal Reflux Disease (GERD) or reflux symptoms such as acid reflux, heartburn, or regurgitation",
    10: "No clear evidence found. Lack of evidence",
}


def get_best_diagnosis_match(reasoning):
    # Extract the diagnosis labels from the dictionary
    labels = list(diagnosis_label_key.values())
    # Use fuzzy matching to find the best match
    best_match = get_close_matches(reasoning, labels, n=1, cutoff=0.1)
    matched_key = None  # Initialize matched_key to None
    if best_match:  # Check if best_match is not empty
        matched_key = list(diagnosis_label_key.keys())[
            list(diagnosis_label_key.values()).index(best_match[0])
        ]

    return matched_key, best_match[0]  # Return the matched key and label


def evaluate_multiclass_classification(y_true, y_pred, class_labels):
    """
    Evaluates a multiclass classification model.

    y_true: Ground truth labels
    y_pred: Predicted labels from the classifier
    class_labels: List of class names

    Returns a dictionary of accuracy, precision, recall, F1, and confusion matrix.
    """

    # Accuracy
    accuracy = accuracy_score(y_true, y_pred)

    # Precision, Recall, F1-score
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="macro"
    )  # macro-averaging

    # Classification report (optional detailed breakdown for each class)
    class_report = classification_report(y_true, y_pred, target_names=class_labels)

    # Confusion Matrix
    conf_matrix = confusion_matrix(y_true, y_pred)

    # Print evaluation metrics
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision (Macro Avg): {precision:.4f}")
    print(f"Recall (Macro Avg): {recall:.4f}")
    print(f"F1 Score (Macro Avg): {f1:.4f}")
    print("\nClassification Report:\n", class_report)

    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        conf_matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_labels,
        yticklabels=class_labels,
    )
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.title("Confusion Matrix")
    plt.show()

    # Return metrics for further analysis if needed
    return {
        "accuracy": accuracy,
        "precision_macro": precision,
        "recall_macro": recall,
        "f1_macro": f1,
        "confusion_matrix": conf_matrix,
    }
