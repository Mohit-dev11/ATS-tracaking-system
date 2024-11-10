import google.generativeai as genai
import os
import streamlit as st
from dotenv import load_dotenv

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the cover letter prompt
def generate_cover_letter(job_title, company_name, job_description):
    prompt = f"""
    Write a professional cover letter for a job application.
    The position is {job_title} at {company_name}.
    The job description is as follows:
    {job_description}
    """

    # Use Gemini to generate the cover letter
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt])
    return response.text

# Streamlit app for generating a cover letter
st.set_page_config(page_title="Cover Letter Generator")
st.header("Cover Letter Generator")

# Input fields
job_title = st.text_input("Job Title")
company_name = st.text_input("Company Name")
job_description = st.text_area("Job Description")

# Generate cover letter button
if st.button("Generate Cover Letter"):
    if job_title and company_name and job_description:
        cover_letter = generate_cover_letter(job_title, company_name, job_description)
        st.subheader("Generated Cover Letter")
        st.write(cover_letter)
    else:
        st.error("Please fill in all fields.")
