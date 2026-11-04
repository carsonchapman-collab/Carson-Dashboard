import streamlit as st
import requests
import json
import re
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Arch-Fab Operations Command",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# FUTURISTIC HUD THEME (Arch-Fab Crimson #A61C24 & Deep Charcoal)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 10% 5%, #18080a 0%, #0d0e12 35%, #050607 100%);
        color: #f3f4f6;
    }

    /* Top Command Header */
    .command-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px 24px;
        background: rgba(18, 20, 26, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(20px);
        margin-bottom: 22px;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.7);
    }

    /* High Visibility Department Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px !important;
        background: rgba(18, 20, 26, 0.95) !important;
        padding: 8px 12px !important;
        border-radius: 9999px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        width: fit-content !important;
        margin-bottom: 26px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.8) !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 9999px !important;
        padding: 10px 26px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [data-baseweb="tab"] p, 
    .stTabs [data-baseweb="tab"] div,
    .stTabs [data-baseweb="tab"] span {
        color: #e2e8f0 !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(166, 28, 36, 0.25) !important;
        border-color: rgba(166, 28, 36, 0.6) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8B141B 0%, #A61C24 60%, #C42630 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 4px 20px rgba(166, 28, 36, 0.65) !important;
    }
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] div,
    .stTabs [aria-selected="true"] span {
        color: #ffffff !important;
        font-weight: 900 !important;
    }

    /* High-Vis HUD Stat Cards */
    .hud-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(166, 28, 36, 0.06) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 22px 24px;
        backdrop-filter: blur(18px);
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.65);
        margin-bottom: 20px;
    }
    .hud-title {
        font-size: 0.8rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .hud-value {
        font-size: 2.3rem;
        font-weight: 900;
        color: #ffffff;
        margin: 8px 0 6px 0;
        line-height: 1.1;
    }
    .bar-bg {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 9999px;
        height: 8px;
        overflow: hidden;
        margin-top: 10px;
    }
    .bar-fill {
        background: linear-gradient(90deg, #8B141B 0%, #A61C24 65%, #EF4444 100%);
        height: 100%;
        border-radius: 9999px;
    }

    /* Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 11px;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 800;
    }
    .badge-crimson {
        background: rgba(166, 28, 36, 0.25);
        color: #fca5a5;
        border: 1px solid rgba(166, 28, 36, 0.55);
    }
    .badge-dark {
        background: rgba(255, 255, 255, 0.08);
        color: #e2e8f0;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .badge-green {
        background: rgba(34, 197, 94, 0.18);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.4);
    }
    .badge-orange {
        background: rgba(249, 115, 22, 0.18);
        color: #fb923c;
        border: 1px solid rgba(249, 115, 22, 0.4);
    }

    /* Dispatch Master Table */
    .dispatch-header {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-top-left-radius: 12px;
        border-top-right-radius: 12px;
        padding: 12px 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .dispatch-header-title {
        color: #38bdf8;
        font-size: 0.85rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        font-family: 'JetBrains Mono', monospace;
    }
    .dispatch-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        background: #090c12;
        border: 1px solid #1e293b;
        border-top: none;
    }
    .dispatch-table th {
        background: #111827;
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        padding: 12px 14px;
        text-align: left;
        border-bottom: 1px solid #1e293b;
    }
    .dispatch-table td {
        padding: 12px 14px;
        font-size: 0.85rem;
        color: #e2e8f0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        vertical-align: middle;
    }
    .dispatch-table tr:hover td {
        background: rgba(255, 255, 255, 0.025);
    }

    .color-swatch {
        display: inline-block;
        width: 14px;
        height: 14px;
        border-radius: 3px;
        margin-right: 8px;
        vertical-align: middle;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .color-silver { background: #94a3b8; }
    .color-bronze { background: #452c1e; }
    .color-black { background: #000000; border-color: #475569; }
    .color-blue { background: #1e3a8a; }
    .color-gray { background: #64748b; }

    .wo-link {
        color: #38bdf8;
        font-weight: 700;
        text-decoration: none;
        font-family: 'JetBrains Mono', monospace;
    }
    .crew-hrs {
        color: #38bdf8;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-tier-target {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.35);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .badge-tier-standard {
        background: rgba(148, 163, 184, 0.1);
        color: #cbd5e1;
        border: 1px solid rgba(148, 163, 184, 0.25);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .stButton > button {
        background: linear-gradient(135deg, #8B141B 0%, #A61C24 60%, #C42630 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 10px 22px !important;
        box-shadow: 0 4px 16px rgba(166, 28, 36, 0.4) !important;
    }
    header, #MainMenu, footer { visibility: hidden; }
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
powder_script_url = registry.get("Powder Coating", [{}])[0].get("url", "")

@st.cache_data(ttl=30)
def fetch_api_data(url):
    if not url:
        return None
    try:
        res = requests.get(url, timeout=30)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return None

master_data_raw = fetch_api_data(master_api_url)
master_data = master_data_raw.get("data") if master_data_raw and "data" in master_data_raw else master_data_raw

# Live fetch from the Powder Coating Apps Script
powder_data = fetch_api_data(powder_script_url)

# ==============================================================================
# HEADER WITH OFFICIAL BRAND ASSETS
# ==============================================================================
st.markdown("""
<div class="command-header">
    <div style="display:flex; align-items:center; gap:20px;">
        <!-- Official Arch-Fab High-Res Monogram Vector (Dark Mode Optimized) -->
        <svg width="68" height="68" viewBox="0 0 1080 1080" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M472 136H678L326 944H120L472 136Z" fill="#F8FAFC"/>
            <path d="M495 540H220L315 324H400L495 540Z" fill="#0D0E12"/>
            <path d="M622 372H998V496H758V610H958V730H758V1000H622V372Z" fill="#A61C24"/>
        </svg>
        <div>
            <div style="font-size:1.6rem; font-weight:900; letter-spacing:-0.03em; color:#ffffff; line-height:1.1;">
                ARCHITECTURAL FABRICATION
            </div>
            <div style="font-size:0.85rem; font-weight:600; color:#9ca3af; letter-spacing:0.04em;">
                OPERATIONS COMMAND CENTER &bull; SHOP FLOOR CONTROL
            </div>
        </div>
    </div>
    <div style="display:flex; align-items:center; gap:14px;">
        <span class="badge badge-green">
            <span style="height:7px; width:7px; background:#4ade80; border-radius:50%; display:inline-block; margin-right:6px; box-shadow:0 0 8px #4ade80;"></span>
            LIVE SYNC
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab_master, tab_powder, tab_logistics = st.tabs([
    "📊 Executive Master", 
    "🎨 Powder Dispatch Hub", 
    "🚚 Logistics & Loadout"
])

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

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Hardware Staging <span class="badge badge-crimson">{hw_pct}%</span></div>
            <div class="hud-value">{hw_comp} <span style="font-size:1.1rem; color:#6b7280; font-weight:600;">/ {hw_total}</span></div>
            <span class="badge badge-dark">{(hw_total - hw_comp)} Pending Action</span>
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
            <span class="badge badge-dark">{log.get('pending', 0)} Scheduled</span>
            <div class="bar-bg"><div class="bar-fill" style="width: {log_pct}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        plant_pct = int((hw_pct + pow_pct + log_pct) / 3) if hw_total > 0 else 0
        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Master Feed <span class="badge badge-green">ONLINE</span></div>
            <div class="hud-value">{plant_pct}%</div>
            <span class="badge badge-dark">Sync: {datetime.now().strftime('%I:%M %p')}</span>
            <div class="bar-bg"><div class="bar-fill" style="width: {plant_pct}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 2: POWDER COATING SHOP FLOOR DISPATCH DASHBOARD
# ==============================================================================
with tab_powder:
    # 1. Fetch from Powder Apps Script
    dispatch_jobs = powder_data.get("jobs", []) if powder_data and "jobs" in powder_data else []

    # 2. Fallback to Master Data Powder Schedule if Dispatch Tab endpoint is empty
    if not dispatch_jobs and master_data and "powder" in master_data:
        for idx, p in enumerate(master_data.get("powder", [])):
            dispatch_jobs.append({
                "seq": idx + 1,
                "color": p.get("color", "Standard"),
                "workOrder": p.get("woName", "N/A"),
                "release": p.get("release", ""),
                "item": "POWDER",
                "qty": 1,
                "estBatches": p.get("batches", 1.0),
                "crewHrs": 4.4,
                "priority": "5: Target Account (T)" if p.get("isPriority") else "6: Standard"
            })

    total_jobs_count = len(dispatch_jobs)
    total_scheduled_qty = int(sum([float(j.get("qty", 0)) for j in dispatch_jobs]))
    total_active_crew_hrs = round(sum([float(j.get("crewHrs", 0)) for j in dispatch_jobs]), 1)

    top_btn_col1, top_btn_col2 = st.columns([3, 1])
    with top_btn_col1:
        st.markdown("<h3 style='margin:0; font-weight:800;'>🎨 Powder Coating Shop Floor Dispatch</h3>", unsafe_allow_html=True)
    with top_btn_col2:
        if st.button("⚡ Recalculate Batch Analysis", use_container_width=True):
            with st.spinner("Executing Google Apps Script..."):
                try:
                    res = requests.get(f"{powder_script_url}?action=analyze", timeout=60)
                    st.success("Batch analysis recalculation completed!")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    def get_swatch_class(color_name):
        c = str(color_name).lower()
        if 'silver' in c: return 'color-silver'
        if 'bronze' in c: return 'color-bronze'
        if 'black' in c: return 'color-black'
        if '5003' in c or 'blue' in c: return 'color-blue'
        return 'color-gray'

    # Clean HTML builder - eliminates raw \n which broke the table in the screenshot
    rows_html = ""
    for job in dispatch_jobs:
        # Sanitize strings to prevent breaking HTML inside table cells
        color_raw = str(job.get("color", "Standard")).replace("\n", " &bull; ").strip()
        release_raw = str(job.get("release", "")).replace("\n", " ").strip()
        wo_raw = str(job.get("workOrder", "")).replace("\n", "").strip()
        item_raw = str(job.get("item", "DEFAULT")).replace("\n", "").strip()
        
        swatch = get_swatch_class(color_raw)
        prio = str(job.get("priority", "6: Standard")).replace("\n", "").strip()
        prio_badge = "badge-tier-target" if "Target" in prio or "5" in prio else "badge-tier-standard"
        tag_html = f"<span class='tag-project'>{job.get('tag')}</span>" if "tag" in job and job.get("tag") else ""

        rows_html += f"<tr>" \
                     f"<td style='font-weight:700; color:#94a3b8;'>{job.get('seq')}</td>" \
                     f"<td><span class='color-swatch {swatch}'></span><span style='font-weight:600;'>{color_raw}</span></td>" \
                     f"<td><a href='#' class='wo-link'>{wo_raw}</a></td>" \
                     f"<td>{release_raw} {tag_html}</td>" \
                     f"<td style='font-weight:600; font-size:0.8rem; color:#94a3b8;'>{item_raw}</td>" \
                     f"<td style='text-align:center; font-weight:700;'>{job.get('qty')}</td>" \
                     f"<td style='text-align:center; font-family:\"JetBrains Mono\";'>{job.get('estBatches')}</td>" \
                     f"<td style='text-align:center;' class='crew-hrs'>{job.get('crewHrs')}</td>" \
                     f"<td><span class='{prio_badge}'>{prio}</span></td>" \
                     f"</tr>"

    if not rows_html:
        rows_html = "<tr><td colspan='9' style='text-align:center; padding:24px; color:#9ca3af;'>No jobs currently in active dispatch queue.</td></tr>"

    full_table_html = f"""
    <div class="dispatch-header">
        <span class="dispatch-header-title">■ REPORT SECTION 02 // ACTIVE MASTER DISPATCH QUEUE</span>
        <span style="color:#94a3b8; font-size:0.75rem; font-weight:700;">{total_jobs_count} OF {total_jobs_count} JOBS DISPLAYED &bull; GANG-SEQUENCED GRID</span>
    </div>
    <table class="dispatch-table">
        <thead>
            <tr>
                <th style="width:40px;">SEQ</th>
                <th>POWDER COLOR (GANG)</th>
                <th>WORK ORDER</th>
                <th>PRODUCTION RELEASE NAME</th>
                <th>WO ITEM</th>
                <th style="text-align:center;">QTY (UNITS)</th>
                <th style="text-align:center;">EST. BATCHES</th>
                <th style="text-align:center;">CREW HRS</th>
                <th>PRIORITY TIER</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    <div style="background:#0b0f19; border:1px solid #1e293b; border-top:none; border-radius:0 0 12px 12px; padding:12px 18px; display:flex; justify-content:space-between; font-size:0.75rem; font-weight:800; letter-spacing:0.06em; color:#94a3b8;">
        <div>TOTAL DISPATCHED WORK ORDERS: <span style="color:#ffffff;">{total_jobs_count}</span> &bull; TOTAL SCHEDULED QUANTITY: <span style="color:#ffffff;">{total_scheduled_qty} UNITS</span></div>
        <div>TOTAL ACTIVE CREW HOURS: <span style="color:#38bdf8; font-size:0.9rem;">{total_active_crew_hrs} HRS</span></div>
    </div>
    """
    
    st.markdown(full_table_html, unsafe_allow_html=True)

# ==============================================================================
# TAB 3: LOGISTICS & LOADOUT
# ==============================================================================
with tab_logistics:
    st.markdown("<h3 style='margin:0; font-weight:800;'>🚚 Logistics & Planned Loadout</h3>", unsafe_allow_html=True)
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    log_items = master_data.get("logistics", []) if master_data else []
    if log_items:
        df_log = pd.DataFrame(log_items)[["reqName", "project", "loadDate", "superintendent", "isLoaded"]]
        df_log.columns = ["Request", "Project", "Planned Date", "Superintendent", "Loaded"]
        st.dataframe(df_log, use_container_width=True, hide_index=True)
    else:
        st.info("No active logistics loadouts found.")
