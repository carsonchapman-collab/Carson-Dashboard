import streamlit as st
import requests
import json
import os
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(
    page_title="Arch-Fab Operations Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# ARCH-FAB RED & BLACK GLASSMORPHISM CSS
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Matte Black & Charcoal Vignette Background */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #1a0808 0%, #0d0d0f 45%, #050505 100%);
        color: #f3f4f6;
    }

    /* Red & Smoke Frosted Glass Cards */
    .glass-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(200, 16, 46, 0.04) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 22px 24px;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 16px;
    }
    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(220, 38, 38, 0.45);
        box-shadow: 0 14px 35px rgba(220, 38, 38, 0.15);
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

    /* Pill Badges */
    .pill-badge {
        display: inline-flex;
        align-items: center;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    .pill-red {
        background: rgba(220, 38, 38, 0.18);
        color: #f87171;
        border: 1px solid rgba(220, 38, 38, 0.35);
    }
    .pill-gray {
        background: rgba(255, 255, 255, 0.07);
        color: #d1d5db;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    .pill-green {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    /* Red Primary Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #b91c1c 0%, #dc2626 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 8px 18px !important;
        box-shadow: 0 4px 15px rgba(220, 38, 38, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%) !important;
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.45) !important;
        transform: scale(1.02);
    }

    /* Top Segmented Navigation Pills */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(20, 20, 24, 0.7);
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
        background: linear-gradient(135deg, #991b1b 0%, #dc2626 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.35);
    }

    /* High-density Dataframe container */
    [data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(15, 15, 18, 0.6);
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
# HEADER WITH ARCH-FAB BRANDING & LOGO
# ==============================================================================
header_col1, header_col2 = st.columns([4, 1])

with header_col1:
    col_logo, col_text = st.columns([0.8, 4])
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=105)
        else:
            # High-res SVG fallback of the AF Swoosh logo
            st.markdown("""
            <svg width="105" height="75" viewBox="0 0 160 110" fill="none" xmlns="http://www.w3.org/2000/svg">
                <!-- Red Arc Swoosh -->
                <path d="M12 90C18 42 58 12 145 8C110 24 75 48 55 90C45 72 30 82 12 90Z" fill="#DC2626"/>
                <!-- Bold 'A' -->
                <path d="M48 95L75 22H92L119 95H102L96 79H71L65 95H48ZM76 65H91L83.5 43L76 65Z" fill="#FFFFFF"/>
                <!-- Bold 'F' overlapping in Red -->
                <path d="M104 38H138V50H118V61H134V73H118V95H104V38Z" fill="#DC2626"/>
            </svg>
            """, unsafe_allow_html=True)
            
    with col_text:
        st.markdown("<h1 style='margin-bottom:0px; font-weight:900; font-size:2.2rem; letter-spacing:-0.03em;'>ARCHITECTURAL FABRICATION</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#9ca3af; margin-top:-2px; font-weight:500;'>Shop Floor Operations & Automation Command Center</p>", unsafe_allow_html=True)

with header_col2:
    st.write("")
    if st.button("🔄 Sync Live Feed", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Department Navigation Tabs
tab_master, tab_powder = st.tabs(["📊 Executive Command", "🎨 Powder Operations"])

# ==============================================================================
# TAB 1: EXECUTIVE MASTER DASHBOARD
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

    # Top KPI Metrics Cards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-title">Hardware Staging <span class="pill-badge pill-red">{hw_pct}%</span></div>
            <div class="card-value">{hw_comp} <span style="font-size:1.1rem; color:#6b7280; font-weight:600;">/ {hw_total}</span></div>
            <span class="pill-badge pill-gray">{(hw_total - hw_comp)} Pending Action</span>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-title">Powder Queue <span class="pill-badge pill-red">{pow_pct}%</span></div>
            <div class="card-value">{pow_comp} <span style="font-size:1.1rem; color:#6b7280; font-weight:600;">/ {pow_total}</span></div>
            <span class="pill-badge pill-red">{pow_sum.get('required', 0)} Runs Active</span>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-title">Logistics Trucks <span class="pill-badge pill-red">{log_pct}%</span></div>
            <div class="card-value">{log_loaded} <span style="font-size:1.1rem; color:#6b7280; font-weight:600;">/ {log_total}</span></div>
            <span class="pill-badge pill-gray">{log.get('pending', 0)} In Loadout</span>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-title">Plant Sync <span class="pill-badge pill-green">ONLINE</span></div>
            <div class="card-value" style="font-size:1.6rem; padding-top:6px;">{datetime.now().strftime('%I:%M %p')}</div>
            <span class="pill-badge pill-gray">Google Cloud API</span>
        </div>
        """, unsafe_allow_html=True)

    # Visual Analytics Row (Red & Charcoal Themed Charts)
    col_chart, col_side = st.columns([2, 1])

    with col_chart:
        st.markdown("#### Weekly Milestone Progress")
        fig = go.Figure()
        categories = ['Hardware Staging', 'Powder Runs', 'Logistics Trucks']
        completed = [hw_comp, pow_comp, log_loaded]
        pending = [max(hw_total - hw_comp, 0), max(pow_total - pow_comp, 0), max(log_total - log_loaded, 0)]

        fig.add_trace(go.Bar(
            y=categories, x=completed, name='Completed', orientation='h',
            marker=dict(color='#DC2626', line=dict(color='rgba(255,255,255,0.15)', width=1))
        ))
        fig.add_trace(go.Bar(
            y=categories, x=pending, name='Remaining', orientation='h',
            marker=dict(color='rgba(255,255,255,0.06)', line=dict(color='rgba(255,255,255,0.1)', width=1))
        ))

        fig.update_layout(
            barmode='stack',
            height=260,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=20, t=10, b=20),
            font=dict(color='#9ca3af', family='Plus Jakarta Sans'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col_side:
        st.markdown("#### Aggregate Plant Throughput")
        gauge_val = int((hw_pct + pow_pct + log_pct) / 3) if hw_total > 0 else 0
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=gauge_val,
            number={'suffix': "%", 'font': {'color': '#ffffff', 'size': 38, 'weight': 'bold'}},
            gauge={
                'axis': {'range': [None, 100], 'tickcolor': "#6b7280"},
                'bar': {'color': "#DC2626"},
                'bgcolor': "rgba(255,255,255,0.04)",
                'borderwidth': 0,
            }
        ))
        gauge_fig.update_layout(
            height=260,
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(gauge_fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

    # Lower Data Tables
    t1, t2 = st.columns(2)
    with t1:
        st.markdown("#### 🔩 Hardware Staging Queue")
        hw_items = master_data.get("hardware", []) if master_data else []
        if hw_items:
            df_hw = pd.DataFrame(hw_items)[["release", "woName", "hwStatus", "dueDate"]]
            df_hw.columns = ["Release", "WO", "Status", "Due"]
            st.dataframe(df_hw, use_container_width=True, hide_index=True)
    with t2:
        st.markdown("#### 🚚 Logistics Dispatch")
        log_items = master_data.get("logistics", []) if master_data else []
        if log_items:
            df_log = pd.DataFrame(log_items)[["reqName", "project", "loadDate", "isLoaded"]]
            df_log.columns = ["Request", "Project", "Load Date", "Loaded"]
            st.dataframe(df_log, use_container_width=True, hide_index=True)

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
