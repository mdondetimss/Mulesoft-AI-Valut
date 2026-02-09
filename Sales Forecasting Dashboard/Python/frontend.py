import streamlit as st
import matplotlib.pyplot as plt
from backend import run_pipeline


st.title("Sales Forecasting and Analysis.")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")


# Use a form to prevent auto-rerun execution
with st.form("analysis_form"):
    lag_value = st.slider("Select Lag Value", min_value=1, max_value=30, value=5)
    submit = st.form_submit_button("Analyze")

# Only run when form is submitted
if submit and uploaded_file is not None:

    # Cache heavy pipeline
    @st.cache_data
    def cached_pipeline(file, lag):
        return run_pipeline(file, lag)

    aggregated, results = cached_pipeline(uploaded_file, lag_value)

    st.subheader("RMSE")
    st.write(f"RMSE: {results['rmse']:.2f}")

    # Plot Sales Over Time
    st.subheader("Sales Over Time")
    fig1, ax1 = plt.subplots(figsize=(10,5))
    ax1.plot(aggregated["Order Date"], aggregated["Sales"])
    ax1.set_title("Sales Over Time")
    st.pyplot(fig1)

    # Plot Predictions
    st.subheader("Actual vs Predicted")
    fig2, ax2 = plt.subplots(figsize=(10,5))
    ax2.plot(results["y_test"].values, label="Actual")
    ax2.plot(results["predictions"], label="Predicted")
    ax2.legend()
    st.pyplot(fig2)