import streamlit as st
import pandas as pd
import plotly.express as px

# Page Title
st.title("Model Comparison Across Datasets")

# Sidebar Options
model_files = {
    "LSTM": r"C:\Users\amanp\Desktop\MINOR\projj\code\metrics\Brazil\LSTM_Model_26-11-2024-08-30-12.csv",
    "TCN": r"C:\Users\amanp\Desktop\MINOR\projj\code\metrics\Brazil\TCN_new_model_26-11-2024-08-29-01.csv",
    "CATBOOST": r"C:\Users\amanp\Desktop\MINOR\projj\code\metrics\Brazil\catboost_normal26-11-2024-08-30-30.csv"
}
model_files_search = {
    "LSTM": r"C:\Users\amanp\Desktop\MINOR\projj\code\metrics\Brazil\LSTM_Model_search_26-11-2024-08-10-26.csv",
    "TCN": r"C:\Users\amanp\Desktop\MINOR\projj\code\metrics\Brazil\TCN_new_model_search_19-02-2025-17-39-28.csv",
    "CATBOOST": r"C:\Users\amanp\Desktop\MINOR\projj\code\metrics\Brazil\catboost_search_26-11-2024-08-11-11.csv",
    "TFT": r"C:\Users\amanp\Desktop\MINOR\projj\code\metrics\Brazil\TFT_new_model_search_26-11-2024-10-47-11.csv"
}
# code/metrics/Brazil/TCN_new_model_search_19-02-2025-17-39-28.csv
# Multiselect for models
model_options = st.sidebar.multiselect(
    "Select Models for Comparison:",
    list(model_files.keys()) + ["TFT"],  # Add TFT explicitly
    default=["LSTM", "TCN"]
)

# Sidebar for Feature Selection
selected_feature = st.sidebar.selectbox(
    "Select a Feature to Compare Across Models:",
    [
        'MAE (DengRate_all) Val',
        'RMSE (DengRate_all) Val',
        'MAPE (DengRate_all) Val',
        'R2 (DengRate_all) Val',
        'MSE (DengRate_all) Val',
        'MAE (DengRate_all) Train',
        'RMSE (DengRate_all) Train',
        'MAPE (DengRate_all) Train',
        'R2 (DengRate_all) Train',
        'MSE (DengRate_all) Train',
        'MAE (DengRate_019) Val',
        'RMSE (DengRate_019) Val',
        'MAPE (DengRate_019) Val',
        'R2 (DengRate_019) Val',
        'MSE (DengRate_019) Val',
        'MAE (DengRate_019) Train',
        'RMSE (DengRate_019) Train',
        'MAPE (DengRate_019) Train',
        'R2 (DengRate_019) Train',
        'MSE (DengRate_019) Train'
    ]
)

# Ensure models are selected
if model_options:
    st.subheader("Model Performance Comparison")

    # Metrics Computation for both datasets
    feature_results_original = []
    feature_results_search = []

    for model in model_options:
        if model != "TFT":  # Exclude TFT from the original dataset
            # Original dataset
            original_data = pd.read_csv(model_files[model])
            original_mean = original_data[selected_feature].mean()
            feature_results_original.append({"Model": model, "Mean Metric": original_mean, "Dataset": "Original"})

        # New dataset
        if model in model_files_search:
            search_data = pd.read_csv(model_files_search[model])
            search_mean = search_data[selected_feature].mean()
            feature_results_search.append({"Model": model, "Mean Metric": search_mean, "Dataset": "New"})

    # Combine results for visualization
    combined_results = pd.DataFrame(feature_results_original + feature_results_search)

    # Plot Feature Comparison with Plotly Express
    st.subheader(f"Comparison of {selected_feature} Across Models and Datasets")
    comparison_fig = px.bar(
        combined_results,
        x="Model",
        y="Mean Metric",
        color="Dataset",
        barmode="group",
        title=f"Comparison of {selected_feature} Across Models and Datasets",
        labels={"Mean Metric": selected_feature},
        text="Mean Metric"
    )
    comparison_fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    comparison_fig.update_layout(xaxis_title="Model", yaxis_title=f"Mean {selected_feature}")
    st.plotly_chart(comparison_fig)

    # Region-Wise Breakdown
    st.subheader("Region-Wise Analysis")
    selected_model = st.selectbox("Select a model to view region-specific metrics:", model_options)

    if selected_model != "TFT":  # Skip original dataset charts for TFT
        # Load data for selected model (original dataset)
        original_model_data = pd.read_csv(model_files[selected_model])
        st.subheader(f"Region-Wise {selected_feature} - Original Dataset ({selected_model})")
        region_fig_original = px.bar(
            original_model_data,
            x="Department",  # Replace with the actual department column in the CSV
            y=selected_feature,
            title=f"Region-Wise {selected_feature} - Original Dataset",
            labels={"Department": "Region", selected_feature: f"{selected_feature}"},
            color="Department",
            text=selected_feature
        )
        region_fig_original.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        region_fig_original.update_layout(xaxis_title="Region", yaxis_title=f"{selected_feature}")
        st.plotly_chart(region_fig_original)

    # Plot Region-Wise Metrics for New Dataset
    if selected_model in model_files_search:  # Ensure data is available for the new dataset
        search_model_data = pd.read_csv(model_files_search[selected_model])
        st.subheader(f"Region-Wise {selected_feature} - New Dataset ({selected_model})")
        region_fig_search = px.bar(
            search_model_data,
            x="Department",  # Replace with the actual department column in the CSV
            y=selected_feature,
            title=f"Region-Wise {selected_feature} - New Dataset",
            labels={"Department": "Region", selected_feature: f"{selected_feature}"},
            color="Department",
            text=selected_feature
        )
        region_fig_search.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        region_fig_search.update_layout(xaxis_title="Region", yaxis_title=f"{selected_feature}")
        st.plotly_chart(region_fig_search)

else:
    st.warning("Please select at least one model for comparison.")
