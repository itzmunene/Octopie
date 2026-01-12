# src/ui/dashboard.py
import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Octopie Command", layout="wide")
API_BASE = "http://127.0.0.1:8000"

st.title("🐙 Octopie Autonomous Enterprise")

# Layout: Sidebar for quick stats
with st.sidebar:
    st.header("System Vitals")
    stats = requests.get(f"{API_BASE}/stats").json()
    st.metric("Total Experiences", stats['total_events'])
    st.metric("Antibodies (Sigs)", stats['signatures'])
    st.success(f"Status: {stats['status']}")

# Tabs for Multiple Capabilities
tab_monitor, tab_malware, tab_evolution = st.tabs(["📈 Monitor", "🛡️ Malware Vault", "🧬 Evolution"])

with tab_monitor:
    st.subheader("Executive Ledger")
    ledger_data = requests.get(f"{API_BASE}/ledger").json()
    if ledger_data:
        df = pd.DataFrame(ledger_data)
        st.line_chart(df.set_index('timestamp')['anomaly_score'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Ledger is empty. Run the simulator or main engine.")

with tab_malware:
    st.subheader("L0: Threat Signatures")
    threats = requests.get(f"{API_BASE}/threats").json()
    st.table(threats)

with tab_evolution:
    st.subheader("L5: Model Retraining")
    st.write("Retrain the Innate OCSVM based on verified 'Normal' experiences.")
    if st.button("Trigger Neural Evolution"):
        st.warning("Feature coming: Connecting to L5 evolution script...")

# Auto-refresh
time.sleep(2)
st.rerun()