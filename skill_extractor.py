import re

SKILLS_DB = [
    "python", "java", "c++", "sql",
    "machine learning", "data analysis",
    "html", "css", "javascript",
    "flask", "django",
    "communication", "teamwork"
]

def extract_skills(text):
    text = text.lower()
    found = []

    for skill in SKILLS_DB:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found.append(skill)

    return found
