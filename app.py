import streamlit as st
import requests
import json
import os
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Arch-Fab Operations Command",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# HIGH-VISIBILITY INDUSTRIAL HUD THEME (Crimson & Charcoal Glass)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Pure Deep Carbon Backdrop with Crimson Ambient Light */
    .stApp {
        background: radial-gradient(circle at 15% 10%, #20080a 0%, #0c0d10 40%, #050608 100%);
        color: #f3f4f6;
    }

    /* Top Command Header */
    .command-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 24px;
        background: rgba(18, 19, 24, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        backdrop-filter: blur(20px);
        margin-bottom: 24px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.7);
    }

    /* Floating Pill Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(14, 15, 18, 0.85);
        padding: 8px 12px;
        border-radius: 9999px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        width: fit-content;
        margin-bottom: 26px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 9999px;
        padding: 10px 26px;
        color: #9ca3af;
        border: 1px solid transparent !important;
        font-weight: 700;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff;
        border-color: rgba(166, 28, 36, 0.4) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8B141B 0%, #A61C24 60%, #C42630 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 18px rgba(166, 28, 36, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
    }

    /* Glowing HUD Metric Cards */
    .hud-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.035) 0%, rgba(166, 28, 36, 0.06) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 22px 24px;
        backdrop-filter: blur(18px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 16px;
    }
    .hud-card:hover {
        transform: translateY(-4px);
        border-color: rgba(166, 28, 36, 0.6);
        box-shadow: 0 14px 38px rgba(166, 28, 36, 0.3);
    }

    .hud-title {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        color: #9ca3af;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .hud-value {
        font-size: 2.4rem;
        font-weight: 900;
        color: #ffffff;
        margin: 10px 0 8px 0;
        line-height: 1.1;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Progress Indicators */
    .bar-bg {
        background: rgba(255, 255, 255, 0.07);
        border-radius: 9999px;
        height: 8px;
        overflow: hidden;
        margin-top: 10px;
    }
    .bar-fill {
        background: linear-gradient(90deg, #8B141B 0%, #A61C24 65%, #EF4444 100%);
        height: 100%;
        border-radius: 9999px;
        box-shadow: 0 0 10px rgba(220, 38, 38, 0.5);
    }

    /* Futuristic Status Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 11px;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.04em;
    }
    .badge-crimson {
        background: rgba(166, 28, 36, 0.22);
        color: #fca5a5;
        border: 1px solid rgba(166, 28, 36, 0.55);
    }
    .badge-dark {
        background: rgba(255, 255, 255, 0.06);
        color: #e5e7eb;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    .badge-green {
        background: rgba(34, 197, 94, 0.16);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.4);
    }
    .badge-orange {
        background: rgba(249, 115, 22, 0.16);
        color: #fb923c;
        border: 1px solid rgba(249, 115, 22, 0.4);
    }

    /* Action Trigger Button */
    .stButton > button {
        background: linear-gradient(135deg, #8B141B 0%, #A61C24 60%, #C42630 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 10px 22px !important;
        box-shadow: 0 4px 16px rgba(166, 28, 36, 0.4) !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.02em;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #A61C24 0%, #C42630 100%) !important;
        box-shadow: 0 6px 24px rgba(220, 38, 38, 0.6) !important;
        transform: scale(1.02);
    }

    /* High Visibility Dark Queue Cards (Replaces standard white tables) */
    .queue-row {
        background: rgba(18, 19, 23, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-left: 3px solid #A61C24;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.15s ease;
    }
    .queue-row:hover {
        background: rgba(26, 28, 34, 0.85);
        border-color: rgba(166, 28, 36, 0.4);
        transform: translateX(3px);
    }

    /* Hide standard Streamlit header elements for a native app feel */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA LOADERS & API SYNC
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
# FUTURISTIC COMMAND HEADER & LOGO INTEGRATION
# ==============================================================================
st.markdown("""
<div class="command-header">
    <div style="display:flex; align-items:center; gap:20px;">
        <svg width="65" height="58" viewBox="0 0 160 140" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Dynamic Crimson Arch Swoosh -->
            <path d="M10 120C15 60 65 18 150 15C110 32 75 62 50 120C40 98 25 110 10 120Z" fill="#A61C24"/>
            <!-- Italicized 'A' -->
            <path d="M38 125L75 28H98L132 125H112L104 104H72L64 125H38ZM77 86H98L87 56L77 86Z" fill="#F3F4F6"/>
            <!-- Bold Overlapping 'F' in Arch-Fab Crimson -->
            <path d="M96 52H142V67H115V78H136V92H115V125H96V52Z" fill="#A61C24"/>
        </svg>
        <div>
            <div style="font-size:1.6rem; font-weight:900; letter-spacing:-0.03em; color:#ffffff; line-height:1.1;">
                ARCHITECTURAL FABRICATION
            </div>
            <div style="font-size:0.85rem; font-weight:600; color:#9ca3af; letter-spacing:0.04em;">
                OPERATIONS COMMAND CENTER &bull; PLANT DISPATCH
            </div>
        </div>
    </div>
    <div style="display:flex; align-items:center; gap:14px;">
        <span class="badge badge-green" style="font-size:0.75rem;">
            <span style="height:7px; width:7px; background:#4ade80; border-radius:50%; display:inline-block; margin-right:6px; box-shadow:0 0 8px #4ade80;"></span>
            LIVE SYNC
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Floating Department Tabs (Each gets its own full dashboard)
tab_master, tab_powder, tab_logistics = st.tabs([
    "📊 Executive Command", 
    "🎨 Powder Coating", 
    "🚚 Logistics & Loadout"
])

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

    # Top KPI HUD Pods
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Hardware Staging <span class="badge badge-crimson">{hw_pct}%</span></div>
            <div class="hud-value">{hw_comp} <span style="font-size:1.1rem; color:#6b7280; font-weight:600;">/ {hw_total}</span></div>
            <span class="badge badge-dark">{(hw_total - hw_comp)} Pending Prep</span>
            <div class="bar-bg"><div class="bar-fill" style="width: {hw_pct}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Powder Queue <span class="badge badge-crimson">{pow_pct}%</span></div>
            <div class="hud-value">{pow_comp} <span style="font-size:1.1rem; color:#6b7280; font-weight:600;">/ {pow_total}</span></div>
            <span class="badge badge-orange">{pow_sum.get('required', 0)} Runs Active</span>
            <div class="bar-bg"><div class="bar-fill" style="width: {pow_pct}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Logistics Trucks <span class="badge badge-crimson">{log_pct}%</span></div>
            <div class="hud-value">{log_loaded} <span style="font-size:1.1rem; color:#6b7280; font-weight:600;">/ {log_total}</span></div>
            <span class="badge badge-dark">{log.get('pending', 0)} Awaiting Load</span>
            <div class="bar-bg"><div class="bar-fill" style="width: {log_pct}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        plant_pct = int((hw_pct + pow_pct + log_pct) / 3) if hw_total > 0 else 0
        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Plant Throughput <span class="badge badge-green">OPTIMAL</span></div>
            <div class="hud-value">{plant_pct}%</div>
            <span class="badge badge-dark">Synced {datetime.now().strftime('%I:%M %p')}</span>
            <div class="bar-bg"><div class="bar-fill" style="width: {plant_pct}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # High-Density Live Queues
    q_col1, q_col2 = st.columns(2)
    with q_col1:
        st.markdown("<h4 style='letter-spacing:0.04em;'>🔩 HARDWARE STAGING DISPATCH</h4>", unsafe_allow_html=True)
        hw_items = master_data.get("hardware", []) if master_data else []
        if hw_items:
            for item in hw_items[:6]:
                is_done = item.get("hwStatus", "").lower() == "complete"
                badge_class = "badge-green" if is_done else "badge-crimson"
                status_txt = "COMPLETE" if is_done else "REQUIRED"
                st.markdown(f"""
                <div class="queue-row">
                    <div>
                        <div style="font-weight:700; color:#ffffff; font-size:0.95rem;">{item.get('woName')} &bull; {item.get('release')}</div>
                        <div style="font-size:0.75rem; color:#9ca3af; margin-top:2px;">Item: {item.get('itemNumber', 'Hardware')} &bull; Due: {item.get('dueDate')}</div>
                    </div>
                    <span class="badge {badge_class}">{status_txt}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active hardware staging jobs.")

    with q_col2:
        st.markdown("<h4 style='letter-spacing:0.04em;'>🎨 POWDER COATING HIGH-PRIORITY RUNS</h4>", unsafe_allow_html=True)
        pow_items = master_data.get("powder", []) if master_data else []
        if pow_items:
            for item in pow_items[:6]:
                status = item.get("status", "Required").upper()
                badge_class = "badge-green" if "COMPLETE" in status else ("badge-crimson" if "REQUIRED" in status else "badge-orange")
                st.markdown(f"""
                <div class="queue-row">
                    <div>
                        <div style="font-weight:700; color:#ffffff; font-size:0.95rem;">{item.get('woName')} &bull; {item.get('color', 'Standard')}</div>
                        <div style="font-size:0.75rem; color:#9ca3af; margin-top:2px;">{item.get('batches', 1)} Batches &bull; {item.get('release')}</div>
                    </div>
                    <span class="badge {badge_class}">{status}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active powder coating jobs.")

# ==============================================================================
# TAB 2: POWDER COATING DEDICATED DASHBOARD
# ==============================================================================
with tab_powder:
    st.markdown("<h3 style='font-weight:800; letter-spacing:-0.02em;'>🎨 Powder Coating Operations & Dispatch Hub</h3>", unsafe_allow_html=True)

    # Department Metrics Bar
    pow_items = master_data.get("powder", []) if master_data else []
    total_batches = sum([float(p.get("batches") or 1) for p in pow_items])
    total_runs = len(pow_items)
    pending_runs = sum([1 for p in pow_items if p.get("status", "").lower() != "complete"])

    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Active Queue Jobs</div>
            <div class="hud-value">{total_runs}</div>
            <span class="badge badge-crimson">{pending_runs} Pending Oven Runs</span>
        </div>
        """, unsafe_allow_html=True)

    with p_col2:
        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Scheduled Batches</div>
            <div class="hud-value">{total_batches:.1f}</div>
            <span class="badge badge-dark">Capacity Target: 40/Wk</span>
        </div>
        """, unsafe_allow_html=True)

    with p_col3:
        st.markdown("""
        <div class="hud-card">
            <div class="hud-title">Color Transitions</div>
            <div class="hud-value">Light &rarr; Dark</div>
            <span class="badge badge-green">Gang Sequencing Active</span>
        </div>
        """, unsafe_allow_html=True)

    with p_col4:
        st.markdown("""
        <div class="hud-card">
            <div class="hud-title">Automation Trigger</div>
            <div class="hud-value" style="font-size:1.4rem; padding-top:8px;">Ready</div>
            <span class="badge badge-green">Web App Connected</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Automated Trigger Console
    col_trigger_desc, col_trigger_btn = st.columns([3, 1])
    with col_trigger_desc:
        st.markdown("#### ⚡ Batch & Labor Analysis Automation")
        st.caption("Aggregates actual labor hours, powder batches, and priority breakdown across all active Work Orders.")
    with col_trigger_btn:
        powder_scripts = registry.get("Powder Coating", [])
        if powder_scripts and st.button("▶ Run Labor Analysis", use_container_width=True):
            with st.spinner("Executing Google Apps Script..."):
                try:
                    res = requests.get(powder_scripts[0]["url"], timeout=60)
                    if res.status_code == 200:
                        data = res.json()
                        if data.get("status") == "success":
                            st.success("Batch analysis successfully updated in Google Sheets!")
                            s = data.get("summary", {})
                            m1, m2, m3 = st.columns(3)
                            m1.metric("WOs Processed", s.get("totalWOCount", 0))
                            m2.metric("Powder Batches", s.get("totalBatches", 0))
                            m3.metric("Labor Hours", round(s.get("totalLabor", 0), 1))
                        else:
                            st.error(data.get("message"))
                except Exception as err:
                    st.error(f"Error: {err}")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Full Powder Floor Dispatch
    st.markdown("#### 📋 Full Powder Schedule & Batch Dispatch")
    if pow_items:
        for p in pow_items:
            status = p.get("status", "Required").upper()
            badge_class = "badge-green" if "COMPLETE" in status else ("badge-crimson" if "REQUIRED" in status else "badge-orange")
            notes = p.get("notes", "No special instructions")
            st.markdown(f"""
            <div class="queue-row" style="margin-bottom:8px;">
                <div style="flex:2;">
                    <span style="font-weight:800; color:#ffffff; font-size:1.05rem;">{p.get('woName')}</span>
                    <span style="color:#9ca3af; font-size:0.85rem; margin-left:12px;">{p.get('release')}</span>
                    <div style="color:#6b7280; font-size:0.8rem; margin-top:3px;">{notes}</div>
                </div>
                <div style="flex:1; text-align:center;">
                    <span class="badge badge-dark" style="font-size:0.8rem;">🎨 {p.get('color', 'Standard')}</span>
                </div>
                <div style="flex:0.8; text-align:center; font-weight:800; color:#ffffff; font-size:1rem;">
                    {p.get('batches', 1)} <span style="font-size:0.75rem; color:#6b7280;">BATCHES</span>
                </div>
                <div style="flex:0.6; text-align:right;">
                    <span class="badge {badge_class}">{status}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No powder items found.")

# ==============================================================================
# TAB 3: LOGISTICS & LOADOUT DEDICATED DASHBOARD
# ==============================================================================
with tab_logistics:
    st.markdown("<h3 style='font-weight:800; letter-spacing:-0.02em;'>🚚 Logistics Dispatch & Truck Loadout</h3>", unsafe_allow_html=True)
    log_items = master_data.get("logistics", []) if master_data else []

    if log_items:
        for item in log_items:
            is_loaded = item.get("isLoaded", False)
            status_txt = "LOADED" if is_loaded else "SCHEDULED"
            badge_class = "badge-green" if is_loaded else "badge-crimson"
            st.markdown(f"""
            <div class="queue-row">
                <div>
                    <span style="font-weight:800; color:#ffffff; font-size:1rem;">{item.get('reqName')}</span>
                    <span style="color:#9ca3af; font-size:0.85rem; margin-left:12px;">{item.get('project')}</span>
                    <div style="color:#6b7280; font-size:0.8rem; margin-top:2px;">
                        Superintendent: {item.get('superintendent', 'N/A')} &bull; Target Load Date: {item.get('loadDate')}
                    </div>
                </div>
                <span class="badge {badge_class}">{status_txt}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No logistics requests active.")
