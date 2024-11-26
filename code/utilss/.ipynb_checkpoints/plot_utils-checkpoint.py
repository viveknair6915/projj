import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_temporal_trends(data, column):
    """
    Plots temporal trends for a given column.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    data['Date'] = pd.to_datetime(data['Date'])  # Ensure Date column is datetime
    data.sort_values(by='Date', inplace=True)   # Sort data by date
    ax.plot(data['Date'], data[column], label=column, color='blue')
    ax.set_xlabel("Date")
    ax.set_ylabel(column)
    ax.set_title(f"Temporal Trend for {column}")
    ax.legend()
    return fig

def plot_correlation_matrix(data):
    """
    Plots a correlation matrix heatmap for the selected columns.
    """
    if data.empty:
        raise ValueError("The input data is empty. Ensure it contains numeric columns.")
    
    # Compute correlation
    corr = data.corr()

    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax, cbar=True)
    ax.set_title("Correlation Matrix")
    return fig

def plot_metrics_comparison(results):
    """
    Plots a comparison of model performance metrics.
    """
    metrics_df = pd.DataFrame(results).T
    
    # Visualizing key metrics
    fig, ax = plt.subplots(figsize=(10, 6))
    metrics_df.plot(kind="bar", ax=ax)
    ax.set_title("Model Metrics Comparison")
    ax.set_ylabel("Metric Value")
    ax.set_xlabel("Models")
    plt.xticks(rotation=45)
    return fig

def plot_actual_vs_predicted(original_data, predictions):
    """
    Plots actual vs. predicted values for a model.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(original_data["Date"], original_data["cases_total"], label="Actual", color="blue")
    ax.plot(original_data["Date"], predictions, label="Predicted", color="orange")
    ax.set_title("Actual vs. Predicted")
    ax.legend()
    return fig

def plot_feature_comparison(feature_results, selected_feature):
    """
    Plots a comparison of a selected feature across models.

    Args:
    - feature_results: Dictionary with models as keys and metric values as values.
    - selected_feature: The feature being compared.

    Returns:
    - fig: Matplotlib figure object.
    """
    # Convert results to a DataFrame
    feature_df = pd.DataFrame(list(feature_results.items()), columns=["Model", selected_feature])
    
    # Plot the feature comparison
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(feature_df["Model"], feature_df[selected_feature], color="skyblue")
    ax.set_title(f"Comparison of {selected_feature} Across Models")
    ax.set_ylabel(selected_feature)
    ax.set_xlabel("Models")
    return fig


def plot_department_metrics(model_data, selected_feature):
    """
    Plots department-specific metrics for the selected feature.

    Args:
    - model_data: DataFrame containing department-level data for the selected model.
    - selected_feature: The feature being analyzed.

    Returns:
    - fig: Matplotlib figure object.
    """
    # Group by department and compute mean for the selected feature
    department_data = model_data.groupby("Department")[selected_feature].mean()
    
    # Plot the department-specific metrics
    fig, ax = plt.subplots(figsize=(10, 5))
    department_data.plot(kind="bar", ax=ax, color="orange")
    ax.set_title(f"Department-Wise {selected_feature} Analysis")
    ax.set_ylabel(selected_feature)
    ax.set_xlabel("Department")
    return fig

    

def plot_feature_importance(feature_importance):
    """
    Plots feature importance for a model.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.barplot(
        x="Importance", 
        y="Feature", 
        data=feature_importance.sort_values("Importance", ascending=False),
        ax=ax
    )
    ax.set_title("Feature Importance")
    return fig