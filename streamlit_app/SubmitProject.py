import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.project_functions import add_project

def main():
    if 'user_id' not in st.session_state:
        st.warning("Please login first.")
        return

    st.header("Submit a New Project")

    title = st.text_input("Project Title")
    desc = st.text_area("Project Description")
    skills = st.text_input("Required Skills (comma separated)")
    timeline = st.text_input("Project Timeline")

    if st.button("Submit Project"):
        if not (title and desc):
            st.error("Please enter the required fields.")
            return
        skills_list = [s.strip() for s in skills.split(",")] if skills else []
        add_project(st.session_state['user_id'], title, desc, skills_list, timeline)
        st.success("Project submitted successfully!")
        st.rerun()
