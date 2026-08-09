import streamlit as st
from google import genai
import pandas as pd
import os
from PIL import Image
import json
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential

# --- 1. CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyB7iPW7cIDY0mzbdxta9R8I7_hX14RsYNY"
PROJECT_NAME = "WateRemind"
client = genai.Client(api_key=GEMINI_API_KEY)
CSV_FILE = "wateremind_history.csv"
CONFIG_FILE = "household_config.json"

st.set_page_config(page_title=PROJECT_NAME, page_icon="💧", layout="wide")

# --- 2. HELPERS & STORAGE ---
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"house_type": "Apartment", "bathrooms": 1, "occupants": 1}

def save_config(config_dict):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_dict, f)

def safe_float(value):
    """Handles None, strings with symbols, and empty values safely."""
    if value is None:
        return 0.0
    try:
        clean_val = str(value).replace('$', '').replace(',', '').strip()
        return float(clean_val) if clean_val else 0.0
    except (ValueError, TypeError):
        return 0.0

def sanitize(text):
    """Removes commas from strings to prevent CSV corruption."""
    if text is None:
        return ""
    return str(text).replace(',', '').strip()

# Initialize Session States
if 'ai_results' not in st.session_state:
    st.session_state.ai_results = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def apply_ai_to_form():
    res = st.session_state.ai_results
    if res:
        st.session_state["f_acc"] = sanitize(res.get('account_number'))
        st.session_state["f_period"] = sanitize(res.get('period'))
        st.session_state["f_usage"] = safe_float(res.get('usage_m3'))
        st.session_state["f_water"] = safe_float(res.get('water_charge'))
        st.session_state["f_drain"] = safe_float(res.get('drainage_sanitation'))
        st.session_state["f_total"] = safe_float(res.get('total_due'))

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_ai_response(prompt, content):
    return client.models.generate_content(model="gemini-2.5-flash", contents=[prompt, content])

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("🏠 Household Profile")
    conf = load_config()
    h_options = ["Apartment", "Single Family Home", "Townhouse", "Multi-Family"]
    new_house = st.selectbox("Type", h_options, index=h_options.index(conf.get('house_type', "Apartment")))
    new_people = st.number_input("Occupants", min_value=1, value=conf.get('occupants', 1))

    if st.button("💾 Save Profile"):
        save_config({"house_type": new_house, "bathrooms": 1, "occupants": new_people})
        st.success("Saved!")

    st.divider()
    if st.button("🗑️ Reset All History"):
        if os.path.exists(CSV_FILE): os.remove(CSV_FILE)
        st.success("History wiped. Start fresh!")
        st.rerun()

st.title(f"💧 {PROJECT_NAME}")

tab_scan, tab_history, tab_chat = st.tabs(["📤 Scan & Save", "📊 History", "🤖 AI Consultant"])

# --- TAB 1: SCAN & SAVE ---
with tab_scan:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("1. AI Scanner")
        up = st.file_uploader("Upload Bill", type=["jpg", "png", "jpeg"])
        if up:
            img = Image.open(up)
            st.image(img, width='stretch')
            if st.button("🪄 Run Analysis"):
                with st.spinner("AI Reading..."):
                    try:
                        prompt = "Analyze SADM Bill. Return ONLY JSON: account_number, period, usage_m3, water_charge, drainage_sanitation, total_due."
                        resp = get_ai_response(prompt, img)
                        txt = resp.text.strip()
                        start, end = txt.find('{'), txt.rfind('}') + 1
                        if start != -1:
                            st.session_state.ai_results = json.loads(txt[start:end])
                            st.success("Scan Complete!")
                    except:
                        st.error("AI Busy. Try again.")

    with c2:
        st.subheader("2. AI Preview")
        if st.session_state.ai_results:
            res = st.session_state.ai_results
            st.metric("Usage", f"{res.get('usage_m3', 0)} m³")
            st.metric("Cost", f"${res.get('total_due', 0)}")
            if st.button("📋 Apply to Form"):
                apply_ai_to_form()
        else:
            st.info("No data scanned yet.")

    st.divider()

    st.subheader("3. Verification & Save")
    with st.form("main_form"):
        f_acc = st.text_input("Account (NIS)", key="f_acc")
        f_per = st.text_input("Period", key="f_period")

        col_a, col_b, col_c = st.columns(3)
        f_use = col_a.number_input("Usage (m³)", min_value=0.0, key="f_usage")
        f_wat = col_b.number_input("Water $", min_value=0.0, key="f_water")
        f_drn = col_c.number_input("Sewer $", min_value=0.0, key="f_drain")
        f_tot = st.number_input("Total $", min_value=0.0, key="f_total")

        if st.form_submit_button("💾 Save to History"):
            config = load_config()
            entry = {
                "date_recorded": datetime.now().strftime("%Y-%m-%d"),
                "house_type": config['house_type'],
                "occupants": config['occupants'],
                "account": sanitize(f_acc),
                "period": sanitize(f_per),
                "usage_m3": f_use,
                "water_cost": f_wat,
                "sewer_cost": f_drn,
                "total_cost": f_tot
            }
            df = pd.DataFrame([entry])
            df.to_csv(CSV_FILE, mode='a', index=False, header=not os.path.isfile(CSV_FILE))
            st.success("Record Saved!")
            st.balloons()

# --- TAB 2: HISTORY ---
with tab_history:
    if os.path.exists(CSV_FILE):
        try:
            # We use on_bad_lines='skip' as a last-resort safety measure
            h_df = pd.read_csv(CSV_FILE, on_bad_lines='skip')
            st.dataframe(h_df, width='stretch')
            if not h_df.empty and 'date_recorded' in h_df.columns:
                st.line_chart(h_df.set_index('date_recorded')['usage_m3'])
        except Exception as e:
            st.error("The CSV file is corrupted. Please reset it in the sidebar.")
    else:
        st.info("No data yet.")

# --- TAB 3: CONSULTANT ---
with tab_chat:
    st.subheader("🤖 Water Expert")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if user_in := st.chat_input("Ask a question..."):
        st.session_state.chat_history.append({"role": "user", "content": user_in})
        with st.chat_message("user"): st.markdown(user_in)

        with st.chat_message("assistant"):
            config = load_config()
            # Safety check for the consultant reading the CSV
            try:
                csv_data = pd.read_csv(CSV_FILE).tail(3).to_string()
            except:
                csv_data = "No history available."

            prompt = f"Monterrey SADM expert. House: {config['occupants']}. History: {csv_data}. Q: {user_in}"
            res = get_ai_response(prompt, "Advice")
            st.markdown(res.text)
            st.session_state.chat_history.append({"role": "assistant", "content": res.text})
