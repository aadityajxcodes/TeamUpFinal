import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.project_functions import get_project_by_id, edit_project
from core.user_functions import get_user_by_id



def main():
    if 'user_id' not in st.session_state:
        st.warning("Please login first.")
        return

    if 'edit_proj_id' not in st.session_state:
        st.warning("Please select a project to edit from your profile.")
        return

    proj = get_project_by_id(st.session_state['edit_proj_id'])
    if not proj:
        st.error("Project not found.")
        return

    # Check if current user is owner
    if proj['owner'] != st.session_state['user_id']:
        st.error("Unauthorized to edit this project.")
        return

    st.header(f"Edit Project: {proj['title']}")

    title = st.text_input("Project Title", value=proj['title'])
    desc = st.text_area("Project Description", value=proj['desc'])
    skills = st.text_input("Required Skills (comma separated)", value=', '.join(proj['required_skills']))
    timeline = st.text_input("Project Timeline", value=proj['timeline'])

    if st.button("Save Changes"):
        skills_list = [s.strip() for s in skills.split(",")] if skills else []
        edit_project(proj['id'], title, desc, skills_list, timeline)
        st.success("Project updated successfully!")
        del st.session_state['edit_proj_id']
        st.rerun()
    
    if st.button("Cancel"):
        del st.session_state['edit_proj_id']
        st.rerun()
