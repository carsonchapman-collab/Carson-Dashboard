import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Arch-Fab Operations Command Center",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Arch-Fab Operations & Automation Hub")

# Load configuration registry
@st.cache_data(ttl=60)
def load_registry():
    try:
        with open("scripts.json", "r") as f:
            return json.load(f)
    except Exception as e:
        return {}

registry = load_registry()
master_api_url = registry.get("Master Config", {}).get("data_feed_url", "")

# Fetch live operational data from Google Apps Script
@st.cache_data(ttl=30)
def fetch_master_data(url):
    if not url:
        return None
    try:
        res = requests.get(url, timeout=30)
        if res.status_code == 200:
            payload = res.json()
            if payload.get("status") == "success":
                return payload.get("data")
    except Exception as e:
        st.error(f"Error fetching live operations data: {e}")
    return None

master_data = fetch_master_data(master_api_url)

# Department Navigation Tabs
tab_master, tab_powder = st.tabs(["📊 Executive Master Dashboard", "🎨 Powder Coating"])

# ==============================================================================
# TAB 1: EXECUTIVE MASTER DASHBOARD
# ==============================================================================
with tab_master:
    st.subheader("Plant-Wide Weekly Production & Logistics Overview")

    if st.button("🔄 Refresh Master Data"):
        st.cache_data.clear()
        st.rerun()

    if master_data and "summary" in master_data:
        summary = master_data["summary"]
        hw = summary.get("hardware", {})
        pow_sum = summary.get("powder", {})
        log = summary.get("logistics", {})

        # Top KPI Metrics Row
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.metric(
                label="Hardware Staging",
                value=f"{hw.get('complete', 0)} / {hw.get('total', 0)}",
                delta=f"{hw.get('required', 0)} Required",
                delta_color="inverse" if hw.get('required', 0) > 0 else "normal"
            )
        with kpi2:
            st.metric(
                label="Powder Queue",
                value=f"{pow_sum.get('complete', 0)} / {pow_sum.get('total', 0)}",
                delta=f"{pow_sum.get('required', 0)} Pending",
                delta_color="inverse" if pow_sum.get('required', 0) > 0 else "normal"
            )
        with kpi3:
            st.metric(
                label="Logistics Loadout",
                value=f"{log.get('loaded', 0)} / {log.get('total', 0)}",
                delta=f"{log.get('pending', 0)} Awaiting Loading",
                delta_color="inverse" if log.get('pending', 0) > 0 else "normal"
            )
        with kpi4:
            st.metric(
                label="System Sync Time",
                value=master_data.get("timestamp", datetime.now().strftime("%H:%M:%S")),
                delta="Live Google Workspace Feed"
            )

        st.divider()

        # Detailed Department Sections
        col_hw, col_log = st.columns(2)

        with col_hw:
            st.markdown("### 🔩 Hardware Staging Queue")
            hw_items = master_data.get("hardware", [])
            if hw_items:
                df_hw = pd.DataFrame(hw_items)[["release", "woName", "hwStatus", "dueDate", "completeDate"]]
                df_hw.columns = ["Release", "Work Order", "Status", "Due Date", "Completed"]
                st.dataframe(df_hw, use_container_width=True, hide_index=True)
            else:
                st.info("No active hardware work orders found.")

        with col_log:
            st.markdown("### 🚚 Logistics & Truck Loadouts")
            log_items = master_data.get("logistics", [])
            if log_items:
                df_log = pd.DataFrame(log_items)[["reqName", "project", "loadDate", "superintendent", "isLoaded"]]
                df_log.columns = ["Request", "Project", "Planned Date", "Superintendent", "Loaded"]
                st.dataframe(df_log, use_container_width=True, hide_index=True)
            else:
                st.info("No active logistics loadouts found.")

        st.divider()
        st.markdown("### 🎨 Powder Coating Queue (This Week)")
        pow_items = master_data.get("powder", [])
        if pow_items:
            df_pow = pd.DataFrame(pow_items)[["release", "woName", "status", "color", "batches", "dueDate", "isPriority"]]
            df_pow.columns = ["Release", "Work Order", "Status", "Color", "Batches", "Due Date", "Priority"]
            st.dataframe(df_pow, use_container_width=True, hide_index=True)

    else:
        st.warning("Connecting to Master Data Feed... Verify sharing settings on the script if this does not resolve after a refresh.")

# ==============================================================================
# TAB 2: POWDER COATING AUTOMATIONS
# ==============================================================================
with tab_powder:
    st.subheader("Powder Coating Automations & Analysis")
    powder_scripts = registry.get("Powder Coating", [])

    for idx, item in enumerate(powder_scripts):
        col_desc, col_btn = st.columns([3, 1])
        with col_desc:
            st.markdown(f"#### {item['name']}")
            st.write(item.get("description", ""))
        with col_btn:
            btn_key = f"powder_run_{idx}"
            if st.button("▶ Run Script", key=btn_key, use_container_width=True):
                with st.spinner("Executing Google Apps Script..."):
                    try:
                        res = requests.get(item["url"], timeout=60)
                        if res.status_code == 200:
                            data = res.json()
                            if data.get("status") == "success":
                                st.success("Batch analysis complete!")
                                if "summary" in data:
                                    s = data["summary"]
                                    m1, m2, m3 = st.columns(3)
                                    m1.metric("WOs Processed", s.get("totalWOCount", 0))
                                    m2.metric("Powder Batches", s.get("totalBatches", 0))
                                    m3.metric("Labor Hours", round(s.get("totalLabor", 0), 1))
                            else:
                                st.error(f"Error reported: {data.get('message')}")
                        else:
                            st.error(f"HTTP Error {res.status_code}: {res.text}")
                    except Exception as err:
                        st.error(f"Request failed: {err}")
        st.divider()
