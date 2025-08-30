
import streamlit as st
import sys
import os

# Add parent dir to sys.path for core imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.user_functions import get_user_by_id
from core.project_functions import get_projects_by_owner, get_project_by_id


st.markdown("""
    <style>
    .project-card {
        background: #f7fafc;
        border: 1px solid #d4e3fa;
        border-radius: 14px;
        box-shadow: 0 2px 12px 0 #9ecff963;
        padding: 1.3em 1em 1em 1em;
        margin-bottom: 1.5em;
        transition: box-shadow 0.23s, border-color 0.14s;
    }
    .project-card:hover {
        box-shadow: 0 8px 32px 0 #03a9f44d;
        border: 1.5px solid #03a9f4;
    }
    .proj-skills {
        margin: 0.5em 0 0.7em 0;
    }
    .proj-skill-tag {
        display: inline-block;
        background: #e6f3fd;
        border: 1px solid #90caf9;
        color: #1976d2;
        padding: 4px 13px 3.5px 13px;
        margin-right: 5px;
        border-radius: 8px;
        font-size: 0.99em;
        margin-bottom: 2px;
        font-weight: 500;
    }
    .proj-meta {
        color: #0288d1;
        font-size: 0.99em;
        margin-bottom: 2px;
    }
    .proj-participants {
        color: #444;
        margin-top: 7px;
        font-size: 0.98em;
    }
    .profile-section-title {
        font-family: inherit;
        color: #2166c1;
        font-size: 1.23rem;
        margin-top: 1.5em;
        margin-bottom: 0.3em;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Check if user is logged in
    if 'user_id' not in st.session_state:
        st.warning("Please login first.")
        return

  
    profile_id = st.session_state.get('see_user_id', st.session_state['user_id'])

    user = get_user_by_id(profile_id)
    if not user:
        st.error("User not found.")
        return
    

    st.markdown(f"<h2 style='color:#2166c1;margin-bottom:0.4em'>{user['full_name']}'s Profile</h2>", unsafe_allow_html=True)

    st.markdown(f"**Username:** {user['username']}")
    st.markdown(f"**Contact:** {user['contact']}")
    skills_html = " ".join(f'<span class="proj-skill-tag">{skill}</span>' for skill in user['skills']) if user['skills'] else "None"
    st.markdown(f"**Skills:** {skills_html}", unsafe_allow_html=True)

    st.markdown(f"**Bio:** {user['bio']}")

    #  Posted Projects 
    st.markdown('<div class="profile-section-title">Posted Projects</div>', unsafe_allow_html=True)
    projects = get_projects_by_owner(user['id'])

    for proj in projects:
        participant_names = []
        for participant_id in proj.get('participants', []):
            participant_user = get_user_by_id(participant_id)
            if participant_user:
                participant_names.append(participant_user['full_name'])
        participants_str = ", ".join(participant_names) if participant_names else "None yet"

        with st.container():
            st.markdown(f'''
                <div class="project-card">
                    <h4 style="margin-bottom:0.25em; color:#2166c1; font-weight:700;">
                        <span style="vertical-align:middle;">{proj["title"]}</span>
                    </h4>
                    <div style="color:#394264; margin-bottom:0.45em;">{proj["desc"]}</div>
                    <div class="proj-skills">
                        <span style="font-weight:500; color:#0288d1; margin-right:7px;">Skills:</span>
                        {''.join(f'<span class="proj-skill-tag">{skill}</span>' for skill in proj["required_skills"])}
                    </div>
                    <div class="proj-meta">🗓️ <b>Timeline:</b> {proj["timeline"]}</div>
                    <div class="proj-participants"><b>👥 Participants:</b> {participants_str}</div>
                </div>
            ''', unsafe_allow_html=True)
           
            if profile_id == st.session_state['user_id']:
                if st.button(f"Edit {proj['title']}", key=f"edit-{proj['id']}"):
                    st.session_state['edit_proj_id'] = proj['id']
                    st.session_state['sidebar_nav'] = "Edit Project"
                    st.rerun()

    # Joined Projects 
    joined_projects_ids = user.get('joined_projects', [])
    st.markdown('<div class="profile-section-title">Joined Projects</div>', unsafe_allow_html=True)
    if joined_projects_ids:
        for proj_id in joined_projects_ids:
            proj = get_project_by_id(proj_id)
            if proj:
                owner = get_user_by_id(proj["owner"])
                owner_name = owner["full_name"] if owner else "Unknown"
                with st.container():
                    st.markdown(f'''
                        <div class="project-card">
                            <h4 style="margin-bottom:0.25em; color:#2166c1; font-weight:700;">
                                <span style="vertical-align:middle;">{proj["title"]}</span>
                            </h4>
                            <div style="color:#394264; margin-bottom:0.45em;">{proj["desc"]}</div>
                            <div class="proj-skills">
                                <span style="font-weight:500; color:#0288d1; margin-right:7px;">Skills:</span>
                                {''.join(f'<span class="proj-skill-tag">{skill}</span>' for skill in proj["required_skills"])}
                            </div>
                            <div class="proj-meta">👑 <b>Owner:</b> {owner_name}</div>
                        </div>
                    ''', unsafe_allow_html=True)
    else:
        st.write("You have not joined any projects yet.")

    if profile_id != st.session_state['user_id']:
        if st.button("Back to my profile"):
            if 'see_user_id' in st.session_state:
                del st.session_state['see_user_id']
            st.session_state['sidebar_nav'] = "Profile"
            st.rerun()

    st.write("Use the sidebar for navigation.")

if __name__ == "__main__":
    main()
