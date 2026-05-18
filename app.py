import streamlit as st
import matplotlib.pyplot as plt
import json
import os

from matcher import match_resume
from skill_extractor import extract_skills
from resume_parser import extract_text_from_pdf

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Resume Intelligence System",
    page_icon="🤖",
    layout="wide"
)

# =========================
# SIDEBAR BRANDING
# =========================
st.sidebar.markdown("""
# 🤖 AI Resume System
### Smart ATS + Resume Tools
---
""")


# =========================
# USER AUTH SYSTEM
# =========================
USER_FILE = "users.json"


def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


def login_system():
    st.sidebar.title("🔐 Login System")

    users = load_users()

    option = st.sidebar.radio("Select Option", ["Login", "Register"])

    if option == "Register":
        st.subheader("📝 Create Account")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Register"):
            if new_user in users:
                st.error("User already exists!")
            else:
                users[new_user] = new_pass
                save_users(users)
                st.success("Account created! Please login.")

    else:
        st.subheader("🔐 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state["logged_in"] = True
                st.session_state["user"] = username
                st.success("Login successful!")
            else:
                st.error("Invalid credentials")

# =========================
# OPTIONAL LOGIN SYSTEM
# =========================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Show login/register system
login_system()

# -------------------------
# USER STATUS
# -------------------------
if st.session_state["logged_in"]:
    st.sidebar.success(
        f"Logged in as: {st.session_state.get('user')}"
    )

    # Logout button
    if st.sidebar.button("🚪 Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

else:
    st.sidebar.info("Continuing as Guest 👤")




# =========================
# HEADER
# =========================
st.title("🤖 AI Resume Intelligence System")
st.markdown("### ATS Analyzer • Resume Improver • Resume Generator")





if st.session_state["logged_in"]:
    st.success(f"Welcome {st.session_state.get('user')} 👋")
else:
    st.success("Welcome Guest 👋")




st.sidebar.success(f"Logged in as: {st.session_state.get('user')}")

if st.sidebar.button("🚪 Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

st.divider()


# =========================
# MODE SELECTION
# =========================
mode = st.sidebar.radio(
    "🧠 Choose Feature",
    ["📊 Analyze Resume", "✨ Improve Resume", "📝 Generate Resume"]
)


# =========================
# FUNCTIONS
# =========================
def ai_suggestions(score, skills):
    suggestions = []

    if score < 40:
        suggestions.append("Add more job-related keywords.")
        suggestions.append("Improve experience section.")
    elif score < 70:
        suggestions.append("Add advanced technical skills.")
        suggestions.append("Include certifications/projects.")
    else:
        suggestions.append("Excellent resume. Tailor it for each job.")

    if len(skills) < 3:
        suggestions.append("Add more technical skills (Python, SQL, Cloud).")

    return suggestions


def improve_resume(resume_text, job_desc, skills):
    tips = []

    job_words = job_desc.lower().split()
    missing = []

    for w in job_words:
        if w.isalpha() and w not in resume_text.lower():
            missing.append(w)

    missing = list(set(missing))[:10]

    if missing:
        tips.append("Add keywords: " + ", ".join(missing))

    if len(skills) < 5:
        tips.append("Add more technical skills (APIs, Cloud, Tools).")

    tips.append("Use action verbs (Built, Developed, Designed).")
    tips.append("Add measurable impact (e.g., improved performance by 30%).")

    return tips


def generate_pdf(score, skills, suggestions):
    file_path = "resume_report.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("AI Resume Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Score: {score}%", styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Skills: " + ", ".join(skills), styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Suggestions:", styles["Heading2"]))

    for s in suggestions:
        content.append(Paragraph("• " + s, styles["Normal"]))

    doc.build(content)
    return file_path


# =========================
# 📊 ANALYZER
# =========================
if mode == "📊 Analyze Resume":

    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf", "txt"])

    with col2:
        job_desc = st.text_area("🧾 Paste Job Description")

    if uploaded_file and job_desc.strip():

        resume_text = extract_text_from_pdf(uploaded_file)

        st.subheader("📄 Resume Preview")
        st.write(resume_text[:1000])

        score = match_resume(resume_text, job_desc)
        skills = extract_skills(resume_text)
        suggestions = ai_suggestions(score, skills)

        st.divider()

        st.subheader("📊 Dashboard")

        c1, c2, c3 = st.columns(3)
        c1.metric("🎯 ATS Score", f"{score}%")
        c2.metric("🧠 Skills", len(skills))
        c3.metric("📌 Status", "Processed")

        st.subheader("🧠 Skills Found")
        st.success(", ".join(skills) if skills else "No skills detected")

        st.subheader("🤖 Suggestions")
        for s in suggestions:
            st.info("✨ " + s)

        st.subheader("📊 Score Graph")
        fig, ax = plt.subplots()
        ax.bar(["Match", "Gap"], [score, 100 - score])
        ax.set_ylim(0, 100)
        st.pyplot(fig)

        st.divider()

        if st.button("📥 Generate PDF Report"):
            file_path = generate_pdf(score, skills, suggestions)

            with open(file_path, "rb") as f:
                st.download_button(
                    "⬇ Download Report",
                    f,
                    file_name="AI_Resume_Report.pdf",
                    mime="application/pdf"
                )

    else:
        st.info("Upload resume and job description to start analysis")


# =========================
# ✨ IMPROVE
# =========================
elif mode == "✨ Improve Resume":

    st.subheader("✨ Resume Improvement Generator")

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])
    job_desc = st.text_area("Paste Job Description")

    if uploaded_file and job_desc:

        resume_text = extract_text_from_pdf(uploaded_file)
        skills = extract_skills(resume_text)

        tips = improve_resume(resume_text, job_desc, skills)

        st.subheader("🧠 Improvement Suggestions")

        for t in tips:
            st.success("✨ " + t)


# =========================
# 📝 GENERATOR
# =========================
elif mode == "📝 Generate Resume":

    st.subheader("📝 Resume Generator from Scratch")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    skills = st.text_area("Skills (comma separated)")
    experience = st.text_area("Experience")

    if st.button("Generate Resume"):

        resume = f"""
{name}
Email: {email}

------------------
SUMMARY
A motivated professional skilled in {skills}.

SKILLS
{skills}

EXPERIENCE
{experience}

------------------
Generated by AI Resume System
"""

        st.subheader("📄 Generated Resume")
        st.text_area("Resume Output", resume, height=300)

        st.download_button(
            "⬇ Download Resume",
            resume,
            file_name="generated_resume.txt"
        )


# =========================
# FOOTER
# =========================
st.divider()
st.markdown("""
### 🚀 AI Resume Intelligence System
Built with Streamlit + NLP + Machine Learning  
🎓 So this is our BCA Final Project 🥱😊🙈🤧
""")
