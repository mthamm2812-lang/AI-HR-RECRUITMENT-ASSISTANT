import tkinter as tk
from tkinter import messagebox, scrolledtext
import os

RESUME_FILE = "resumes/resume.txt"
# -------------------------------
# TOOL 1: Extract skills
# -------------------------------

def extract_skills(text):
    skills_list = [
        "python",
        "java",
        "c++",
        "sql",
        "html",
        "css",
        "javascript",
        "react",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "data science",
        "mongodb",
        "mysql",
        "git",
        "github",
        "spring boot",
        "communication",
        "teamwork"
    ]

    text = text.lower()
    found = []

    for skill in skills_list:
        if skill in text:
            found.append(skill)

    return found


# -------------------------------
# TOOL 2: Resume matching
# -------------------------------

def calculate_match(resume, job_description):

    resume_skills = extract_skills(resume)
    job_skills = extract_skills(job_description)

    if len(job_skills) == 0:
        return 0, resume_skills, []

    matched = []

    for skill in job_skills:
        if skill in resume_skills:
            matched.append(skill)

    score = int((len(matched) / len(job_skills)) * 100)

    missing = []

    for skill in job_skills:
        if skill not in resume_skills:
            missing.append(skill)

    return score, matched, missing


# -------------------------------
# TOOL 3: RAG Knowledge Base
# -------------------------------

knowledge_base = {
    "python": [
        "Python interview questions may focus on variables, functions, OOP and exception handling."
    ],

    "sql": [
        "SQL interview questions may include SELECT, JOIN, GROUP BY and subqueries."
    ],

    "java": [
        "Java interviews commonly cover OOP, inheritance, polymorphism and exception handling."
    ],

    "machine learning": [
        "Machine learning interviews may cover supervised learning, unsupervised learning and model evaluation."
    ],

    "communication": [
        "HR interviews commonly evaluate communication, teamwork, adaptability and problem solving."
    ]
}


def retrieve_questions(skills):

    questions = []

    for skill in skills:
        if skill in knowledge_base:
            questions.extend(knowledge_base[skill])

    return questions


# -------------------------------
# AGENT
# -------------------------------

def run_recruitment_agent():

    resume = resume_box.get("1.0", tk.END).strip()
    job = job_box.get("1.0", tk.END).strip()

    if not resume or not job:
        messagebox.showwarning(
            "Missing Information",
            "Please enter both Resume and Job Description."
        )
        return

    score, matched, missing = calculate_match(resume, job)

    resume_skills = extract_skills(resume)

    questions = []

    if matched:
        for skill in matched:
            questions.append(
                f"1. Explain your experience with {skill}."
            )

    questions.append(
        f"{len(questions) + 1}. Tell me about yourself."
    )

    questions.append(
        f"{len(questions) + 1}. Why do you want this job?"
    )

    questions.append(
        f"{len(questions) + 1}. What are your strengths?"
    )

    retrieved = retrieve_questions(matched)

    result = ""

    result += "===== AI HR RECRUITMENT ASSISTANT =====\n\n"

    result += f"Candidate Match Score: {score}%\n\n"

    if score >= 80:
       recommendation = "Strong Match - Recommended"
    elif score >= 60:
       recommendation = "Moderate Match - Consider"
    else:
       recommendation = "Low Match - Not Recommended"

    result += f"Recommendation: {recommendation}\n\n"

    result += "Skills Found in Resume:\n"

    if resume_skills:
        for skill in resume_skills:
            result += f"✓ {skill}\n"
    else:
        result += "No recognized skills found.\n"

    result += "\nMatched Skills:\n"

    if matched:
        for skill in matched:
            result += f"✓ {skill}\n"
    else:
        result += "No matching skills found.\n"

    result += "\nMissing Skills:\n"

    if missing:
        for skill in missing:
            result += f"✗ {skill}\n"
    else:
        result += "No major missing skills.\n"

    result += "\n===== INTERVIEW QUESTIONS =====\n"

    for question in questions:
        result += question + "\n"

    result += "\n===== RAG KNOWLEDGE RETRIEVAL =====\n"

    if retrieved:
        for item in retrieved:
            result += "• " + item + "\n"
    else:
        result += "No additional knowledge retrieved.\n"

    result += "\n===== AGENT ACTION =====\n"
    result += "Resume analysed successfully.\n"
    result += "Job description analysed successfully.\n"
    result += "Candidate-job matching completed.\n"
    result += "Interview questions generated.\n"

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)

