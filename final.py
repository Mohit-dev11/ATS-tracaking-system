

import streamlit as st
from PIL import Image
import plotly.express as px
import pandas as pd
import google.generativeai as genai
import pdf2image
import io
import os
import base64
from fpdf import FPDF
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define functions


def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


def calculate_score(response_text):
    # Example scoring logic based on keywords
    keywords = ['Python', 'SQL', 'JavaScript', 'Teamwork', 'Leadership']
    score = sum(1 for keyword in keywords if keyword in response_text)
    max_score = len(keywords)
    percentage_score = (score / max_score) * 100
    return percentage_score


def generate_score_chart(scores):
    df = pd.DataFrame(scores, columns=['Criteria', 'Score'])
    fig = px.bar(df, x='Criteria', y='Score',
                 title='Resume Scoring Analysis', text='Score', height=400)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(yaxis=dict(range=[0, 100]))
    return fig


def generate_cover_letter(job_title, company_name, job_description):
    prompt = f"""
    Write a professional cover letter for a job application.
    The position is {job_title} at {company_name}.
    The job description is as follows:
    {job_description}
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt])
    return response.text


# Streamlit App
st.set_page_config(page_title="ATS Resume Expert")

# Sidebar Navigation
option = st.sidebar.radio("Select an Option", [
                          "Resume Analysis", "Build Your Own Resume", "Job Search Recommendations", "Cover Letter Generator"])

# Resume Analysis Section
if option == "Resume Analysis":
    st.header("ATS Tracking System")
    input_text = st.text_area("Job Description: ", key="input")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF)...", type=["pdf"])

    if uploaded_file:
        st.write("PDF Uploaded Successfully")

    submit1 = st.button("Tell Me About the Resume")
    submit2 = st.button("Skills Gap Analysis")
    submit3 = st.button("Percentage Match")
    submit4 = st.button("How to Improve My Resume")
    submit5 = st.button("Visualize Resume Score")

    # Define prompts for analysis
    input_prompt1 = "Provide an evaluation on the candidate's alignment with the role."
    input_prompt2 = "Identify any skills gaps and improvement suggestions."
    input_prompt3 = "Evaluate and provide a match percentage, missing keywords, and final thoughts."
    input_prompt4 = "Suggest improvements on layout, content, and effectiveness."

    if submit1 and uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    elif submit2 and uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("Skills Gap Analysis")
        st.write(response)
    elif submit3 and uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("Match Percentage and Analysis")
        st.write(response)
    elif submit4 and uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        st.subheader("Resume Improvement Suggestions")
        st.write(response)
    elif submit5 and uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        score = calculate_score(response)
        st.subheader("Resume Scoring Visualization")
        st.write(f"Your Resume Score: **{score:.2f}%**")

        # Generate chart data
        criteria_scores = [
            ("Relevance", score * 0.8),  # Example weightage
            ("Keywords Match", score * 0.6),
            ("Content Clarity", score * 0.7),
            ("Overall ATS Compatibility", score)
        ]
        chart = generate_score_chart(criteria_scores)
        st.plotly_chart(chart)
# Build Your Own Resume Section
elif option == "Build Your Own Resume":
    st.header("Build Your Own Resume")
    template_choice = st.selectbox("Choose a Resume Template", [
                                   "Classic", "Modern", "Professional"])

    with st.form("resume_form"):
        st.subheader("Personal Information")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        linkedin = st.text_input(
            "LinkedIn Profile URL", placeholder="https://linkedin.com/in/yourprofile")
        st.subheader("Professional Summary")
        summary = st.text_area(
            "Summary", placeholder="Brief professional background...")
        st.subheader("Work Experience")
        job_title = st.text_input("Job Title")
        company = st.text_input("Company")
        job_duration = st.text_input("Duration (e.g., 2020 - 2022)")
        job_description = st.text_area(
            "Job Description", placeholder="Describe your responsibilities and achievements...")
        st.subheader("Education")
        education = st.text_input("School/Degree")
        grad_year = st.text_input("Graduation Year")
        st.subheader("Skills")
        skills = st.text_area("List your skills separated by commas",
                              placeholder="e.g., Python, Data Analysis, SQL")
        submit = st.form_submit_button("Generate Resume")

    if submit:
        # AI-Powered Content Suggestions (Optional)
        if not summary:
            summary = f"A highly motivated {job_title} with expertise in {
                skills.split(',')[0]} and a proven track record at {company}."

        # Generate Resume PDF
        pdf = FPDF()
        pdf.add_page()

        # Template: Classic
        if template_choice == "Classic":
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt="Resume", ln=True, align="C")
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, txt="Personal Information", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
            pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
            pdf.cell(200, 10, txt=f"Phone: {phone}", ln=True)
            pdf.cell(200, 10, txt=f"LinkedIn: {linkedin}", ln=True)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, txt="Professional Summary", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 10, txt=summary)

        # Template: Modern
        elif template_choice == "Modern":
            pdf.set_fill_color(200, 220, 255)
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt="Resume", ln=True, align="C", fill=True)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
            pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
            pdf.cell(200, 10, txt=f"Phone: {phone}", ln=True)
            pdf.cell(200, 10, txt=f"LinkedIn: {linkedin}", ln=True)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, txt="Summary", ln=True, fill=True)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 10, txt=summary)

        # Template: Professional
        elif template_choice == "Professional":
            pdf.set_font("Times", "B", 18)
            pdf.cell(200, 10, txt=name, ln=True, align="C")
            pdf.set_font("Times", "", 12)
            pdf.cell(200, 10, txt=f"Email: {email} | Phone: {
                     phone} | LinkedIn: {linkedin}", ln=True, align="C")
            pdf.set_font("Times", "B", 14)
            pdf.cell(200, 10, txt="Professional Summary", ln=True)
            pdf.set_font("Times", "", 12)
            pdf.multi_cell(0, 10, txt=summary)

        # Save and Allow Download
        pdf_output = f"{name.replace(' ', '_')}_Resume_{template_choice}.pdf"
        pdf.output(pdf_output)
        with open(pdf_output, "rb") as pdf_file:
            st.download_button("Download Your Resume",
                               pdf_file, file_name=pdf_output)


# Job Search Recommendations Section
elif option == "Job Search Recommendations":
    st.header("Job Search Recommendations")
    with st.form("job_search_form"):
        st.subheader("Enter Your Job Title and Skills")
        job_title = st.text_input(
            "Job Title", placeholder="e.g., Software Engineer")
        skills = st.text_area(
            "Skills", placeholder="e.g., Python, JavaScript, SQL")
        location = st.text_input("Preferred Location",
                                 placeholder="e.g., New York")
        submit = st.form_submit_button("Search Jobs")

    if submit:
        if job_title and skills:
            linkedin_search_url = f"https://www.linkedin.com/jobs/search/?keywords={
                job_title}&location={location}"
            st.write(
                f"Job listings for **{job_title}** with skills **{skills}** in **{location}**.")
            st.markdown(
                f"[Click here to search for jobs on LinkedIn]({linkedin_search_url})")
        else:
            st.error("Please provide both a Job Title and Skills for job search.")

    linkedin_profile = st.text_input(
        "Enter your LinkedIn Profile URL", placeholder="https://linkedin.com/in/yourprofile")
    if linkedin_profile:
        st.markdown(f"[View LinkedIn profile]({linkedin_profile})")

# Cover Letter Generator Section
elif option == "Cover Letter Generator":
    st.header("Cover Letter Generator")
    job_title = st.text_input("Job Title")
    company_name = st.text_input("Company Name")
    job_description = st.text_area("Job Description")

    if st.button("Generate Cover Letter"):
        if job_title and company_name and job_description:
            cover_letter = generate_cover_letter(
                job_title, company_name, job_description)
            st.subheader("Generated Cover Letter")
            st.write(cover_letter)
        else:
            st.error("Please fill in all fields.")
