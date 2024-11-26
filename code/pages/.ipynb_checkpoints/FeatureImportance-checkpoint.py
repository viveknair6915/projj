import streamlit as st
import pandas as pd
import plotly.express as px
from utilss.model_utils import get_feature_importance

# Page Title
st.title("Feature Importance")

# Sidebar Options
model_files = {
    "LSTM": r"C:\Users\amanp\Desktop\MINOR\projj\code\metrics\Brazil\LSTM_Model_26-11-2024-08-30-12.csv",
    "TCN": r"C:\Users\amanp\Desktop\MINOR\projj\code\metrics\Brazil\TCN_new_model_26-11-2024-08-29-01.csv",
    "CATBOOST": r"C:\Users\amanp\Desktop\MINOR\projj\code\metrics\Brazil\catboost_normal26-11-2024-08-30-30.csv"
}

# Sidebar selection for model
selected_model = st.sidebar.selectbox(
    "Select a Model for Feature Importance:",
    list(model_files.keys())
)

# Load Original Data
original_data = pd.read_csv("C:/Users/amanp/Desktop/MINOR/projj/code/dataset/Brazil_UF_dengue_monthly.csv")

# Display Feature Importance
if selected_model:
    st.subheader(f"Feature Importance for {selected_model}")
    
    # Compute Feature Importance
    feature_importance = get_feature_importance(original_data, selected_model)
    feature_importance_df = pd.DataFrame(feature_importance, columns=["Feature", "Importance"])
    
    # Plot Feature Importance using Plotly Express
    fig = px.bar(
        feature_importance_df.sort_values("Importance", ascending=False),
        x="Importance",
        y="Feature",
        orientation="h",  # Horizontal bar chart
        title=f"Feature Importance for {selected_model}",
        labels={"Importance": "Importance Score", "Feature": "Feature"},
        color="Importance",
        color_continuous_scale="Viridis"
    )
    fig.update_layout(
        yaxis=dict(title="Features", categoryorder="total ascending"),  # Order features by importance
        xaxis=dict(title="Importance Score"),
        margin=dict(l=0, r=0, t=50, b=50)
    )
    st.plotly_chart(fig)
else:
    st.warning("Please select a model to view feature importance.")
