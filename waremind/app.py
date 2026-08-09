import streamlit as st
import pandas as pd
import json
import ollama
import re
from datetime import datetime

# --- DATABASE LOGIC ---
CSV_FILE = 'water_usage_data.csv'

def load_data():
    try:
        df = pd.read_csv(CSV_FILE)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=["Date", "Consumption_m3", "Total_Cost", "Period_Start", "Period_End"])

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# --- AI PROCESSING ---
def extract_json_from_text(text):
    """Robustly extract JSON even if the model forgets braces."""
    try:
        # 1. Try to find content between { }
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))

        # 2. Fallback: If no braces, try to wrap the text (fixes your specific error)
        # Clean up triple backticks or "json" labels if present
        clean_text = text.replace("```json", "").replace("```", "").strip()
        if not clean_text.startswith("{"):
            clean_text = "{" + clean_text + "}"

        return json.loads(clean_text)
    except Exception as e:
        print(f"Parsing error: {e}")
        return None

# --- UI CONFIG ---
st.set_page_config(page_title="WateRemind", layout="wide")

# Initialize Session State for form fields
if 'scanned_data' not in st.session_state:
    st.session_state.scanned_data = {"consumption": 0.0, "cost": 0.0, "start": None, "end": None}

# --- SECTION 4: CONFIGURATION (Sidebar) ---
with st.sidebar:
    st.header("⚙️ Household Profile")
    st.info("This context helps the AI give better advice.")
    hh_type = st.selectbox("Household Type", ["Apartment", "Terraced House", "Detached House", "Villa/Garden"])
    occupants = st.number_input("Number of People", min_value=1, max_value=20, value=2)
    has_garden = st.checkbox("Has Garden/Lawn?")
    has_pool = st.checkbox("Has Swimming Pool?")
    climate = st.text_input("Region/Climate", "Temperate")

# --- MAIN APP ---
st.title("WateRemind")
tab1, tab2, tab3 = st.tabs(["📤 Scan & Entry", "📊 History & CSV", "🤖 AI Coach"])

# --- SECTION 1: SCAN & MANUAL INPUT ---
with tab1:
    col_img, col_form = st.columns([1, 1])

    with col_img:
        st.subheader("1. Scan Receipt")
        uploaded_file = st.file_uploader("Upload Bill Image", type=['jpg', 'jpeg', 'png'])

        if uploaded_file:
            st.image(uploaded_file, caption="Target Receipt", use_container_width=True)
            if st.button("🚀 Run AI Scan"):
                with st.spinner("Ollama (LLaVA) is reading the receipt..."):
                    res = ollama.generate(
                        model='llava',
                        prompt="Extract: total consumption (numeric value), total cost (numeric value), service start date, and service end date. Return ONLY JSON with keys: consumption, cost, start, end. Use null for missing values.",
                        images=[uploaded_file.getvalue()]
                    )
                    parsed = extract_json_from_text(res['response'])
                    if parsed:
                        st.session_state.scanned_data = parsed
                        st.success("Data extracted! Review it in the form ->")
                    else:
                        st.error("Could not parse JSON. The AI said: " + res['response'])

    with col_form:
        st.subheader("2. Confirm & Save")
        with st.form("entry_form"):
            # Using session state to pre-fill if AI found data
            d_date = st.date_input("Record Date", datetime.now())
            d_cons = st.number_input("Consumption (m³)", value=float(st.session_state.scanned_data.get('consumption') or 0.0))
            d_cost = st.number_input("Total Cost ($)", value=float(st.session_state.scanned_data.get('cost') or 0.0))
            d_start = st.text_input("Period Start", value=str(st.session_state.scanned_data.get('start') or ""))
            d_end = st.text_input("Period End", value=str(st.session_state.scanned_data.get('end') or ""))

            submit_btn = st.form_submit_button("💾 Save Record")

            if submit_btn:
                df = load_data()
                new_row = pd.DataFrame([[d_date, d_cons, d_cost, d_start, d_end]],
                                       columns=["Date", "Consumption_m3", "Total_Cost", "Period_Start", "Period_End"])
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                st.balloons()
                st.success("Saved to CSV!")

# --- SECTION 2: VIEW DATA ---
with tab2:
    st.header("📈 Usage History")
    df_view = load_data()
    if not df_view.empty:
        st.dataframe(df_view, use_container_width=True)

        # Download Button
        csv_bytes = df_view.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", data=csv_bytes, file_name="water_usage.csv", mime="text/csv")

        # Simple Chart
        st.line_chart(df_view.set_index("Date")["Consumption_m3"])
    else:
        st.info("No records yet. Upload a bill to see your history.")

# --- SECTION 3: AI CHATBOT ---
with tab3:
    st.header("🤖 AI Water Coach")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if chat_input := st.chat_input("How does my usage look this month?"):
        st.session_state.messages.append({"role": "user", "content": chat_input})
        with st.chat_message("user"):
            st.markdown(chat_input)

        with st.chat_message("assistant"):
            # Construct context for Llama3
            history_str = df_view.tail(5).to_string() # Last 5 records
            context = (
                f"Household: {hh_type}, People: {occupants}, Garden: {has_garden}, Pool: {has_pool}, Climate: {climate}.\n"
                f"Recent History:\n{history_str}"
            )

            full_prompt = f"Context: {context}\nUser Question: {chat_input}\n\nHelpful, concise advice:"

            with st.spinner("Consulting AI Coach..."):
                response = ollama.generate(model='llama3', prompt=full_prompt)
                reply = response['response']
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
