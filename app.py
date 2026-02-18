import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CPE-Pulse | Engineering Data Analysis",
    page_icon="⚡",
    layout="wide"
)

# --- 2. SIDEBAR SETUP ---
st.sidebar.title("⚡ CPE-Pulse")
st.sidebar.write("*Interactive Engineering Lessons*")
lesson = st.sidebar.radio(
    "Select Module:",
    [
        "📖 Lesson 1: Variation (Gear Case)", 
        "📈 Lesson 2: Relationships (Torque)",
        "🔧 Playground: Upload Data"
    ]
)

# Sidebar Glossary (Context-Aware)
st.sidebar.markdown("---")
st.sidebar.header("📚 Key Terms")
if "Lesson 1" in lesson:
    st.sidebar.info("**Runout:** How much a gear 'wobbles'. Lower is better.")
    st.sidebar.info("**Std Dev (σ):** Consistency. Low σ means parts are identical.")
elif "Lesson 2" in lesson:
    st.sidebar.info("**Correlation (r):** Relationship strength. 1.0 is perfect.")
    st.sidebar.info("**Regression:** Using math to predict a value (y = mx + b).")

# ==========================================
# LESSON 1: THE MACK TRUCK GEAR CASE
# ==========================================
if lesson == "📖 Lesson 1: Variation (Gear Case)":
    st.title("⚙️ Lesson 1: Handling Variation")
    
    st.markdown("""
    ### 🏗️ The Scenario
    You are a Process Engineer at Mack Truck. You need to reduce gear distortion (**Runout**).
    * **Method A (Laid):** Gears laid flat in the furnace.
    * **Method B (Hung):** Gears hung from a rod.
    """)

    # Data Loading
    laid_data = [5, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 15, 15, 15, 15, 16, 17, 17, 18, 19, 27]
    hung_data = [7, 8, 8, 10, 10, 10, 10, 11, 11, 11, 12, 13, 13, 13, 15, 17, 17, 17, 17, 18, 19, 19, 20, 21, 21, 21, 22, 22, 22, 23, 23, 23, 23, 24, 27, 27, 28, 31, 36]
    df = pd.concat([
        pd.DataFrame({'Runout': laid_data, 'Method': 'Laid'}),
        pd.DataFrame({'Runout': hung_data, 'Method': 'Hung'})
    ])

    # Visualization
    st.subheader("📊 Part 1: Visualizing the Data")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        graph_type = st.radio("Graph Style:", ["Dot Plot", "Box Plot"], horizontal=True)
        if graph_type == "Dot Plot":
            fig = px.strip(df, x="Runout", y="Method", color="Method", title="Runout Comparison")
            fig.update_traces(marker=dict(size=10, opacity=0.7))
        else:
            fig = px.box(df, x="Runout", y="Method", color="Method", title="Statistical Spread")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.info("💡 **Tip:** Notice how the 'Hung' data (Red) spreads further to the right. That means it's less consistent.")

    # Statistics
    st.subheader("🧮 Part 2: The Metrics")
    m_laid, s_laid = np.mean(laid_data), np.std(laid_data)
    m_hung, s_hung = np.mean(hung_data), np.std(hung_data)
    
    c1, c2 = st.columns(2)
    c1.metric("Laid: Avg Runout", f"{m_laid:.2f}", delta="- Better")
    c2.metric("Laid: Consistency (Std Dev)", f"{s_laid:.2f}", help="Lower is better")

# ==========================================
# LESSON 2: RELATIONSHIPS (TORQUE VS TENSION)
# ==========================================
elif lesson == "📈 Lesson 2: Relationships (Torque)":
    st.title("📈 Lesson 2: Predicting Outcomes")
    
    st.markdown("""
    ### 🔩 The Scenario
    Can we predict bolt **Tension** (Clamping Force) just by measuring **Torque** (Wrench Force)?
    """)

    # 1. Generate Data
    np.random.seed(42)
    torque = np.linspace(10, 100, 40)
    # y = mx + b + noise
    tension = (torque * 2.5) + np.random.normal(0, 15, 40) 
    df_bolt = pd.DataFrame({'Torque (Nm)': torque, 'Tension (N)': tension})

    # 2. Calculate Math Model (Linear Regression)
    m, b = np.polyfit(torque, tension, 1) # Slope (m) and Intercept (b)

    # 3. Visualization
    st.subheader("🔍 Part 1: The Scatterplot")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        show_line = st.checkbox("Show Prediction Line (Math Model)")
        
        # Base Scatter Plot
        fig = px.scatter(df_bolt, x="Torque (Nm)", y="Tension (N)", title="Torque vs. Tension Experiment")
        
        # Manually add line (No statsmodels needed!)
        if show_line:
            # Create a line from min torque to max torque
            x_line = np.array([10, 100])
            y_line = m * x_line + b
            fig.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', name='Prediction Model', line=dict(color='red')))
            
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.info(f"**Correlation:** {df_bolt['Torque (Nm)'].corr(df_bolt['Tension (N)']):.2f}")
        st.write("A score near 1.0 means Torque is a great predictor of Tension.")

    # 4. Interactive Calculator
    st.subheader("🎛️ Part 2: The Engineer's Tool")
    st.write("Use the slider to predict tension for any torque setting.")
    
    user_input = st.slider("Wrench Torque Setting (Nm):", 10, 100, 50)
    prediction = m * user_input + b
    
    st.success(f"Predicted Clamping Force: **{prediction:.2f} N**")

# ==========================================
# PLAYGROUND
# ==========================================
elif lesson == "🔧 Playground: Upload Data":
    st.title("🔧 Data Playground")
    st.write("Upload any CSV to view.")
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        df = pd.read_csv(file)
        st.dataframe(df.head())