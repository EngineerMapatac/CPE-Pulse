import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CPE-Pulse | Engineering Data Analysis",
    page_icon="⚙️",
    layout="wide"
)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("⚡ CPE-Pulse")
st.sidebar.caption("Based on *Vardeman & Jobe*")
lesson = st.sidebar.radio(
    "Select Lesson:",
    ["📖 Lesson 1: Variation (Gear Case)", "🔧 Playground: Upload Data"]
)

# --- LESSON 1: THE MACK TRUCK GEAR CASE ---
if lesson == "📖 Lesson 1: Variation (Gear Case)":
    st.title("⚙️ Lesson 1: Handling Variation in Manufacturing")
    st.markdown("""
    **The Problem:** A process engineer at Mack Truck needs to minimize distortion (runout) in gears during heat treatment. 
    Should the gears be **Laid Flat** or **Hung**?
    
    *Reference: Basic Engineering Data Collection and Analysis, Chapter 1, Example 1*
    """)

    # 1. LOAD ACTUAL DATA FROM TEXTBOOK
    laid_data = [5, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 15, 15, 15, 15, 16, 17, 17, 18, 19, 27]
    hung_data = [7, 8, 8, 10, 10, 10, 10, 11, 11, 11, 12, 13, 13, 13, 15, 17, 17, 17, 17, 18, 19, 19, 20, 21, 21, 21, 22, 22, 22, 23, 23, 23, 23, 24, 27, 27, 28, 31, 36]

    df_laid = pd.DataFrame({'Runout (.0001 in)': laid_data, 'Method': 'Laid'})
    df_hung = pd.DataFrame({'Runout (.0001 in)': hung_data, 'Method': 'Hung'})
    df = pd.concat([df_laid, df_hung])

    # 2. INTERACTIVE VISUALIZATION
    st.subheader("1. Visualizing the Variation")
    st.write("Compare the 'spread' of data points below. A wider spread means less consistency.")
    
    graph_type = st.radio("Select Visualization Style:", ["Dot Plot (Textbook Style)", "Box Plot (Statistical View)"], horizontal=True)

    if graph_type == "Dot Plot (Textbook Style)":
        fig = px.strip(df, x="Runout (.0001 in)", y="Method", color="Method", 
                       title="Comparison of Thrust Face Runouts",
                       hover_data=["Runout (.0001 in)"])
        fig.update_traces(marker=dict(size=10, opacity=0.7))
    else:
        fig = px.box(df, x="Runout (.0001 in)", y="Method", color="Method", points="all",
                     title="Statistical Spread: Laid vs. Hung")
    
    st.plotly_chart(fig, use_container_width=True)

    # 3. ENGINEERING ANALYSIS
    st.subheader("2. Quantifying the Improvement")
    col1, col2 = st.columns(2)
    
    mean_laid = df_laid['Runout (.0001 in)'].mean()
    mean_hung = df_hung['Runout (.0001 in)'].mean()
    std_laid = df_laid['Runout (.0001 in)'].std()
    std_hung = df_hung['Runout (.0001 in)'].std()

    with col1:
        st.info(f"**Laid Gears (Flat)**")
        st.metric("Mean Runout (Lower is better)", f"{mean_laid:.2f}")
        st.metric("Std Dev (Consistency)", f"{std_laid:.2f}")

    with col2:
        st.warning(f"**Hung Gears (Vertical)**")
        st.metric("Mean Runout (Lower is better)", f"{mean_hung:.2f}")
        st.metric("Std Dev (Consistency)", f"{std_hung:.2f}")

    # --- NEW SECTION: INTERACTIVE QUIZ ---
    st.markdown("---")
    st.subheader("📝 Knowledge Check: Engineering Decision")
    
    # Question 1
    q1 = st.radio(
        "1. Looking at the Standard Deviation (Std Dev), which method is more consistent (predictable)?",
        ["Hung Gears", "Laid Gears", "They are the same"],
        index=None
    )
    if q1 == "Laid Gears":
        st.success("✅ Correct! A lower Std Dev (4.3 vs 7.3) means the 'Laid' process varies less.")
    elif q1:
        st.error("❌ Incorrect. Look at the 'Std Dev' values above. Lower is more consistent.")

    # Question 2
    q2 = st.radio(
        "2. Why is the 'Hung' method considered worse for this specific part?",
        ["It uses too much heat.", "It has a higher average runout (distortion) and more variation.", "The data is missing."],
        index=None
    )
    if q2 == "It has a higher average runout (distortion) and more variation.":
        st.success("✅ Correct! In engineering, we want 'On Target' (Low Mean) and 'Consistent' (Low Std Dev).")
    elif q2:
        st.error("❌ Incorrect. Check the Mean and Std Dev values again.")

    # Question 3 (Critical Thinking)
    q3 = st.selectbox(
        "3. If the 'Laid' method costs $5.00/gear and 'Hung' costs $0.50/gear, would you still switch?",
        ["Select your answer...", "Yes, quality is everything.", "No, the cost difference is huge.", "It depends on the tolerance limits."]
    )
    if q3 == "It depends on the tolerance limits.":
        st.success("✅ Correct! As an engineer, you must balance Cost vs. Quality. If 'Hung' gears still pass the tolerance check, the cheaper option might be better.")
    elif q3 != "Select your answer...":
        st.info("💡 Hint: In Six Sigma, we don't just maximize quality; we optimize for 'Fitness for Use' vs Cost.")

# --- PLAYGROUND ---
elif lesson == "🔧 Playground: Upload Data":
    st.header("🔧 Data Analysis Playground")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        df_user = pd.read_csv(uploaded_file)
        st.dataframe(df_user.head())