import streamlit as st
import requests
import json
import os
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Arch-Fab Operations Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# OFFICIAL ARCH-FAB RED & BLACK THEME (#A61C24 + #0A0A0C)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 10% 10%, #17080a 0%, #0c0d10 40%, #060607 100%);
        color: #f3f4f6;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(166, 28, 36, 0.04) 100%);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 18px;
        padding: 22px 24px;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.65);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 16px;
    }
    .glass-card:hover {
        transform: translateY(-3px);
        border-color: rgba(166, 28, 36, 0.5);
        box-shadow: 0 12px 32px rgba(166, 28, 36, 0.22);
    }

    .card-title {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #9ca3af;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .card-value {
        font-size: 2.3rem;
        font-weight: 900;
        color: #ffffff;
        margin: 10px 0 6px 0;
        line-height: 1.1;
    }

    /* Status Pills */
    .pill-badge {
        display: inline-flex;
        align-items: center;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    .pill-red {
        background: rgba(166, 28, 36, 0.22);
        color: #fca5a5;
        border: 1px solid rgba(166, 28, 36, 0.45);
    }
    .pill-gray {
        background: rgba(255, 255, 255, 0.06);
        color: #d1d5db;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    .pill-green {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    /* Custom Progress Bars */
    .progress-bar-bg {
        background: rgba(255, 255, 255, 0.06);
        border-radius: 9999px;
        height: 10px;
        overflow: hidden;
        margin-top: 8px;
    }
    .progress-bar-fill {
        background: linear-gradient(90deg, #8B141B 0%, #A61C24 100%);
        height: 100%;
        border-radius: 9999px;
    }

    /* Arch-Fab Red Gradient Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #8B141B 0%, #A61C24 60%, #C42630 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 8px 18px !important;
        box-shadow: 0 4px 14px rgba(166, 28, 36, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #A61C24 0%, #C42630 100%) !important;
        box-shadow: 0 6px 20px rgba(196, 38, 48, 0.5) !important;
        transform: scale(1.02);
    }

    /* Top Navigation Pills */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(20, 20, 24, 0.75);
        padding: 6px 8px;
        border-radius: 9999px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        width: fit-content;
        margin-bottom: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 9999px;
        padding: 8px 22px;
        color: #9ca3af;
        border: none !important;
        font-weight: 700;
        font-size: 0.9rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8B141B 0%, #A61C24 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(166, 28, 36, 0.4);
    }

    [data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(14, 14, 18, 0.65);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA LOADERS
# ==============================================================================
@st.cache_data(ttl=60)
def load_registry():
    try:
        with open("scripts.json", "r") as f:
            return json.load(f)
    except:
        return {}

registry = load_registry()
master_api_url = registry.get("Master Config", {}).get("data_feed_url", "")

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
    except:
        pass
    return None

master_data = fetch_master_data(master_api_url)

# ==============================================================================
# HEADER WITH BRANDED LOGO
# ==============================================================================
header_col1, header_col2 = st.columns([4.2, 1])

with header_col1:
    col_logo, col_text = st.columns([0.65, 4])
    with col_logo:
        if os.path.exists("logo-icon.png"):
            st.image("logo-icon.png", width=75)
        elif os.path.exists("logo-banner.jpg"):
            st.image("logo-banner.jpg", width=140)
        else:
            st.markdown("""
            <svg width="78" height="78" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 85L38 15H54L80 85H64L58 70H34L28 85H12ZM38 56H54L46 34L38 56Z" fill="#FFFFFF"/>
                <path d="M52 38H88V50H68V58H84V70H68V95H52V38Z" fill="#A61C24"/>
            </svg>
            """, unsafe_allow_html=True)

    with col_text:
        st.markdown("<h1 style='margin-bottom:0px; font-weight:900; font-size:2.2rem; letter-spacing:-0.03em;'>ARCHITECTURAL FABRICATION</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#9ca3af; margin-top:-3px; font-weight:600;'>Operations & Automation Hub</p>", unsafe_allow_html=True)

with header_col2:
    st.write("")
    if st.button("🔄 Sync Live Feed", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Tabs
tab_master, tab_powder = st.tabs(["📊 Executive Command", "🎨 Powder Operations"])

# ==============================================================================
# TAB 1: EXECUTIVE COMMAND
# ==============================================================================
with tab_master:
    summary = master_data.get("summary", {}) if master_data else {}
    hw = summary.get("hardware", {})
    pow_sum = summary.get("powder", {})
    log = summary.get("logistics", {})

    hw_total = hw.get("total", 0)
    hw_comp = hw.get("complete", 0)
    hw_pct = int((hw_comp / hw_total * 100)) if hw_total > 0 else 0

    pow_total = pow_sum.get("total", 0)
    pow_comp = pow_sum.get("complete", 0)
    pow_pct = int((pow_comp / pow_total * 100)) if pow_total > 0 else 0

    log_total = log.get("total", 0)
    log_loaded = log.get("loaded", 0)
    log_pct = int((log_loaded / log_total * 100)) if log_total > 0 else 0

    # Metric Cards Row
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-title">Hardware Staging <span class="pill-badge pill-red">{hw_pct}%</span></div>
            <div class="card-value">{hw_comp} <span style="font-size:1.1rem; color:#6b7280; font-weight:600;">/ {hw_total}</span></div>
            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {hw_pct}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-title">Powder Queue <span class="pill-badge pill-red">{pow_pct}%</span></div>
            <div class="card-value">{pow_comp} <span style="font-size:1.1rem; color:#6b7280; font-weight:600;">/ {pow_total}</span></div>
            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {pow_pct}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-title">Logistics Trucks <span class="pill-badge pill-red">{log_pct}%</span></div>
            <div class="card-value">{log_loaded} <span style="font-size:1.1rem; color:#6b7280; font-weight:600;">/ {log_total}</span></div>
            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {log_pct}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-title">Plant Sync <span class="pill-badge pill-green">ONLINE</span></div>
            <div class="card-value" style="font-size:1.6rem; padding-top:6px;">{datetime.now().strftime('%I:%M %p')}</div>
            <span class="pill-badge pill-gray">Google Workspace API</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Data Tables
    t1, t2 = st.columns(2)
    with t1:
        st.markdown("#### 🔩 Hardware Staging Queue")
        hw_items = master_data.get("hardware", []) if master_data else []
        if hw_items:
            df_hw = pd.DataFrame(hw_items)[["release", "woName", "hwStatus", "dueDate"]]
            df_hw.columns = ["Release", "WO", "Status", "Due"]
            st.dataframe(df_hw, use_container_width=True, hide_index=True)
        else:
            st.info("No active hardware records.")

    with t2:
        st.markdown("#### 🚚 Logistics Dispatch")
        log_items = master_data.get("logistics", []) if master_data else []
        if log_items:
            df_log = pd.DataFrame(log_items)[["reqName", "project", "loadDate", "isLoaded"]]
            df_log.columns = ["Request", "Project", "Load Date", "Loaded"]
            st.dataframe(df_log, use_container_width=True, hide_index=True)
        else:
            st.info("No active logistics records.")

# ==============================================================================
# TAB 2: POWDER OPERATIONS
# ==============================================================================
with tab_powder:
    st.subheader("Powder Coating Batch Automations")
    powder_scripts = registry.get("Powder Coating", [])

    for idx, item in enumerate(powder_scripts):
        col_desc, col_btn = st.columns([3, 1])
        with col_desc:
            st.markdown(f"#### {item['name']}")
            st.caption(item.get("description", ""))
        with col_btn:
            btn_key = f"powder_run_{idx}"
            if st.button("▶ Run Script", key=btn_key, use_container_width=True):
                with st.spinner("Processing analysis..."):
                    try:
                        res = requests.get(item["url"], timeout=60)
                        if res.status_code == 200:
                            data = res.json()
                            if data.get("status") == "success":
                                st.success("Batch analysis complete!")
                                s = data.get("summary", {})
                                m1, m2, m3 = st.columns(3)
                                m1.metric("WOs Processed", s.get("totalWOCount", 0))
                                m2.metric("Powder Batches", s.get("totalBatches", 0))
                                m3.metric("Labor Hours", round(s.get("totalLabor", 0), 1))
                            else:
                                st.error(data.get("message"))
                    except Exception as err:
                        st.error(f"Failed: {err}")
