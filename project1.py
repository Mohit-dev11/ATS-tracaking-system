import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# Streamlit App
st.set_page_config(page_title="Simple Resume Builder")
st.header("Build Your Resume")

# Collecting User Data
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

    # Profile Picture Upload
    profile_picture = st.file_uploader("Upload your profile picture", type=["jpg", "jpeg", "png"])

    submit = st.form_submit_button("Generate Resume")

# Generate PDF Resume
if submit:
    pdf = FPDF()
    pdf.add_page()

    # Add Profile Picture if uploaded
    if profile_picture:
        img = Image.open(profile_picture)
        img_path = "profile_picture.jpg"
        img.save(img_path)

        # Add image to PDF (adjust size and position)
        pdf.image(img_path, x=10, y=10, w=40, h=40)

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Resume", ln=True, align="C")

    # Personal Information
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Personal Information", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {phone}", ln=True)
    pdf.cell(200, 10, txt=f"LinkedIn: {linkedin}", ln=True)

    # Professional Summary
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Professional Summary", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, txt=summary)

    # Work Experience
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Work Experience", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, txt=f"{job_title} at {company} ({job_duration})", ln=True)
    pdf.multi_cell(0, 10, txt=job_description)

    # Education
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Education", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, txt=f"{education} ({grad_year})", ln=True)

    # Skills
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Skills", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, txt=skills)

    # Save the PDF
    pdf_output = f"{name.replace(' ', '_')}_Resume.pdf"
    pdf.output(pdf_output)

    # Display Download Link
    with open(pdf_output, "rb") as pdf_file:
        st.download_button("Download Your Resume", pdf_file, file_name=pdf_output)
