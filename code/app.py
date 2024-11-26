import streamlit as st

st.title("Machine Learning Analysis Dashboard")
st.write("hello")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page", ["EDA", "Model Comparison", "Feature Importance"])

if page == "EDA":
    from pages import EDA
    EDA
elif page == "Model Comparison":
    from pages import Comparison 
    Comparison
# elif page == "Feature Importance":
#     from pages import FeatureImportance 
#     FeatureImportance
