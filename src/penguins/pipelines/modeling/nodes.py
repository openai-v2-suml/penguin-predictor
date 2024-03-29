"""Nodes for the modeling pipeline."""
from typing import Tuple

import mlflow
import pandas as pd
from autogluon.tabular import TabularPredictor
from sklearn.model_selection import train_test_split


def split_data(data: pd.DataFrame) -> Tuple:
    """Split data into train and test sets."""
    train, test = train_test_split(data, test_size=0.2)
    return train, test


def train_model(train: pd.DataFrame, test: pd.DataFrame) -> TabularPredictor:
    """Train a model on the given data."""
    mlflow.set_experiment("penguins")
    classificator = TabularPredictor(label="species", log_to_file=False, problem_type="multiclass",
                                     eval_metric="accuracy")
    classificator.fit(train, time_limit=120)
    classificator.evaluate(test)
    for key, value in classificator.fit_summary()["model_performance"].items():
        mlflow.log_metric(f"{key}_accuracy", value)
    return classificator
