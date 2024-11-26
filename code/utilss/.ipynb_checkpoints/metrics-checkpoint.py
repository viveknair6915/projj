import numpy as np

def calculate_rmse(y_true, y_pred):
    """
    Calculate Root Mean Squared Error (RMSE).

    Args:
        y_true (array-like): Ground truth values.
        y_pred (array-like): Predicted values.

    Returns:
        float: RMSE value.
    """
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

def calculate_mae(y_true, y_pred):
    """
    Calculate Mean Absolute Error (MAE).

    Args:
        y_true (array-like): Ground truth values.
        y_pred (array-like): Predicted values.

    Returns:
        float: MAE value.
    """
    return np.mean(np.abs(y_true - y_pred))
