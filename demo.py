import streamlit as st
import requests
import time

# CONFIG
API_URL = "http://localhost:8000/analyze"

st.set_page_config(page_title="LLM Guardian", page_icon="🛡️", layout="centered")

# HEADER
st.title("LLM Guardian")
st.markdown("### Enterprise Firewall for AI Models")
st.markdown("---")

# INPUT AREA
user_input = st.text_area("Enter Prompt for Inspection:", height=150, placeholder="Type a prompt here to test the security layer...")

# ACTION BUTTON
if st.button(" Inspect Prompt", type="primary", use_container_width=True):
    if not user_input:
        st.warning(" Please enter a prompt first.")
    else:
        # PROGRESS BAR ANIMATION (Fake "Scanning" effect for demo)
        progress_text = "Scanning..."
        my_bar = st.progress(0, text=progress_text)
        strea
        for percent_complete in range(100):
            time.sleep(0.01) # fast scan
            my_bar.progress(percent_complete + 1, text=progress_text)
        
        try:
            # CALL THE SERVER
            payload = {"message": user_input}
            response = requests.post(API_URL, json=payload)
            
            # CLEAR PROGRESS BAR
            my_bar.empty()
            
            if response.status_code == 200:
                data = response.json()
                verdict = data.get("verdict", "UNKNOWN")
                risk_score = data.get("risk_score", 0.0)
                
                # --- FINAL VERDICT DISPLAY ---
                if "BLOCK" in verdict:
                    st.error(" **THREAT DETECTED (BLOCKED)**")
                    st.markdown(f"**Security Risk Level:** `{risk_score * 100:.1f}%` (High)")
                    st.markdown("The prompt was intercepted and **did not** reach the LLM.")
                else:
                    st.success(" **SAFE PROMPT (ALLOWED)**")
                    st.markdown(f"**Security Risk Level:** `{risk_score * 100:.1f}%` (Low)")
                    st.markdown("Passed all checks. Forwarded to LLM.")
            
            else:
                st.error(f"Server Error: {response.status_code}")
                
        except Exception as e:
            st.error(f"Connection Failed. Is the backend running? Error: {e}")

# FOOTER
st.markdown("---")
st.caption("Secured by LLM Guardian Enterprise V2")