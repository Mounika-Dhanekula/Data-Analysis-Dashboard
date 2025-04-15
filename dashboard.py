
import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px

# Page Configurations
st.set_page_config(page_title="🚀 Dynamic Data Dashboard", layout="wide", page_icon="📊")

# Sidebar for Uploading Datasets
st.sidebar.header("📂 Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("📥 **Upload your CSV or Excel file here:**", type=["csv", "xlsx"])

# Load Dataset
@st.cache_data
def load_data(file):
    try:
        if file.name.endswith('.csv'):
            data = pd.read_csv(file, encoding='latin1', on_bad_lines='skip')
            return data
        elif file.name.endswith('.xlsx'):
            return pd.read_excel(file)
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"🚨 Oops! An error occurred while loading the file: {e}")
        return pd.DataFrame()

# Load actual or fallback demo data
if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    st.info("🔎 No file uploaded — loading a demo dataset to preview functionality.")
    df = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=10),
        "Sales": [120, 135, 160, 190, 210, 230, 250, 270, 300, 320],
        "Category": ["A", "A", "B", "A", "B", "B", "C", "C", "C", "A"]
    })
    uploaded_file = type("FakeUpload", (object,), {"name": "demo_data.csv"})()

# Main UI
if not df.empty:
    dataset_name = uploaded_file.name.split('.')[0].replace('_', ' ').title()
    st.markdown(f'<h1 style="text-align:center;">📊 {dataset_name} Dashboard 🚀</h1>', unsafe_allow_html=True)

    st.markdown("### 🗂 Dataset Overview")
    st.markdown(f"📅 Last refreshed on: {datetime.datetime.now().strftime('%d %B %Y')}")
    st.markdown("✅ Dataset loaded! Here’s a preview:")
    st.dataframe(df)

    # Sidebar graph controls
    st.sidebar.markdown("### 📊 Graph Options")
    x_axis = st.sidebar.selectbox("🔎 Select X-axis", options=df.columns)
    y_axis = st.sidebar.selectbox("📌 Select Y-axis", options=df.columns)
    graph_type = st.sidebar.selectbox("🎨 Choose Graph Type", options=["Line Chart", "Bar Chart", "Histogram", "Pie Chart"])

    try:
        df[y_axis] = pd.to_numeric(df[y_axis], errors='coerce')
        avg_value = df[y_axis].dropna().mean()
        st.sidebar.markdown(f"⭐ *Average {y_axis}:* {avg_value:.2f}")
    except Exception as e:
        st.sidebar.warning(f"⚠ Unable to calculate average: {e}")

    # Graph visualization
    st.markdown("### 📈 Graph Visualizations")
    if graph_type == "Line Chart":
        fig = px.line(df, x=x_axis, y=y_axis, title=f"📈 Line Chart: {y_axis} vs {x_axis}", template="plotly_white")
    elif graph_type == "Bar Chart":
        fig = px.bar(df, x=x_axis, y=y_axis, title=f"📊 Bar Chart: {y_axis} vs {x_axis}", template="plotly_white")
    elif graph_type == "Histogram":
        fig = px.histogram(df, x=x_axis, title=f"📉 Histogram: {x_axis}", template="plotly_white")
    elif graph_type == "Pie Chart":
        pie_data = df[y_axis].value_counts().reset_index()
        pie_data.columns = ["Category", "Count"]
        fig = px.pie(pie_data, values="Count", names="Category",
                     title=f"🥧 Pie Chart: Distribution of {y_axis}",
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)

    # Dataset download option
    st.markdown("### 💾 Download Processed Dataset")
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Click to Download CSV", data=csv_data, file_name=f"{dataset_name}.csv", mime="text/csv")

else:
    st.markdown('<h1 style="text-align:center;">📊 Interactive Data Dashboard 🚀</h1>', unsafe_allow_html=True)
    st.markdown("## 👋 Welcome to the Dynamic Data Dashboard!")
    st.markdown("### 🛠 Upload a Dataset from the sidebar to get started.")
    st.info("💡 Use CSV or Excel formats.")

# Footer
st.markdown("""
    <hr style="border-top: 2px solid #003366;">
    <p style="text-align: center; font-size: small;">🌟 Designed with creativity by Mounika | Powered by Streamlit 🚀</p>
""", unsafe_allow_html=True)
