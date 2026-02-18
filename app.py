import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    should the gears be **Laid Flat** or **Hung**?
    
    *Reference: Basic Engineering Data Collection and Analysis, Chapter 1, Example 1*
    """)

    # 1. LOAD ACTUAL DATA FROM TEXTBOOK 
    # "Laid" data (38 gears) and "Hung" data (39 gears) from Table 1.1
    laid_data = [5, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 15, 15, 15, 15, 16, 17, 17, 18, 19, 27]
    hung_data = [7, 8, 8, 10, 10, 10, 10, 11, 11, 11, 12, 13, 13, 13, 15, 17, 17, 17, 17, 18, 19, 19, 20, 21, 21, 21, 22, 22, 22, 23, 23, 23, 23, 24, 27, 27, 28, 31, 36]

    # Create a DataFrame for analysis
    df_laid = pd.DataFrame({'Runout (.0001 in)': laid_data, 'Method': 'Laid'})
    df_hung = pd.DataFrame({'Runout (.0001 in)': hung_data, 'Method': 'Hung'})
    df = pd.concat([df_laid, df_hung])

    # 2. INTERACTIVE VISUALIZATION
    st.subheader("1. Visualizing the Variation")
    st.write("The book uses 'Dot Diagrams' to show that variation exists even within a single method.")
    
    # User Control: Choose Graph Type
    graph_type = st.radio("Select Visualization Style:", ["Dot Plot (Textbook Style)", "Box Plot (Statistical View)"], horizontal=True)

    if graph_type == "Dot Plot (Textbook Style)":
        # Simulate a Dot Plot using Strip Plot
        fig = px.strip(df, x="Runout (.0001 in)", y="Method", color="Method", 
                       title="Comparison of Thrust Face Runouts (Textbook Figure 1.1)",
                       hover_data=["Runout (.0001 in)"])
        fig.update_traces(marker=dict(size=10, opacity=0.7))
    else:
        # Box Plot for clearer statistical summary
        fig = px.box(df, x="Runout (.0001 in)", y="Method", color="Method", points="all",
                     title="Statistical Spread: Laid vs. Hung")
    
    st.plotly_chart(fig, use_container_width=True)

    # 3. ENGINEERING ANALYSIS
    st.subheader("2. Quantifying the Improvement")
    
    col1, col2 = st.columns(2)
    
    # Calculate Statistics
    mean_laid = df_laid['Runout (.0001 in)'].mean()
    mean_hung = df_hung['Runout (.0001 in)'].mean()
    std_laid = df_laid['Runout (.0001 in)'].std()
    std_hung = df_hung['Runout (.0001 in)'].std()

    with col1:
        st.info(f"**Laid Gears**")
        st.metric("Mean Runout", f"{mean_laid:.2f}")
        st.metric("Std Dev (Consistency)", f"{std_laid:.2f}")

    with col2:
        st.warning(f"**Hung Gears**")
        st.metric("Mean Runout", f"{mean_hung:.2f}")
        st.metric("Std Dev (Consistency)", f"{std_hung:.2f}")

    # 4. CONCLUSION
    st.subheader("3. The Engineering Decision")
    improvement = mean_hung - mean_laid
    
    st.markdown(f"""
    > **Textbook Insight:** "From Figure 1.1... several points are obvious. One is that there is variation... [but] Laid runouts are on the whole smaller." [cite: 479]
    
    **Analysis:**
    * **Accuracy:** Laying the gears reduces the average runout by **{improvement:.2f}** units.
    * **Precision:** The 'Laid' method has a lower Standard Deviation (**{std_laid:.2f}** vs **{std_hung:.2f}**), meaning it is more consistent.
    
    **Recommendation:** Unless the cost of 'Laying' is significantly higher, it is the superior engineering method.
    """)

# --- PLAYGROUND: UPLOAD OWN DATA ---
elif lesson == "🔧 Playground: Upload Data":
    st.header("🔧 Data Analysis Playground")
    st.write("Upload your own engineering CSV files (e.g., sensor logs, circuit tests).")
    
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        df_user = pd.read_csv(uploaded_file)
        st.write("### Data Preview")
        st.dataframe(df_user.head())
        
        # Simple auto-plotter
        numeric_cols = df_user.select_dtypes(include=['float', 'int']).columns
        if len(numeric_cols) > 0:
            target_col = st.selectbox("Select Column to Analyze:", numeric_cols)
            fig_user = px.histogram(df_user, x=target_col, title=f"Distribution of {target_col}")
            st.plotly_chart(fig_user)