# -------------------------------
# CLEAR FUNCTION
# -------------------------------
def load_resume():
    if os.path.exists(RESUME_FILE):
        with open(RESUME_FILE, "r", encoding="utf-8") as file:
            resume_box.insert(tk.END, file.read())

def clear_all():

    resume_box.delete("1.0", tk.END)
    job_box.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)

# -------------------------------
# GUI
# -------------------------------

# -------------------------------
# MODERN GUI
# -------------------------------

window = tk.Tk()
window.title("AI HR Recruitment Assistant")
window.geometry("1000x800")
window.configure(bg="#e8f0fe")

# Header
header = tk.Frame(window, bg="#6C63FF", height=80)
header.pack(fill="x")

title = tk.Label(
    header,
    text="🤖 AI HR Recruitment Assistant",
    font=("Arial", 24, "bold"),
    bg="#6C63FF",
    fg="white"
)
title.pack(pady=20)

# Main container
main_frame = tk.Frame(window, bg="#f4f6f8")
main_frame.pack(fill="both", expand=True, padx=25, pady=20)

# Resume section
resume_label = tk.Label(
    main_frame,
    text="📄 Candidate Resume",
    font=("Arial", 14, "bold"),
    bg="#f4f6f8"
)
resume_label.pack(anchor="w")

resume_box = scrolledtext.ScrolledText(
    main_frame,
    width=110,
    height=8,
    font=("Arial", 11),
    bg="#FFF8E7",
    fg="#333333",
    insertbackground="#333333",
    wrap=tk.WORD
)
resume_box.pack(fill="x", pady=(5, 15))

# Job section
job_label = tk.Label(
    main_frame,
    text="💼 Job Description",
    font=("Arial", 14, "bold"),
    bg="#f4f6f8"
)
job_label.pack(anchor="w")

job_box = scrolledtext.ScrolledText(
    main_frame,
    width=110,
    height=7,
    font=("Arial", 11),
    bg="#EFFFF4",
    fg="#333333",
    insertbackground="#333333",
    wrap=tk.WORD
)
job_box.pack(fill="x", pady=(5, 15))

# Buttons
button_frame = tk.Frame(main_frame, bg="#f4f6f8")
button_frame.pack(pady=5)

analyze_button = tk.Button(
    button_frame,
    text="🔍 ANALYZE RESUME",
    command=run_recruitment_agent,
    font=("Arial", 12, "bold"),
    bg="#6C63FF",
    fg="white",
    activebackground="#5848E8",
    padx=25,
    pady=10
)
analyze_button.grid(row=0, column=0, padx=10)

clear_button = tk.Button(
    button_frame,
    text="↻ CLEAR",
    command=clear_all,
    font=("Arial", 12, "bold"),
    bg="#FF9F43",
    fg="white",
    activebackground="#E58B2B",
    padx=25,
    pady=10
)
clear_button.grid(row=0, column=1, padx=10)

# Result section
result_label = tk.Label(
    main_frame,
    text="📊 AI Recruitment Result",
    font=("Arial", 14, "bold"),
    bg="#f4f6f8"
)
result_label.pack(anchor="w", pady=(15, 5))

output_box = scrolledtext.ScrolledText(
    main_frame,
    width=110,
    height=18,
    font=("Consolas", 10),
    wrap=tk.WORD
)
output_box.pack(fill="both", expand=True)
resume_box.insert(tk.END, """
Name: M. Thanalakshmi
Qualification: B.Tech (Information Technology)

Skills:
Python
Java
SQL
HTML
CSS
Machine Learning
MongoDB
Communication
Teamwork
""")

window.mainloop()