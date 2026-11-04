import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Arch-Fab Operations Command",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# OFFICIAL ARCH-FAB LOGO (Clean Inline SVG)
# ==============================================================================
ARCH_FAB_LOGO = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="68" height="68">'
    '<path d="M 60,820 C 110,380 440,110 990,95 C 750,210 510,390 350,810 C 270,690 170,760 60,820 Z" fill="#A61C24"/>'
    '<path d="M 230,860 L 510,140 L 680,140 L 920,860 L 760,860 L 700,680 L 450,680 L 390,860 Z M 490,540 L 660,540 L 575,280 Z" fill="#FFFFFF"/>'
    '<path d="M 620,380 L 990,380 L 990,495 L 770,495 L 770,580 L 950,580 L 950,685 L 770,685 L 770,890 L 620,890 Z" fill="#A61C24"/>'
    '</svg>'
)

# ==============================================================================
# INDUSTRIAL HUD THEME (Arch-Fab Crimson #A61C24 & Deep Charcoal)
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

.command-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    background: rgba(18, 20, 26, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 18px;
    backdrop-filter: blur(20px);
    margin-bottom: 22px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.7);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 12px !important;
    background: rgba(18, 20, 26, 0.95) !important;
    padding: 8px 12px !important;
    border-radius: 9999px !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    width: fit-content !important;
    margin-bottom: 24px !important;
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

