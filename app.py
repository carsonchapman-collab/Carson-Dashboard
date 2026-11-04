import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="Operations Command Center",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Central Operations & Automation Hub")
st.caption("Centralized launcher for departmental Google Apps Script automations")

# Load registry
try:
    with open("scripts.json", "r") as f:
        departments = json.load(f)
except Exception as e:
    st.error(f"Error reading scripts.json: {e}")
    departments = {}

if not departments:
    st.warning("No departments configured yet.")
else:
    # Create tabs dynamically based on the departments in scripts.json
    tab_names = list(departments.keys())
    tabs = st.tabs(tab_names)

    for tab, dept_name in zip(tabs, tab_names):
        with tab:
            st.subheader(f"{dept_name} Automations")
            script_list = departments[dept_name]

            for idx, item in enumerate(script_list):
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(f"### {item['name']}")
                    st.write(item.get("description", ""))

                with col2:
                    button_key = f"{dept_name}_{idx}"
                    if st.button("▶ Run Script", key=button_key, use_container_width=True):
                        with st.spinner("Executing Google Apps Script..."):
                            try:
                                res = requests.get(item["url"], timeout=60)
                                if res.status_code == 200:
                                    data = res.json()
                                    if data.get("status") == "success":
                                        st.success("Execution complete!")
                                        if "summary" in data:
                                            s = data["summary"]
                                            st.metric("Total WOs Processed", s.get("totalWOCount", 0))
                                            st.metric("Total Powder Batches", s.get("totalBatches", 0))
                                            st.metric("Total Labor Hours", round(s.get("totalLabor", 0), 1))
                                    else:
                                        st.error(f"Script reported error: {data.get('message')}")
                                else:
                                    st.error(f"HTTP Error {res.status_code}: {res.text}")
                            except Exception as err:
                                st.error(f"Request failed: {err}")

                st.divider()
