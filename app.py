import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. Page Configuration (Browser Tab Title & Layout)
st.set_page_config(
    page_title="CPE-Pulse | Engr Data Analysis",
    page_icon="⚡",
    layout="wide"
)

# 2. Sidebar Navigation (Mobile-Friendly Menu)
st.sidebar.title("⚡ CPE-Pulse")
st.sidebar.markdown("By: *Engr. J.R. Mapatac*")
page = st.sidebar.radio(
    "Select Module:",
    ["🏠 Home", "📡 Network Traffic", "🤖 Sensor Fusion", "🔋 Power Profiler"]
)

# --- PAGE: HOME ---
if page == "🏠 Home":
    st.title("Welcome to CPE-Pulse ⚡")
    st.markdown("""
    ### Engineering Data Analysis for Everyone
    This platform bridges the gap between **Computer Engineering hardware** and **Data Science**.
    
    **Choose a module from the sidebar to start:**
    * **📡 Network Traffic:** Analyze packet loss and latency (Cisco focus).
    * **🤖 Sensor Fusion:** Clean noisy robotics data (Kalman Filters).
    * **🔋 Power Profiler:** Optimize embedded systems (Six Sigma/DMAIC).
    """)
    
    st.info("💡 **Tip:** Open the sidebar (top-left arrow on mobile) to navigate.")

# --- PAGE: NETWORK TRAFFIC (Interactive Demo) ---
elif page == "📡 Network Traffic":
    st.header("📡 Network Traffic Analyzer")
    st.write("Upload your Wireshark CSV export or Router Logs to visualize bottlenecks.")

    # A. The Interactive File Uploader
    uploaded_file = st.file_uploader("Upload Network Log (CSV)", type=["csv"])

    # B. If user uploads a file, run analysis
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ File Uploaded Successfully!")
            
            # Show raw data preview
            with st.expander("View Raw Data"):
                st.dataframe(df.head())

            # C. Engineering Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Packets", len(df))
            col2.metric("Avg Latency", f"{df['latency_ms'].mean():.2f} ms")
            col3.metric("Max Throughput", f"{df['throughput_mbps'].max()} Mbps")

            # D. Mobile-Friendly Visualization (Plotly)
            st.subheader("Latency vs. Time")
            fig = px.line(df, x='time_sec', y='latency_ms', title='Network Latency Stability')
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error parsing file: {e}. Make sure your CSV has 'latency_ms' and 'time_sec' columns.")
    
    # E. Demo Data Button (For users without files)
    else:
        if st.button("Use Sample Data (Demo)"):
            # Create dummy engineering data
            data = {
                'time_sec': np.arange(0, 60, 1),
                'latency_ms': np.random.normal(20, 5, 60),  # Normal distribution around 20ms
                'throughput_mbps': np.random.uniform(10, 100, 60)
            }
            df_sample = pd.DataFrame(data)
            
            st.markdown("---")
            st.write("### 📊 Sample Analysis Result")
            fig_sample = px.line(df_sample, x='time_sec', y='latency_ms', title='Simulated Network Latency')
            st.plotly_chart(fig_sample, use_container_width=True)

# --- PAGE: ROBOTICS (Placeholder) ---
elif page == "🤖 Sensor Fusion":
    st.header("🤖 Sensor Fusion & Filtering")
    st.warning("🚧 This module is under construction. Coming soon!")
    

# --- PAGE: POWER (Placeholder) ---
elif page == "🔋 Power Profiler":
    st.header("🔋 Embedded Power Profiler")
    st.warning("🚧 This module is under construction. Coming soon!")