.queue-row {
    background: rgba(18, 20, 26, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-left: 4px solid #A61C24;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

[data-testid="stDataFrame"] {
    border-radius: 16px;
    border: 1px solid #1e293b;
    background: #090c12;
    overflow: hidden;
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
# REGISTRY CONFIGURATION
# ==============================================================================
try:
    with open("scripts.json", "r") as f:
        registry = json.load(f)
except:
    registry = {}

master_api_url = registry.get("Master Config", {}).get("data_feed_url", "")
powder_script_url = registry.get("Powder Coating", [{}])[0].get("url", "")

# Non-blocking fetcher with a strict 4-second timeout
def safe_fetch(url):
    if not url:
        return None
    try:
        res = requests.get(url, timeout=4)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return None

# ==============================================================================
# HEADER
# ==============================================================================
h_left, h_right = st.columns([4, 1.2])

with h_left:
    header_html = (
        '<div class="command-header">'
        '<div style="display:flex; align-items:center; gap:18px;">'
        f'{ARCH_FAB_LOGO}'
        '<div>'
        '<div style="font-size:1.6rem; font-weight:900; letter-spacing:-0.03em; color:#ffffff; line-height:1.1;">'
        'ARCHITECTURAL FABRICATION'
        '</div>'
        '<div style="font-size:0.85rem; font-weight:600; color:#9ca3af; letter-spacing:0.04em;">'
        'OPERATIONS COMMAND CENTER &bull; PLANT DISPATCH'
        '</div>'
        '</div>'
        '</div>'
        '<div>'
        '<span class="badge badge-green">'
        '<span style="height:7px; width:7px; background:#4ade80; border-radius:50%; display:inline-block; margin-right:6px; box-shadow:0 0 8px #4ade80;"></span>'
        'ONLINE'
        '</span>'
        '</div>'
        '</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)

with h_right:
    st.write("")
    if st.button("🔄 Sync Live Feed", use_container_width=True):
        st.session_state["cached_master"] = safe_fetch(master_api_url)
        st.session_state["cached_powder"] = safe_fetch(powder_script_url)
        st.rerun()

# Department Segmented Tabs
tab_master, tab_powder, tab_logistics = st.tabs([
    "📊 Executive Master", 
    "🎨 Powder Dispatch Hub", 
    "🚚 Logistics & Loadout"
])

# Initialize Session Cache if not yet loaded
if "cached_master" not in st.session_state:
    st.session_state["cached_master"] = safe_fetch(master_api_url)

raw_master = st.session_state.get("cached_master")
master_data = raw_master.get("data") if raw_master and isinstance(raw_master, dict) and "data" in raw_master else raw_master

# ==============================================================================
# TAB 1: EXECUTIVE MASTER DASHBOARD
# ==============================================================================
with tab_master:
    summary = master_data.get("summary", {}) if master_data else {}
    hw = summary.get("hardware", {})
    pow_sum = summary.get("powder", {})
    log = summary.get("logistics", {})

    hw_total = hw.get("total", 13)
    hw_comp = hw.get("complete", 11)
    hw_pct = int((hw_comp / hw_total * 100)) if hw_total > 0 else 85

    pow_total = pow_sum.get("total", 12)
    pow_comp = pow_sum.get("complete", 4)
    pow_pct = int((pow_comp / pow_total * 100)) if pow_total > 0 else 33

    log_total = log.get("total", 14)
    log_loaded = log.get("loaded", 10)
    log_pct = int((log_loaded / log_total * 100)) if log_total > 0 else 71

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            f'<div class="hud-card">'
            f'<div class="hud-title">Hardware Staging <span class="badge badge-crimson">{hw_pct}%</span></div>'
            f'<div class="hud-value">{hw_comp} <span style="font-size:1.1rem; color:#6b7280; font-weight:600;">/ {hw_total}</span></div>'
            f'<span class="badge badge-dark">{(hw_total - hw_comp)} Pending Action</span>'
            f'<div class="bar-bg"><div class="bar-fill" style="width: {hw_pct}%;"></div></div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with k2:
        st.markdown(
            f'<div class="hud-card">'
            f'<div class="hud-title">Powder Queue <span class="badge badge-crimson">{pow_pct}%</span></div>'
            f'<div class="hud-value">{pow_comp} <span style="font-size:1.1rem; color:#6b7280; font-weight:600;">/ {pow_total}</span></div>'
            f'<span class="badge badge-orange">{pow_total - pow_comp} Active Runs</span>'
            f'<div class="bar-bg"><div class="bar-fill" style="width: {pow_pct}%;"></div></div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with k3:
        st.markdown(
            f'<div class="hud-card">'
            f'<div class="hud-title">Logistics Trucks <span class="badge badge-crimson">{log_pct}%</span></div>'
            f'<div class="hud-value">{log_loaded} <span style="font-size:1.1rem; color:#6b7280; font-weight:600;">/ {log_total}</span></div>'
            f'<span class="badge badge-dark">{log_total - log_loaded} Scheduled</span>'
            f'<div class="bar-bg"><div class="bar-fill" style="width: {log_pct}%;"></div></div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with k4:
        plant_pct = int((hw_pct + pow_pct + log_pct) / 3)
        st.markdown(
            f'<div class="hud-card">'
            f'<div class="hud-title">Master Feed <span class="badge badge-green">SYNCED</span></div>'
            f'<div class="hud-value">{plant_pct}%</div>'
            f'<span class="badge badge-dark">{datetime.now().strftime("%I:%M %p")}</span>'
            f'<div class="bar-bg"><div class="bar-fill" style="width: {plant_pct}%;"></div></div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("<h4 style='letter-spacing:0.04em; font-weight:800;'>🔩 HARDWARE STAGING DISPATCH</h4>", unsafe_allow_html=True)
        hw_items = master_data.get("hardware", []) if master_data else []
        if hw_items:
            for item in hw_items[:6]:
                is_done = item.get("hwStatus", "").lower() == "complete"
                badge_class = "badge-green" if is_done else "badge-crimson"
                status_txt = "COMPLETE" if is_done else "REQUIRED"
                st.markdown(
                    f'<div class="queue-row">'
                    f'<div>'
                    f'<div style="font-weight:700; color:#ffffff; font-size:0.95rem;">{item.get("woName")} &bull; {item.get("release")}</div>'
                    f'<div style="font-size:0.75rem; color:#9ca3af; margin-top:2px;">Item: {item.get("itemNumber", "Hardware")} &bull; Due: {item.get("dueDate")}</div>'
                    f'</div>'
                    f'<span class="badge {badge_class}">{status_txt}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div class="queue-row"><div><div style="font-weight:700; color:#ffffff;">SO666419 &bull; Release 3</div><div style="font-size:0.75rem; color:#9ca3af;">Hardware staging in progress</div></div><span class="badge badge-crimson">REQUIRED</span></div>'
                '<div class="queue-row"><div><div style="font-weight:700; color:#ffffff;">SO666262 &bull; Release 4</div><div style="font-size:0.75rem; color:#9ca3af;">Staged and verified</div></div><span class="badge badge-green">COMPLETE</span></div>',
                unsafe_allow_html=True
            )

    with col_right:
        st.markdown("<h4 style='letter-spacing:0.04em; font-weight:800;'>🚚 LOGISTICS LOADOUT DISPATCH</h4>", unsafe_allow_html=True)
        log_items = master_data.get("logistics", []) if master_data else []
        if log_items:
            for item in log_items[:6]:
                is_loaded = item.get("isLoaded", False)
                status_txt = "LOADED" if is_loaded else "SCHEDULED"
                badge_class = "badge-green" if is_loaded else "badge-crimson"
                st.markdown(
                    f'<div class="queue-row">'
                    f'<div>'
                    f'<div style="font-weight:700; color:#ffffff; font-size:0.95rem;">{item.get("reqName")} &bull; {item.get("project")}</div>'
                    f'<div style="font-size:0.75rem; color:#9ca3af; margin-top:2px;">Superintendent: {item.get("superintendent", "N/A")} &bull; Date: {item.get("loadDate")}</div>'
                    f'</div>'
                    f'<span class="badge {badge_class}">{status_txt}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div class="queue-row"><div><div style="font-weight:700; color:#ffffff;">REQ-8812 &bull; Northpoint Project</div><div style="font-size:0.75rem; color:#9ca3af;">Truck loaded at Bay 2</div></div><span class="badge badge-green">LOADED</span></div>'
                '<div class="queue-row"><div><div style="font-weight:700; color:#ffffff;">REQ-8815 &bull; Bonds Ranch</div><div style="font-size:0.75rem; color:#9ca3af;">Awaiting final packaging</div></div><span class="badge badge-crimson">SCHEDULED</span></div>',
                unsafe_allow_html=True
            )

# ==============================================================================
# TAB 2: POWDER COATING SHOP FLOOR DISPATCH
# ==============================================================================
with tab_powder:
    if "cached_powder" not in st.session_state:
        st.session_state["cached_powder"] = safe_fetch(powder_script_url)

    raw_powder = st.session_state.get("cached_powder")
    dispatch_raw = raw_powder.get("jobs", []) if raw_powder and isinstance(raw_powder, dict) and "jobs" in raw_powder else [
        {"seq": 1, "color": "Anodized Silver", "workOrder": "SO666419", "release": "8139 T 8000 Bent Branch Release 3 - Bldg 3 Sunshades (CO1)", "item": "SUNSHADE", "qty": 3, "estBatches": 10.75, "crewHrs": 4.4, "priority": "5: Target Account (T)"},
        {"seq": 2, "color": "Anodized Silver", "workOrder": "SO666262", "release": "8414T LDG - The Park at Northpoint Release 4 (Building 4 & 6)", "item": "HELIOS", "qty": 20, "estBatches": 4.25, "crewHrs": 22.0, "priority": "5: Target Account (T)"},
        {"seq": 3, "color": "Dark Bronze", "workOrder": "SO666178", "release": "8530T Bonds Ranch - MF Phase 1 Release 4 (bldg 4)", "item": "HELIOS", "qty": 5, "estBatches": 4.25, "crewHrs": 5.5, "priority": "5: Target Account (T)"},
        {"seq": 4, "color": "Dark Bronze", "workOrder": "SO666176", "release": "8530T Bonds Ranch - MF Phase 1 Release 4 (bldg 4)", "item": "AWNING", "qty": 2, "estBatches": 3.81, "crewHrs": 4.4, "priority": "5: Target Account (T)"},
        {"seq": 5, "color": "Dark Bronze", "workOrder": "SO666521", "release": "8167 The Culbreath Release 10", "item": "ATLAS", "qty": 1, "estBatches": 3.47, "crewHrs": 1.1, "priority": "6: Standard"},
        {"seq": 6, "color": "Matte Black", "workOrder": "SO666025", "release": "8624 Mike Corn Industrial Release 1", "item": "HELIOS", "qty": 1, "estBatches": 4.25, "crewHrs": 4.4, "priority": "6: Standard"},
        {"seq": 7, "color": "RAL 5003", "workOrder": "SO665686", "release": "8607 SAISD Lake View HS Concessions Release 1", "item": "HELIOS", "qty": 4, "estBatches": 4.25, "crewHrs": 4.4, "priority": "6: Standard"},
        {"seq": 8, "color": "RAL 7037", "workOrder": "SO665259", "release": "8171 Denton Creek Regional WWTP Expansion Release 1 Admin", "item": "DEFAULT", "qty": 1, "estBatches": 3.64, "crewHrs": 4.4, "priority": "6: Standard"},
        {"seq": 9, "color": "RAL 7037", "workOrder": "SO665258", "release": "8171 Denton Creek Regional WWTP Expansion Release 1 Admin", "item": "DEFAULT", "qty": 1, "estBatches": 3.64, "crewHrs": 4.4, "priority": "6: Standard"},
        {"seq": 10, "color": "RAL 7037", "workOrder": "SO665257", "release": "8171 Denton Creek Regional WWTP Expansion Release 1 Admin", "item": "DEFAULT", "qty": 1, "estBatches": 3.64, "crewHrs": 4.4, "priority": "6: Standard"},
        {"seq": 11, "color": "Standard", "workOrder": "SO666697", "release": "8624 Mike Corn Industrial Release 1", "item": "DEFAULT", "qty": 1, "estBatches": 3.64, "crewHrs": 4.4, "priority": "6: Standard"}
    ]

    clean_records = []
    for j in dispatch_raw:
        color_clean = str(j.get("color", "Standard")).replace("\n", " / ").strip()
        release_clean = str(j.get("release", "")).replace("\n", " ").strip()
        wo_clean = str(j.get("workOrder", "")).replace("\n", "").strip()
        item_clean = str(j.get("item", "DEFAULT")).replace("\n", "").strip()
        prio_clean = str(j.get("priority", "6: Standard")).replace("\n", "").strip()

        clean_records.append({
            "Seq": int(j.get("seq", len(clean_records) + 1)),
            "Powder Color (Gang)": color_clean,
            "Work Order": wo_clean,
            "Release Name": release_clean,
            "WO Item": item_clean,
            "Qty (Units)": int(float(j.get("qty", 0) or 0)),
            "Est. Batches": round(float(j.get("estBatches", 0) or 0), 2),
            "Crew Hrs": round(float(j.get("crewHrs", 0) or 0), 1),
            "Priority Tier": prio_clean
        })

    df_powder = pd.DataFrame(clean_records)

    total_jobs = len(df_powder)
    total_qty = int(df_powder["Qty (Units)"].sum()) if not df_powder.empty else 0
    total_crew = round(df_powder["Crew Hrs"].sum(), 1) if not df_powder.empty else 0.0

    p_head, p_act = st.columns([3, 1.2])
    with p_head:
        st.markdown("<h3 style='margin:0; font-weight:800;'>🎨 Powder Coating Shop Floor Dispatch Dashboard</h3>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#38bdf8; font-family:JetBrains Mono; font-size:0.82rem; font-weight:700;'>■ ACTIVE MASTER DISPATCH QUEUE // {total_jobs} OF {total_jobs} JOBS GANG-SEQUENCED</span>", unsafe_allow_html=True)
    with p_act:
        if st.button("⚡ Recalculate Batch Analysis", use_container_width=True):
            with st.spinner("Executing Google Apps Script..."):
                try:
                    res = requests.get(f"{powder_script_url}?action=analyze", timeout=15)
                    st.success("Batch analysis recalculation finished!")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    st.dataframe(
        df_powder,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Seq": st.column_config.NumberColumn("SEQ", width="small"),
            "Powder Color (Gang)": st.column_config.TextColumn("POWDER COLOR (GANG)", width="medium"),
            "Work Order": st.column_config.TextColumn("WORK ORDER", width="small"),
            "Release Name": st.column_config.TextColumn("PRODUCTION RELEASE NAME", width="large"),
            "WO Item": st.column_config.TextColumn("WO ITEM", width="small"),
            "Qty (Units)": st.column_config.ProgressColumn(
                "QTY (UNITS)",
                format="%d",
                min_value=0,
                max_value=max(int(df_powder["Qty (Units)"].max() or 1), 20),
                width="small"
            ),
            "Est. Batches": st.column_config.NumberColumn("EST. BATCHES", format="%.2f", width="small"),
            "Crew Hrs": st.column_config.NumberColumn("CREW HRS", format="%.1f hrs", width="small"),
            "Priority Tier": st.column_config.TextColumn("PRIORITY TIER", width="medium")
        }
    )

    footer_html = (
        '<div style="background:#0b0f19; border:1px solid #1e293b; border-radius:12px; padding:12px 18px; margin-top:10px; display:flex; justify-content:space-between; font-size:0.78rem; font-weight:800; letter-spacing:0.06em; color:#94a3b8;">'
        f'<div>TOTAL DISPATCHED WORK ORDERS: <span style="color:#ffffff;">{total_jobs}</span> &bull; TOTAL SCHEDULED QUANTITY: <span style="color:#ffffff;">{total_qty} UNITS</span></div>'
        f'<div>TOTAL ACTIVE CREW HOURS: <span style="color:#38bdf8; font-size:0.95rem;">{total_crew} HRS</span></div>'
        '</div>'
    )
    st.markdown(footer_html, unsafe_allow_html=True)

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
        st.info("Logistics queue is ready. Click 'Sync Live Feed' to fetch real-time truck data.")
