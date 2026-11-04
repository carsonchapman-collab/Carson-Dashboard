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
        background: rgba(18, 20, 26, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        backdrop-filter: blur(20px);
        margin-bottom: 22px;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.7);
    }

    /* Floating Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(14, 16, 20, 0.9);
        padding: 8px 12px;
        border-radius: 9999px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        width: fit-content;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 9999px;
        padding: 10px 24px;
        color: #9ca3af;
        border: 1px solid transparent !important;
        font-weight: 700;
        font-size: 0.92rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8B141B 0%, #A61C24 60%, #C42630 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 18px rgba(166, 28, 36, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
    }

    /* High-Vis HUD Stat Cards */
    .hud-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.035) 0%, rgba(166, 28, 36, 0.05) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 20px 22px;
        backdrop-filter: blur(18px);
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.6);
        transition: transform 0.2s ease, border-color 0.2s ease;
        margin-bottom: 16px;
    }
    .hud-card:hover {
        transform: translateY(-3px);
        border-color: rgba(166, 28, 36, 0.6);
    }
    .hud-title {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #9ca3af;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .hud-value {
        font-size: 2.2rem;
        font-weight: 900;
        color: #ffffff;
        margin: 8px 0 6px 0;
        line-height: 1.1;
    }

    /* Grid Dispatch Table Styling */
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
        overflow: hidden;
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

    /* Color Swatches */
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
    .color-black { background: #000000; border-color: #334155; }
    .color-blue { background: #1e3a8a; }
    .color-gray { background: #64748b; }

    /* WO Links */
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
    .tag-project {
        background: #fef08a;
        color: #854d0e;
        font-size: 0.68rem;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 4px;
        margin-left: 6px;
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

# Live fetch from the new Powder Apps Script endpoint
powder_data = fetch_api_data(powder_script_url)

# ==============================================================================
# HEADER
# ==============================================================================
col_head_left, col_head_right = st.columns([4, 1.2])

with col_head_left:
    logo_col, text_col = st.columns([0.65, 4])
    with logo_col:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=78)
        elif os.path.exists("logo-icon.png"):
            st.image("logo-icon.png", width=78)
        else:
            st.markdown("""
            <div style="font-size:2.8rem; font-weight:900; line-height:0.9; color:#A61C24;">
                <span style="color:#ffffff;">A</span>F
            </div>
            """, unsafe_allow_html=True)

    with text_col:
        st.markdown("<h1 style='margin:0; padding:0; font-weight:900; font-size:2rem; letter-spacing:-0.03em;'>ARCHITECTURAL FABRICATION</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#9ca3af; margin-top:-4px; font-weight:600; font-size:0.88rem;'>Operations Hub &bull; Shop Floor Control</p>", unsafe_allow_html=True)

with col_head_right:
    st.write("")
    if st.button("🔄 Sync Live Feed", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Department Segmented Tabs
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
    pow_total = pow_sum.get("total", 0)
    pow_comp = pow_sum.get("complete", 0)
    log_total = log.get("total", 0)
    log_loaded = log.get("loaded", 0)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Hardware Staging</div>
            <div class="hud-value">{hw_comp} <span style="font-size:1.1rem; color:#6b7280;">/ {hw_total}</span></div>
            <span class="badge-tier-standard">{(hw_total - hw_comp)} Pending Action</span>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Powder Runs</div>
            <div class="hud-value">{pow_comp} <span style="font-size:1.1rem; color:#6b7280;">/ {pow_total}</span></div>
            <span class="badge-tier-target">{pow_sum.get('required', 0)} Active Queue</span>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Logistics Trucks</div>
            <div class="hud-value">{log_loaded} <span style="font-size:1.1rem; color:#6b7280;">/ {log_total}</span></div>
            <span class="badge-tier-standard">{log.get('pending', 0)} Scheduled</span>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="hud-card">
            <div class="hud-title">Master Feed</div>
            <div class="hud-value" style="font-size:1.6rem; padding-top:6px;">ONLINE</div>
            <span class="badge-tier-target">{datetime.now().strftime('%I:%M %p')} Sync</span>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 2: POWDER COATING SHOP FLOOR DISPATCH DASHBOARD
# ==============================================================================
with tab_powder:
    # Pull directly from live API if returned; fallback cleanly if syncing
    dispatch_jobs = powder_data.get("jobs", []) if powder_data and "jobs" in powder_data else []

    total_jobs_count = len(dispatch_jobs)
    total_scheduled_qty = int(sum([float(j.get("qty", 0)) for j in dispatch_jobs]))
    total_active_crew_hrs = round(sum([float(j.get("crewHrs", 0)) for j in dispatch_jobs]), 1)

    # Top Trigger Action Bar
    btn_c1, btn_c2 = st.columns([3, 1])
    with btn_c1:
        st.markdown("<h3 style='margin:0; font-weight:800;'>🎨 Powder Coating Shop Floor Dispatch</h3>", unsafe_allow_html=True)
    with btn_c2:
        if st.button("⚡ Recalculate Batch Analysis", use_container_width=True):
            with st.spinner("Executing Google Apps Script..."):
                try:
                    res = requests.get(f"{powder_script_url}?action=analyze", timeout=60)
                    st.success("Batch analysis recalculation finished!")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # High-Density Grid Container
    st.markdown(f"""
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
    """, unsafe_allow_html=True)

    def get_swatch_class(color_name):
        c = str(color_name).lower()
        if 'silver' in c: return 'color-silver'
        if 'bronze' in c: return 'color-bronze'
        if 'black' in c: return 'color-black'
        if '5003' in c or 'blue' in c: return 'color-blue'
        return 'color-gray'

    rows_html = ""
    for job in dispatch_jobs:
        swatch = get_swatch_class(job.get("color"))
        prio = str(job.get("priority", ""))
        prio_badge = "badge-tier-target" if "Target" in prio or "5" in prio else "badge-tier-standard"
        tag_html = f"<span class='tag-project'>{job.get('tag')}</span>" if "tag" in job and job.get("tag") else ""

        rows_html += f"""
        <tr>
            <td style="font-weight:700; color:#94a3b8;">{job.get('seq')}</td>
            <td><span class="color-swatch {swatch}"></span><span style="font-weight:600;">{job.get('color')}</span></td>
            <td><a href="#" class="wo-link">{job.get('workOrder')}</a></td>
            <td>{job.get('release')} {tag_html}</td>
            <td style="font-weight:600; font-size:0.8rem; color:#94a3b8;">{job.get('item')}</td>
            <td style="text-align:center; font-weight:700;">{job.get('qty')}</td>
            <td style="text-align:center; font-family:'JetBrains Mono';">{job.get('estBatches')}</td>
            <td style="text-align:center;" class="crew-hrs">{job.get('crewHrs')}</td>
            <td><span class="{prio_badge}">{prio}</span></td>
        </tr>
        """

    if not rows_html:
        rows_html = "<tr><td colspan='9' style='text-align:center; padding:24px; color:#9ca3af;'>No jobs currently in active dispatch queue.</td></tr>"

    st.markdown(rows_html + """
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # Footer Aggregates Bar
    st.markdown(f"""
    <div style="background:#0b0f19; border:1px solid #1e293b; border-top:none; border-radius:0 0 12px 12px; padding:12px 18px; display:flex; justify-content:space-between; font-size:0.75rem; font-weight:800; letter-spacing:0.06em; color:#94a3b8;">
        <div>TOTAL DISPATCHED WORK ORDERS: <span style="color:#ffffff;">{total_jobs_count}</span> &bull; TOTAL SCHEDULED QUANTITY: <span style="color:#ffffff;">{total_scheduled_qty} UNITS</span></div>
        <div>TOTAL ACTIVE CREW HOURS: <span style="color:#38bdf8; font-size:0.9rem;">{total_active_crew_hrs} HRS</span></div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 3: LOGISTICS & LOADOUT
# ==============================================================================
with tab_logistics:
    st.markdown("<h3 style='margin:0; font-weight:800;'>🚚 Logistics & Planned Loadout</h3>", unsafe_allow_html=True)
    log_items = master_data.get("logistics", []) if master_data else []
    if log_items:
        df_log = pd.DataFrame(log_items)[["reqName", "project", "loadDate", "superintendent", "isLoaded"]]
        df_log.columns = ["Request", "Project", "Planned Date", "Superintendent", "Loaded"]
        st.dataframe(df_log, use_container_width=True, hide_index=True)
    else:
        st.info("No active logistics loadouts.")
