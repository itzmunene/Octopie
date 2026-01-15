# src/ui/dashboard.py
import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Octopie Command", layout="wide")

# --- Custom Minimalist CSS (Matching your image) ---
st.markdown("""
    <style>
    .main { background-color: #1e1e2e; color: #cdd6f4; }
    .stMetric { background-color: #313244; padding: 15px; border-radius: 10px; border-left: 5px solid #f38ba8; }
    div[data-testid="stTable"] { background-color: #181825; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- Data Fetching ---
def fetch_data(endpoint):
    try:
        response = requests.get(f"http://localhost:8000/{endpoint}")
        return response.json()
    except:
        return None

st.title("🐙 Octopie: Autonomous Defense System")

# --- Layout ---
# 1. Top Row: Stats
stats = fetch_data("stats")
col1, col2, col3, col4, col5 = st.columns(5)
if stats:
    col1.metric("Total Events", stats['total_events'])
    col2.metric("Antibodies", stats['signatures'])
    col3.metric("L2 Status", "NOMINAL", delta="Innate")
    col4.metric("L3 Context", "ACTIVE", delta="Adaptive")
    col5.metric("L4 Reflex", "READY", delta="Containment")

# 2. Middle Row: The Pulse & Distribution
col_main, col_side = st.columns([2, 1])
ledger_data = fetch_data("ledger")

if ledger_data:
    df = pd.DataFrame(ledger_data)
    
    with col_main:
        st.subheader("Neural Anomaly Pulse (L2)")
        # Creating the line chart from your design
        fig = px.line(df, x='timestamp', y='anomaly_score', 
                     template="plotly_dark", color_discrete_sequence=['#f38ba8'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with col_side:
        st.subheader("Threat Distribution")
        # Horizontal bar chart matching the right side of your design
        fig_bar = px.bar(df, y='context_status', orientation='h', 
                         template="plotly_dark", color='context_status')
        st.plotly_chart(fig_bar, use_container_width=True)

# 3. Bottom Row: Ledger
st.subheader("Executive Ledger (L5 Memory)")
if ledger_data:
    st.table(df[['timestamp', 'cpu_percent', 'anomaly_score', 'context_status', 'action_taken']].head(10))

# --- Auto-refresh ---
time.sleep(1)
st.rerun()