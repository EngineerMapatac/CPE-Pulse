import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CPE-Pulse | Engineering Data Analysis",
    page_icon="⚡",
    layout="wide"
)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("⚡ CPE-Pulse")
st.sidebar.caption("Based on *Vardeman & Jobe*")
lesson = st.sidebar.radio(
    "Select Lesson:",
    [
        "📖 Lesson 1: Variation (Gear Case)", 
        "📈 Lesson 2: Relationships (Torque vs. Tension)",
        "🔧 Playground: Upload Data"
    ]
)

# ==========================================
# LESSON 1: THE MACK TRUCK GEAR CASE
# ==========================================
if lesson == "📖 Lesson 1: Variation (Gear Case)":
    st.title("⚙️ Lesson 1: Handling Variation in Manufacturing")
    st.markdown("""
    **The Problem:** A process engineer at Mack Truck needs to minimize distortion (runout) in gears during heat treatment. 
    Should the gears be **Laid Flat** or **Hung**?
    
    *Reference: Basic Engineering Data Collection and Analysis, Chapter 1, Example 1*
    """)

    # --- Data Loading (Same as before) ---
    laid_data = [5, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 15, 15, 15, 15, 16, 17, 17, 18, 19, 27]
    hung_data = [7, 8, 8, 10, 10, 10, 10, 11, 11, 11, 12, 13, 13, 13, 15, 17, 17, 17, 17, 18, 19, 19, 20, 21, 21, 21, 22, 22, 22, 23, 23, 23, 23, 24, 27, 27, 28, 31, 36]
    df_laid = pd.DataFrame({'Runout': laid_data, 'Method': 'Laid'})
    df_hung = pd.DataFrame({'Runout': hung_data, 'Method': 'Hung'})
    df = pd.concat([df_laid, df_hung])

    # --- Visualization ---
    st.subheader("1. Visualizing the Variation")
    graph_type = st.radio("Select Style:", ["Dot Plot", "Box Plot"], horizontal=True)
    
    if graph_type == "Dot Plot":
        fig = px.strip(df, x="Runout", y="Method", color="Method", title="Runout Comparison")
    else:
        fig = px.box(df, x="Runout", y="Method", color="Method", title="Statistical Spread")
    
    st.plotly_chart(fig, use_container_width=True)

    # --- Quiz Section ---
    st.markdown("---")
    st.subheader("📝 Knowledge Check")
    q1 = st.radio("Which method is more consistent?", ["Hung", "Laid"], index=None)
    if q1 == "Laid": st.success("✅ Correct! Lower standard deviation = more consistency.")
    elif q1: st.error("❌ Incorrect. Look at the spread.")


# ==========================================
# LESSON 2: RELATIONSHIPS (TORQUE VS TENSION)
# ==========================================
elif lesson == "📈 Lesson 2: Relationships (Torque vs. Tension)":
    st.title("📈 Lesson 2: Analyzing Relationships (Scatterplots)")
    st.markdown("""
    **The Problem:** Engineers often need to predict one variable based on another. 
    *Example:* Does applying more **Torque** to a bolt always result in more **Tension**?
    
    *Reference: Basic Engineering Data Collection and Analysis, Chapter 4*
    """)

    # 1. GENERATE ENGINEERING DATA (Simulated based on Chapter 4 concepts)
    # Creating a dataset with a strong positive correlation but some "noise" (real life)
    np.random.seed(42)
    torque = np.linspace(10, 100, 30)  # 10 to 100 Nm
    tension = (torque * 2.5) + np.random.normal(0, 15, 30)  # Linear relation + Noise
    
    df_bolt = pd.DataFrame({'Torque (Nm)': torque, 'Tension (N)': tension})

    col1, col2 = st.columns([2, 1])

    with col1:
        # 2. SCATTERPLOT VISUALIZATION
        st.subheader("1. Visualizing the Relationship")
        st.write("A **Scatterplot** is the standard tool for seeing if X affects Y.")
        
        # Add Trendline toggle
        show_trend = st.checkbox("Show Best-Fit Line (Regression)")
        
        fig_scatter = px.scatter(df_bolt, x="Torque (Nm)", y="Tension (N)", 
                                 title="Bolt Experiment: Torque vs. Tension",
                                 trendline="ols" if show_trend else None)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        # 3. CORRELATION METRICS
        st.subheader("2. Measuring Strength")
        st.markdown("How strong is the relationship? We use **Correlation (r)**.")
        
        correlation = df_bolt['Torque (Nm)'].corr(df_bolt['Tension (N)'])
        
        st.metric("Correlation Coefficient (r)", f"{correlation:.4f}")
        
        if correlation > 0.9:
            st.success("Strong Positive Relationship")
        elif correlation > 0.5:
            st.warning("Moderate Relationship")
        else:
            st.error("Weak/No Relationship")

        st.info("""
        **Rule of Thumb:**
        * **r = 1.0:** Perfect Line
        * **r = 0.0:** Random Noise
        * **r = -1.0:** Perfect Inverse Line
        """)

    # 4. INTERACTIVE PREDICTION TOOL
    st.markdown("---")
    st.subheader("3. Engineering Prediction Tool")
    st.write("Since we have a strong relationship, we can **predict** Tension for a given Torque.")
    
    # Simple Linear Regression (y = mx + b)
    m, b = np.polyfit(torque, tension, 1)
    
    user_torque = st.slider("Select Input Torque (Nm):", 10, 150, 50)
    predicted_tension = m * user_torque + b
    
    st.metric(f"Predicted Tension for {user_torque} Nm", f"{predicted_tension:.2f} N")

# ==========================================
# PLAYGROUND
# ==========================================
elif lesson == "🔧 Playground: Upload Data":
    st.header("🔧 Data Analysis Playground")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(df.head())
        
        # Auto-detect numeric columns for scatterplot
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if len(numeric_cols) >= 2:
            x_axis = st.selectbox("Select X Axis", numeric_cols, index=0)
            y_axis = st.selectbox("Select Y Axis", numeric_cols, index=1)
            
            fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
            st.plotly_chart(fig)