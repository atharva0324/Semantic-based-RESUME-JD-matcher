import streamlit as st
import requests

st.set_page_config(page_title="Resume JD Matcher", page_icon="📄", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    .main { padding: 2rem 3rem; }
    .stTextArea textarea {
    border-radius: 10px;
    font-size: 14px;
    background-color: #161b22;
    color: #e6edf3 !important;
    border: 1px solid #1f6feb;
    caret-color: #e6edf3;
    }
    .stTextArea textarea::placeholder {
        color: #8b949e !important;
    }
label { color: #e6edf3 !important; }
    .stButton button {
        width: 100%;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 16px;
        font-weight: 600;
        background: linear-gradient(135deg, #1f6feb, #0d419d);
        color: white;
        border: none;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #388bfd, #1f6feb);
    }
    .stDivider { border-color: #30363d; }
    h1, h2, h3, h4 { color: #e6edf3 !important; }
    .skill-matched {
        display: inline-block;
        background-color: #1a7a4a22;
        color: #3fb950;
        border: 1px solid #3fb950;
        padding: 5px 14px;
        border-radius: 20px;
        margin: 4px;
        font-size: 13px;
        font-weight: 500;
    }
    .skill-missing {
        display: inline-block;
        background-color: #da363322;
        color: #f85149;
        border: 1px solid #f85149;
        padding: 5px 14px;
        border-radius: 20px;
        margin: 4px;
        font-size: 13px;
        font-weight: 500;
    }
    .section-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        min-height: 150px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 📄 Resume JD Matcher")
st.markdown("Paste a job description and your resume to see how well your skills match.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Job Description")
    jd = st.text_area("", placeholder="Paste the job description here...",
                      height=300, key="jd_input", label_visibility="collapsed")

with col2:
    st.markdown("#### Resume")
    resume = st.text_area("", placeholder="Paste your resume here...",
                          height=300, key="resume_input", label_visibility="collapsed")

st.markdown("")
_, btn_col, _ = st.columns([2, 1, 2])

with btn_col:
    match_btn = st.button("Analyze Match")

if match_btn:
    if not jd or not resume:
        st.warning("Please paste both a job description and your resume.")
    else:
        with st.spinner("Analyzing your resume..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/match",
                    json={"jd": jd, "resume": resume}
                )
                result = response.json()
                score = result['final_score']

                st.divider()

                if score >= 60:
                    color = "#3fb950"
                    bg = "#1a7a4a22"
                    border = "#3fb950"
                    verdict = "STRONG MATCH"
                    msg = "Your resume aligns well with this role."
                elif score >= 40:
                    color = "#d29922"
                    bg = "#d2992222"
                    border = "#d29922"
                    verdict = "MODERATE MATCH"
                    msg = "Consider tailoring your resume to better fit this role."
                else:
                    color = "#f85149"
                    bg = "#da363322"
                    border = "#f85149"
                    verdict = "LOW MATCH"
                    msg = "Significant gaps between your resume and this job description."

                st.markdown(f"""
                    <div style="background:{bg}; border:1px solid {border}; border-radius:14px; padding:2rem; margin-bottom:1.5rem;">
                        <div style="font-size:13px; font-weight:600; color:{color}; letter-spacing:1px;">{verdict}</div>
                        <div style="font-size:72px; font-weight:800; color:{color}; line-height:1.1;">{score}%</div>
                        <div style="font-size:15px; color:{color}; margin-top:0.5rem;">{msg}</div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("### Skill Analysis")

                col_matched, col_missing = st.columns(2)

                with col_matched:
                    st.markdown("#### ✅ Matched Skills")
                    if result['matched_skills']:
                        tags = " ".join([
                            f'<span class="skill-matched">{skill}</span>'
                            for skill in sorted(result['matched_skills'])
                        ])
                    else:
                        tags = "<span style='color:#888'>No exact matches found</span>"
                    st.markdown(f'<div class="section-box">{tags}</div>', unsafe_allow_html=True)

                with col_missing:
                    st.markdown("#### ❌ Missing Skills")
                    if result['missing_skills']:
                        tags = " ".join([
                            f'<span class="skill-missing">{skill}</span>'
                            for skill in sorted(result['missing_skills'])
                        ])
                    else:
                        tags = "<span style='color:#888'>No missing skills detected</span>"
                    st.markdown(f'<div class="section-box">{tags}</div>', unsafe_allow_html=True)

                st.caption(f"Inference time: {result['inference_time_seconds']}s")

            except Exception as e:
                st.error(f"Could not connect to API. Make sure the server is running. Error: {e}")