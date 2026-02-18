import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CPE-Pulse | Engineering Data Analysis",
    page_icon="⚡",
    layout="wide"
)

# --- SIDEBAR: NAVIGATION & GLOSSARY ---
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

# --- SIDEBAR: QUICK VOCABULARY ---
st.sidebar.markdown("---")
st.sidebar.header("📚 Key Terms")
if "Lesson 1" in lesson:
    st.sidebar.info("**Runout:** How much a gear 'wobbles' or is distorted. Lower is better.")
    st.sidebar.info("**Standard Deviation (σ):** A measure of consistency. Low σ means all parts are nearly identical.")
    st.sidebar.info("**Mean (μ):** The average value.")
elif "Lesson 2" in lesson:
    st.sidebar.info("**Correlation (r):** How strongly two variables are linked. (1.0 is a perfect match).")
    st.sidebar.info("**Outlier:** A data point that doesn't fit the pattern (likely an error or anomaly).")
    st.sidebar.info("**Regression:** A math formula used to predict future values.")


# ==========================================
# LESSON 1: THE MACK TRUCK GEAR CASE
# ==========================================
if lesson == "📖 Lesson 1: Variation (Gear Case)":
    st.title("⚙️ Lesson 1: Handling Variation in Manufacturing")
    
    # --- 1. THE CONTEXT (THE "WHY") ---
    st.markdown("""
    ### 🏗️ The Engineering Scenario
    You are a Process Engineer at Mack Truck. You are heat-treating large steel gears. 
    * **The Goal:** Minimize distortion (called **"Runout"**). If a gear is distorted, it vibrates and fails.
    * **The Decision:** You can load the gears into the furnace in two ways:
        1.  **Laid Flat:** Resting on their side.
        2.  **Hung:** Suspended from a rod.
    
    We ran a test on 77 gears to see which method is better.
    """)

    # --- 2. LOAD DATA ---
    laid_data = [5, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 15, 15, 15, 15, 16, 17, 17, 18, 19, 27]
    hung_data = [7, 8, 8, 10, 10, 10, 10, 11, 11, 11, 12, 13, 13, 13, 15, 17, 17, 17, 17, 18, 19, 19, 20, 21, 21, 21, 22, 22, 22, 23, 23, 23, 23, 24, 27, 27, 28, 31, 36]
    df_laid = pd.DataFrame({'Runout': laid_data, 'Method': 'Laid'})
    df_hung = pd.DataFrame({'Runout': hung_data, 'Method': 'Hung'})
    df = pd.concat([df_laid, df_hung])

    # --- 3. VISUALIZATION WITH EXPLANATION ---
    st.markdown("---")
    st.subheader("📊 Part 1: Visualizing the 'Spread'")
    st.write("Before calculating numbers, engineers look at the shape of the data.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        graph_type = st.radio("Select Graph Style:", ["Dot Plot (Raw Data)", "Box Plot (Summary)"], horizontal=True)
        if graph_type == "Dot Plot (Raw Data)":
            fig = px.strip(df, x="Runout", y="Method", color="Method", 
                           title="Comparison of Runout (Lower is Better)", hover_data=["Runout"])
            fig.update_traces(marker=dict(size=12, opacity=0.7))
        else:
            fig = px.box(df, x="Runout", y="Method", color="Method", points="all",
                         title="Statistical Summary (Box Plot)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 💡 How to read this:")
        if graph_type == "Dot Plot (Raw Data)":
            st.info("""
            * Each **dot** is one gear.
            * Look at the **Blue dots (Laid)**. Notice they are clumped to the left (lower numbers).
            * Look at the **Red dots (Hung)**. They are spread out way to the right.
            """)
        else:
            st.info("""
            * The **Box** holds the middle 50% of gears.
            * The **Line in the middle** is the Median.
            * The **Longer whiskers** on the 'Hung' group show it is unstable/unpredictable.
            """)

    # --- 4. STATISTICS WITH EXPLANATION ---
    st.markdown("---")
    st.subheader("🧮 Part 2: The Numbers")
    
    mean_laid = df_laid['Runout'].mean()
    mean_hung = df_hung['Runout'].mean()
    std_laid = df_laid['Runout'].std()
    std_hung = df_hung['Runout'].std()

    c1, c2, c3 = st.columns(3)
    c1.metric("Laid: Average Runout", f"{mean_laid:.2f}", delta="- Better", delta_color="normal")
    c2.metric("Laid: Std Deviation", f"{std_laid:.2f}", help="Lower means more consistent")
    c3.success(f"**Conclusion:** Laying gears flat reduces runout by {mean_hung - mean_laid:.2f} units on average.")


# ==========================================
# LESSON 2: RELATIONSHIPS (TORQUE VS TENSION)
# ==========================================
elif lesson == "📈 Lesson 2: Relationships (Torque)":
    st.title("📈 Lesson 2: Predicting Outcomes (Correlation)")
    
    # --- 1. THE CONTEXT ---
    st.markdown("""
    ### 🔩 The Engineering Scenario
    You are designing a bolted joint for a bridge. 
    You need to achieve a specific **Tension (Clamping Force)** in the bolt. 
    However, you cannot measure Tension directly in the field. You can only measure **Torque** (how hard you turn the wrench).
    
    **The Question:** Can we predict exactly how much Tension we get for a specific amount of Torque?
    """)

    # --- 2. GENERATE DATA ---
    np.random.seed(42)
    torque = np.linspace(10, 100, 40)
    tension = (torque * 2.5) + np.random.normal(0, 15, 40) 
    df_bolt = pd.DataFrame({'Torque (Nm)': torque, 'Tension (N)': tension})

    # --- 3. SCATTERPLOT LESSON ---
    st.markdown("---")
    st.subheader("🔍 Part 1: The Scatterplot")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        show_trend = st.checkbox("Show 'Line of Best Fit' (Regression Model)")
        fig_scatter = px.scatter(df_bolt, x="Torque (Nm)", y="Tension (N)", 
                                 title="Experiment Results: Torque vs. Tension",
                                 trendline="ols" if show_trend else None)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        st.markdown("#### 💡 What is happening?")
        st.info("""
        * **The Pattern:** As Torque (X) goes up, Tension (Y) goes up. This is a **Positive Correlation**.
        * **The Noise:** Notice the dots don't form a perfect line. This is due to **friction** and **dust** on the threads.
        * **The Line:** This is our 'Model'. It averages out the noise to give us a prediction.
        """)

    # --- 4. INTERACTIVE TOOL ---
    st.markdown("---")
    st.subheader("🎛️ Part 2: Engineering Calculator")
    st.write("Use the slider below to use the data model to set your wrench.")

    m, b = np.polyfit(torque, tension, 1)
    
    user_torque = st.slider("Step 1: Set your Torque Wrench (Nm)", 10, 100, 50)
    pred_tension = m * user_torque + b
    
    st.success(f"Step 2: Predicted Clamping Force = **{pred_tension:.2f} Newtons**")


# ==========================================
# PLAYGROUND
# ==========================================
elif lesson == "🔧 Playground: Upload Data":
    st.title("🔧 Data Playground")
    st.write("Upload a CSV file to inspect it.")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(df.head())