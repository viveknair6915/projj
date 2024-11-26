import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def calculate_metrics(y_true, y_pred):
    """
    Calculates evaluation metrics: RMSE, MAE, and R².
    """
    return {
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "MAE": mean_absolute_error(y_true, y_pred),
        "R²": r2_score(y_true, y_pred)
    }

def get_feature_importance(data, model_name, dataset_type):
    """
    Computes feature importance for the selected model and dataset type.
    Parameters:
    - data: pd.DataFrame, the dataset to compute feature importance for.
    - model_name: str, name of the selected model.
    - dataset_type: str, type of dataset ('Original' or 'New').

    Returns:
    - pd.DataFrame with feature names and importance scores.
    """
    # Drop non-predictive columns based on dataset type
    if dataset_type == "Original":
        features = data.columns.drop(["Date", "cases_total"], errors="ignore")
    else:  # For new dataset
        features = data.columns.drop(["Year"], errors="ignore")

    # Generate mock importance values as placeholders
    importance_scores = np.random.rand(len(features))
    
    return pd.DataFrame({"Feature": features, "Importance": importance_scores})

