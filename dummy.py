

import streamlit as st

# Streamlit App
st.set_page_config(page_title="Job Search Redirect")
st.header("Job Search Recommendations")

# Collecting User Data
with st.form("job_search_form"):
    st.subheader("Enter Your Job Title and Skills")
    job_title = st.text_input(
        "Job Title", placeholder="e.g., Software Engineer")
    skills = st.text_area(
        "Skills", placeholder="e.g., Python, JavaScript, SQL")
    location = st.text_input("Preferred Location",
                             placeholder="e.g., New York")
    submit = st.form_submit_button("Search Jobs")

# If the user submits the form
if submit:
    if job_title and skills:
        # Construct LinkedIn Job Search URL
        linkedin_search_url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={
            location}&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"

        # Provide redirection link
        st.write(f"Here are some job listings for **{
                 job_title}** with skills **{skills}** in **{location}**.")
        st.markdown(f"[Click here to search for jobs on LinkedIn](https://www.linkedin.com/jobs/search/?keywords={
                    job_title}&location={location})")
    else:
        st.error("Please provide both a Job Title and Skills for job search.") 


        # Display LinkedIn profile button (if the user has a LinkedIn URL)
linkedin_profile = st.text_input("Enter your LinkedIn Profile URL", placeholder="https://linkedin.com/in/yourprofile")

if linkedin_profile:
    st.markdown(f"[Click here to view your LinkedIn profile]({linkedin_profile})")

