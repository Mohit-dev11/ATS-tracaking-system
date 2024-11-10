import streamlit as st
from PIL import Image
import google.generativeai as genai
import pdf2image
import io
import os
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the function for resume analysis
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

# Streamlit App
st.set_page_config(page_title="ATS Resume Expert")

# Sidebar Navigation
option = st.sidebar.radio("Select an Option", ["Resume Analysis", "Build Your Own Resume"])

# Resume Analysis Section
if option == "Resume Analysis":
    st.header("ATS Tracking System")
    input_text = st.text_area("Job Description: ", key="input")
    uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

    if uploaded_file is not None:
        st.write("PDF Uploaded Successfully")

    submit1 = st.button("Tell Me About the Resume")
    submit2 = st.button("Skills Gap Analysis")
    submit3 = st.button("Percentage match")
    submit4 = st.button("How to Improve My Resume")

    # Define prompts for analysis
    input_prompt1 = """
    You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
    """

    input_prompt2 = """
    Evaluate the resume and identify any skills gaps based on the job description. 
    Provide suggestions on how the candidate can improve their skills to better match the requirements.
    """

    input_prompt3 = """
    You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
    your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
    the job description. First the output should come as percentage and then keywords missing and last final thoughts.
    """

    input_prompt4 = """
    Provide constructive feedback on how the candidate can improve their resume. 
    Focus on layout, content, and any other aspects that could enhance its effectiveness.
    """

    if submit1:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload the resume")

    elif submit2:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt2, pdf_content, input_text)
            st.subheader("Skills Gap Analysis")
            st.write(response)
        else:
            st.write("Please upload the resume")

    elif submit3:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.write("Please upload the resume")

    elif submit4:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt4, pdf_content, input_text)
            st.subheader("Resume Improvement Suggestions")
            st.write(response)
        else:
            st.write("Please upload the resume")

# Build Your Own Resume Section
elif option == "Build Your Own Resume":
    st.header("Build Your Own Resume")

    # Collecting User Data for Resume Creation
    with st.form("resume_form"):
        st.subheader("Personal Information")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        linkedin = st.text_input("LinkedIn Profile URL", placeholder="https://linkedin.com/in/yourprofile")

        st.subheader("Professional Summary")
        summary = st.text_area("Summary", placeholder="Brief professional background...")

        st.subheader("Work Experience")
        job_title = st.text_input("Job Title")
        company = st.text_input("Company")
        job_duration = st.text_input("Duration (e.g., 2020 - 2022)")
        job_description = st.text_area("Job Description", placeholder="Describe your responsibilities and achievements...")

        st.subheader("Education")
        education = st.text_input("School/Degree")
        grad_year = st.text_input("Graduation Year")

        st.subheader("Skills")
        skills = st.text_area("List your skills separated by commas", placeholder="e.g., Python, Data Analysis, SQL")

        submit = st.form_submit_button("Generate Resume")

    # Generate PDF Resume (same as previous code)
    if submit:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()

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

        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt="Work Experience", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, txt=f"{job_title} at {company} ({job_duration})", ln=True)
        pdf.multi_cell(0, 10, txt=job_description)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt="Education", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, txt=f"{education} ({grad_year})", ln=True)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt="Skills", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, txt=skills)

        pdf_output = f"{name.replace(' ', '_')}_Resume.pdf"
        pdf.output(pdf_output)

        with open(pdf_output, "rb") as pdf_file:
            st.download_button("Download Your Resume", pdf_file, file_name=pdf_output)
