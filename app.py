import streamlit as st
import matplotlib.pyplot as plt
from matcher import match_resume
from skill_extractor import extract_skills

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Resume Analyzer Pro")
st.markdown("### Smart Resume Screening System (ATS + AI Powered)")
st.divider()

# ---------------- INPUT SECTION ----------------
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume (.pdf / .txt)", type=["pdf", "txt"])

with col2:
    job_desc = st.text_area("🧾 Paste Job Description")

# ---------------- HELPER: READ FILE ----------------
def read_file(file):
    if file.name.endswith(".txt"):
        return str(file.read(), "utf-8")
    elif file.name.endswith(".pdf"):
        import PyPDF2
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
        return text
    return ""

# ---------------- AI SUGGESTIONS ----------------
def ai_suggestions(score, skills):
    suggestions = []

    if score < 40:
        suggestions.append("Add more relevant keywords from job description.")
        suggestions.append("Improve project and experience details.")
    elif score < 70:
        suggestions.append("Good resume, but add advanced technical skills.")
        suggestions.append("Include certifications or internships.")
    else:
        suggestions.append("Excellent resume! Tailor it for specific roles.")

    if len(skills) < 3:
        suggestions.append("Add more technical skills like Python, SQL, etc.")

    return suggestions

# ---------------- MAIN LOGIC ----------------
if uploaded_file and job_desc:

    resume_text = read_file(uploaded_file)

    st.subheader("📄 Resume Preview")
    st.write(resume_text[:1000])

    # AI ANALYSIS
    score = match_resume(resume_text, job_desc)
    skills = extract_skills(resume_text)
    suggestions = ai_suggestions(score, skills)

    st.divider()
    st.subheader("📊 AI Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("🎯 Match Score", f"{score}%")
    col2.metric("🧠 Skills Found", len(skills))
    col3.metric("📌 Status", "Analyzed")

    # ---------------- SKILLS ----------------
    st.subheader("🧠 Extracted Skills")

    if skills:
        st.success(", ".join(skills))
    else:
        st.warning("No major skills detected")

    # ---------------- AI FEEDBACK ----------------
    st.subheader("🤖 AI Suggestions")

    for s in suggestions:
        st.info("✨ " + s)

    # ---------------- GRAPH ----------------
    st.subheader("📊 Score Visualization")

    fig, ax = plt.subplots()
    ax.bar(["Match Score", "Gap"], [score, 100 - score])
    ax.set_ylim(0, 100)
    st.pyplot(fig)

else:
    st.info("👆 Please upload resume and paste job description to start analysis")