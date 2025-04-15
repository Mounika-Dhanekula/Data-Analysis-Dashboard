import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px

# Page Configurations
st.set_page_config(page_title="🚀 Dynamic Data Dashboard", layout="wide", page_icon="📊")

# Sidebar for Uploading Datasets
st.sidebar.header("📂 Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Drag and drop your file here 📥", type=["csv", "xlsx"])

# Load Dataset
@st.cache_data
def load_data(file):
    try:
        if file.name.endswith('.csv'):
            data = pd.read_csv(file, encoding='latin1', on_bad_lines='skip')  # Skip problematic rows
            return data
        elif file.name.endswith('.xlsx'):
            return pd.read_excel(file)
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"🚨 Oops! An error occurred while loading the file: {e}")
        return pd.DataFrame()

# File Handling
if uploaded_file is not None:
    df = load_data(uploaded_file)  # Load dataset if a file is uploaded

    if not df.empty:
        # Dynamic Title based on Dataset Name
        dataset_name = uploaded_file.name.split('.')[0].replace('_', ' ').title()
        st.markdown(f'<h1 style="text-align:center;">📊 {dataset_name} Dashboard 🚀</h1>', unsafe_allow_html=True)

        st.markdown("### 🗂 *Dataset Overview*")
        st.markdown(f"📅 *Last refreshed on:* {datetime.datetime.now().strftime('%d %B %Y')}")
        st.markdown("✅ Your uploaded dataset has been successfully loaded! Here’s a preview:")
        st.dataframe(df)

        # Dropdowns for selecting X-axis, Y-axis, and graph type
        st.sidebar.markdown("### 📊 *Graph Options*")
        x_axis = st.sidebar.selectbox("🔎 Select X-axis", options=df.columns)
        y_axis = st.sidebar.selectbox("📌 Select Y-axis", options=df.columns)
        graph_type = st.sidebar.selectbox("🎨 Choose Graph Type", options=["Line Chart", "Bar Chart", "Histogram", "Pie Chart"])

        # Ensure Y-axis column is numeric for averaging
        try:
            df[y_axis] = pd.to_numeric(df[y_axis], errors='coerce')  # Convert non-numeric values to NaN
            avg_value = df[y_axis].dropna().mean()
            st.sidebar.markdown(f"⭐ **Average {y_axis}:** {avg_value:.2f}")
        except Exception as e:
            st.sidebar.warning(f"⚠️ Unable to calculate average: {e}")

        # Display the selected graph based on user input
        st.markdown("### 📈 *Graph Visualizations*")
        if graph_type == "Line Chart":
            fig_line = px.line(df, x=x_axis, y=y_axis, title=f"📈 Line Chart: {y_axis} vs {x_axis}", template="plotly_white")
            st.plotly_chart(fig_line, use_container_width=True)

        elif graph_type == "Bar Chart":
            fig_bar = px.bar(df, x=x_axis, y=y_axis, title=f"📊 Bar Chart: {y_axis} vs {x_axis}", template="plotly_white")
            st.plotly_chart(fig_bar, use_container_width=True)

        elif graph_type == "Histogram":
            fig_histogram = px.histogram(df, x=x_axis, title=f"📉 Histogram: {x_axis}", template="plotly_white")
            st.plotly_chart(fig_histogram, use_container_width=True)

        elif graph_type == "Pie Chart":
            pie_data = df[y_axis].value_counts().reset_index()
            pie_data.columns = ["Category", "Count"]
            fig_pie = px.pie(pie_data, values="Count", names="Category", title=f"🥧 Pie Chart: Distribution of {y_axis}", color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_pie, use_container_width=True)

        # Option to download the dataset
        st.markdown("### 💾 *Download Processed Dataset*")
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Click to Download Dataset as CSV", data=csv_data, file_name=f"{dataset_name}.csv", mime="text/csv")

    else:
        st.warning("⚠️ The uploaded file could not be processed. Please check the file structure and try again.")
else:
    st.markdown('<h1 style="text-align:center;">📊 Interactive Data Dashboard 🚀</h1>', unsafe_allow_html=True)
    st.markdown("### 🛠 *Upload a Dataset to Begin!*")
    st.info("💡 Use the sidebar to upload your CSV or Excel file.")

# Footer
st.markdown("""
    <hr style="border-top: 2px solid #003366;">
    <p style="text-align: center; font-size: small;">🌟 Designed with creativity by Mounika | Powered by Streamlit 🚀</p>
""", unsafe_allow_html=True)
