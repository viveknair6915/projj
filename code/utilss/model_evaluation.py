import pandas as pd
import matplotlib.pyplot as plt

def evaluate_models(models):
    metrics = []
    for name, path in models.items():
        data = pd.read_csv(path)
        metrics.append({
            "Model": name,
            "RMSE": calculate_rmse(data),
            "MAE": calculate_mae(data),
            "R²": calculate_r2(data),
        })
    return pd.DataFrame(metrics)

def calculate_rmse(data):
    return ((data['actual'] - data['predicted'])**2).mean()**0.5

def calculate_mae(data):
    return abs(data['actual'] - data['predicted']).mean()

def calculate_r2(data):
    actual_mean = data['actual'].mean()
    ss_total = ((data['actual'] - actual_mean)**2).sum()
    ss_residual = ((data['actual'] - data['predicted'])**2).sum()
    return 1 - (ss_residual / ss_total)
