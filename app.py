import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="CPE-Pulse Pro", layout="wide")

# --- 1. INJECT CUSTOM CSS (The "Design" Layer) ---
# This hides the default menu and styles your metrics to look like dashboard cards.
st.markdown("""
    <style>
    /* Make the metric cards look like real engineering displays */
    div[data-testid="stMetric"] {
        background-color: #f0f2f6;
        border-left: 5px solid #4B4B4B;
        padding: 10px;
        border-radius: 5px;
    }
    
    /* Custom Class for 'Pass' Status */
    .pass-status {
        color: #28a745;
        font-weight: bold;
        padding: 5px;
        border: 1px solid #28a745;
        border-radius: 4px;
    }

    /* Custom Class for 'Fail' Status */
    .fail-status {
        color: #dc3545;
        font-weight: bold;
        padding: 5px;
        border: 1px solid #dc3545;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. PYTHON LOGIC (The "Brain" Layer) ---
st.title("⚡ CPE-Pulse: Custom UI Demo")
st.write("This shows how Python calculates the data, but HTML/CSS makes it look professional.")

# Simulate Engineering Data
voltage = 3.1  # Volts
threshold = 3.3

# --- 3. MIXING THEM TOGETHER ---
col1, col2 = st.columns(2)

with col1:
    # Standard Streamlit (Python only)
    st.metric(label="Voltage Sensor (Standard)", value=f"{voltage} V")

with col2:
    # Custom HTML Injection
    if voltage < threshold:
        status_html = '<span class="fail-status">LOW VOLTAGE WARNING</span>'
    else:
        status_html = '<span class="pass-status">OPTIMAL</span>'
    
    # We use markdown to render the HTML string we built
    st.markdown(f"""
        <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
            <p style="margin:0; font-size: 14px; color: #666;">Voltage Sensor (Custom HTML)</p>
            <h2 style="margin:0;">{voltage} V</h2>
            <p style="margin-top: 5px;">Status: {status_html}</p>
        </div>
    """, unsafe_allow_html=True)