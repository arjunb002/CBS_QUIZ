import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Load credentials from Streamlit secrets
creds_dict = st.secrets["gcp_service_account"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
client = gspread.authorize(creds)

# Open sheet
sheet = client.open_by_key("1XszJM6CQ72QqhJQr_YaX-ZCCHmtr_DYsINZbHX-Gx6c").sheet1

# --- Streamlit App ---
st.set_page_config(page_title="CBS Fit Quiz", layout="centered")
st.title("🎓 Are You a Fit for CBS's PGPMDS?")

# --- User Info ---
st.subheader("👤 Your Details")
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")

# --- Quiz ---
st.subheader("📋 Quiz (10 Questions)")
questions = [
    {"q": "What is the main language used in data science?", "options": ["Python", "C++", "Ruby"], "answer": "Python"},
    {"q": "SQL is used for?", "options": ["Drawing", "Data Queries", "Music Production"], "answer": "Data Queries"},
    {"q": "Time series data involves?", "options": ["Geographical data", "Time-stamped data", "Random numbers"], "answer": "Time-stamped data"},
    {"q": "What does Hadoop handle?", "options": ["Emails", "Big Data", "Graphic Design"], "answer": "Big Data"},
    {"q": "Which is a data visualization tool?", "options": ["TensorFlow", "Excel", "Matplotlib"], "answer": "Matplotlib"},
    {"q": "What does MSE stand for in machine learning?", "options": ["Mean Squared Error", "Maximum Similarity Estimator", "Matrix Sampling Evaluation"], "answer": "Mean Squared Error"},
    {"q": "Blockchain is useful for?", "options": ["Secure Transactions", "Cooking", "Art"], "answer": "Secure Transactions"},
    {"q": "Data Analytics helps in?", "options": ["Decision Making", "Sleeping", "Text Editing"], "answer": "Decision Making"},
    {"q": "In business analytics, KPI stands for?", "options": ["Key Performance Indicator", "Knowledge Performance Insight", "Key Predictive Indicator"], "answer": "Key Performance Indicator"},
    {"q": "In a normal distribution, the mean is equal to?", "options": ["Median and Mode", "Only Mode", "Standard Deviation"], "answer": "Median and Mode"},
]

score = 0
responses = []

for i, q in enumerate(questions):
    st.write(f"**Q{i+1}:** {q['q']}")
    choice = st.radio("Select your answer:", options=[""] + q["options"], key=f"q{i}")
    responses.append(choice)
    if choice == q["answer"]:
        score += 1

# --- Submit Button ---
if st.button("Submit"):
    if not name or not email or not phone:
        st.warning("Please fill in all the details before submitting.")
    elif "" in responses:
        st.warning("Please answer all questions before submitting.")
    else:
        st.success(f"🎯 You scored {score}/10")

        if score >= 7:
            st.info("🔥 You're a perfect fit for CBS PGPMDS!")
        elif 4 <= score < 7:
            st.info("👍 You’re good to go for the course!")
        else:
            st.info("📘 Apply and level up your data knowledge!")

        # Save to Google Sheet
        row = [name, email, phone, score] + responses
        sheet.append_row(row)
        st.success("✅ Your response has been recorded!")


