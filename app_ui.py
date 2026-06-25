import streamlit as st
import requests

st.set_page_config(
    page_title="Resume JD Matcher",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
    <style>
    .main { padding: 2rem 3rem; }
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        font-size: 14px;
    }
    .score-card {
        background: #f8f9fa;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .score-number {
        font-size: 64px;
        font-weight: 700;
        line-height: 1;
    }
    .score-label {
        font-size: 14px;
        color: #6c757d;
        margin-top: 0.5rem;
    }
    .meta-info {
        font-size: 12px;
        color: #adb5bd;
        margin-top: 1rem;
    }
    .stButton button {
        width: 100%;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 16px;
        font-weight: 600;
        background-color: #1a1a2e;
        color: white;
        border: none;
    }
    .stButton button:hover {
        background-color: #16213e;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("## Resume JD Matcher")
st.markdown("Paste a job description and your resume to see how well they match.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Job Description")
    jd = st.text_area("", placeholder="Paste the job description here...", height=300, key="jd", label_visibility="collapsed")

with col2:
    st.markdown("#### Resume")
    resume = st.text_area("", placeholder="Paste your resume here...", height=300, key="resume", label_visibility="collapsed")

st.markdown("")
_, btn_col, _ = st.columns([2, 1, 2])

with btn_col:
    match_btn = st.button("Analyze Match")

if match_btn:
    if not jd or not resume:
        st.warning("Please paste both a job description and your resume.")
    else:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/match",
                    json={"jd": jd, "resume": resume}
                )
                result = response.json()
                score = result["match_percentage"]

                st.divider()
                m1, m2, m3 = st.columns(3)

                with m1:
                    st.metric("Match Score", f"{score}%")

                with m2:
                    st.metric("Inference Time", f"{result['inference_time_seconds']}s")

                with m3:
                    st.metric("Model", result["model_used"])

                st.markdown("")

                if score >= 70:
                    st.success(f"Strong match! Your resume aligns well with this role.")
                elif score >= 50:
                    st.warning("Moderate match. Consider tailoring your resume to better fit this role.")
                else:
                    st.error("Low match. There are significant gaps between your resume and this job description.")

            except Exception as e:
                st.error(f"Could not connect to API. Make sure the server is running. Error: {e}")