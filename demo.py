import streamlit as st
import time

st.set_page_config(page_title="LLM Guardian", page_icon="🛡️", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #050508; }
#MainMenu, footer, header { display: none !important; }
.block-container { padding-top: 0 !important; padding-bottom: 0 !important; max-width: 640px !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* Full-height centering */
.main-wrap {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem 1rem;
}

/* Glow orb behind shield */
.orb {
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    border-radius: 50%;
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -60%);
    pointer-events: none;
    animation: pulse 4s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:0.5;transform:translate(-50%,-60%) scale(1)} 50%{opacity:1;transform:translate(-50%,-60%) scale(1.15)} }

.shield { font-size: 3.5rem; display: block; text-align: center; margin-bottom: 0.6rem; filter: drop-shadow(0 0 20px rgba(99,102,241,0.8)); animation: float 3s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-7px)} }

.title { text-align: center; font-size: 2.6rem; font-weight: 900; letter-spacing: -1.5px; color: #e2e8f0; margin-bottom: 0.2rem; }
.sub   { text-align: center; color: #334155; font-size: 0.88rem; margin-bottom: 2rem; }

/* Input */
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px solid rgba(255,255,255,0.07) !important;
    border-radius: 18px !important;
    color: #e2e8f0 !important;
    font-size: 1rem !important;
    font-family: 'Inter', sans-serif !important;
    padding: 1.1rem 1.3rem !important;
    resize: none !important;
    line-height: 1.6 !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}
.stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.45) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.08) !important;
}
.stTextArea textarea::placeholder { color: #1e293b !important; }
.stTextArea label { display: none !important; }

/* Button */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important; border: none !important;
    border-radius: 14px !important; font-size: 1rem !important;
    font-weight: 600 !important; padding: 0.85rem !important;
    box-shadow: 0 4px 24px rgba(99,102,241,0.35) !important;
    transition: all 0.2s !important; margin-top: 0.5rem !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover { box-shadow: 0 8px 36px rgba(99,102,241,0.55) !important; transform: translateY(-1px) !important; }

/* Verdict cards */
.card {
    border-radius: 22px; padding: 2.4rem 2rem;
    text-align: center; margin-top: 1.5rem;
    animation: fadeup 0.35s ease;
    width: 100%;
}
.card-safe   { background: rgba(16,185,129,0.06); border: 1.5px solid rgba(16,185,129,0.22); box-shadow: 0 0 60px rgba(16,185,129,0.05); }
.card-danger { background: rgba(239,68,68,0.06);  border: 1.5px solid rgba(239,68,68,0.22);  box-shadow: 0 0 60px rgba(239,68,68,0.05); }
.card-review { background: rgba(245,158,11,0.06); border: 1.5px solid rgba(245,158,11,0.22); box-shadow: 0 0 60px rgba(245,158,11,0.05); }
@keyframes fadeup { from{opacity:0;transform:translateY(14px)} to{opacity:1;transform:translateY(0)} }

.v-icon { font-size: 3rem; display: block; margin-bottom: 0.5rem; }
.v-safe   { font-size: 2rem; font-weight: 900; color: #10b981; letter-spacing: -0.5px; }
.v-danger { font-size: 2rem; font-weight: 900; color: #ef4444; letter-spacing: -0.5px; }
.v-review { font-size: 2rem; font-weight: 900; color: #f59e0b; letter-spacing: -0.5px; }
.v-desc   { font-size: 0.88rem; color: #475569; margin-top: 0.4rem; line-height: 1.5; }

/* Risk bar */
.rbar-wrap { display:flex; align-items:center; gap:0.7rem; justify-content:center; margin-top:1.2rem; }
.rbar-track { width:130px; height:5px; background:rgba(255,255,255,0.05); border-radius:999px; overflow:hidden; }
.rbar-safe   { height:100%; border-radius:999px; background:linear-gradient(90deg,#10b981,#34d399); }
.rbar-danger { height:100%; border-radius:999px; background:linear-gradient(90deg,#ef4444,#f87171); }
.rbar-review { height:100%; border-radius:999px; background:linear-gradient(90deg,#f59e0b,#fbbf24); }
.rbar-lbl { font-size:0.72rem; color:#334155; font-weight:500; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def load_guardian():
    from detector import LLMGuardian
    return LLMGuardian()

with st.spinner(""):
    guardian = load_guardian()

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown('<div class="orb"></div>', unsafe_allow_html=True)
st.markdown('<span class="shield">🛡️</span>', unsafe_allow_html=True)
st.markdown('<div class="title">LLM Guardian</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Is your prompt safe?</div>', unsafe_allow_html=True)

prompt = st.text_area("p", height=140, placeholder="Type or paste your prompt here...", label_visibility="collapsed")
clicked = st.button("Check Prompt →")

if clicked:
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        pb = st.progress(0)
        for i in range(1, 101):
            time.sleep(0.006)
            pb.progress(i)
        pb.empty()

        result  = guardian.analyze(prompt.strip())
        verdict = result["verdict"]
        risk    = result["risk_score"]
        pct     = int(risk * 100)

        if verdict == "BLOCK":
            card, vcls, bar = "card-danger", "v-danger", "rbar-danger"
            icon, label, desc = "🚨", "Not Safe", "This prompt looks like a manipulation attempt. Blocked."
        elif verdict == "ALLOW":
            card, vcls, bar = "card-safe", "v-safe", "rbar-safe"
            icon, label, desc = "✅", "Safe", "No threats detected. This prompt is safe."
        else:
            card, vcls, bar = "card-review", "v-review", "rbar-review"
            icon, label, desc = "⚠️", "Suspicious", "Unusual patterns found. Treated as unsafe."

        st.markdown(f"""
        <div class="card {card}">
            <span class="v-icon">{icon}</span>
            <div class="{vcls}">{label}</div>
            <div class="v-desc">{desc}</div>
            <div class="rbar-wrap">
                <span class="rbar-lbl">Risk</span>
                <div class="rbar-track"><div class="{bar}" style="width:{pct}%"></div></div>
                <span class="rbar-lbl">{pct}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)