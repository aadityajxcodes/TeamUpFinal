import streamlit as st
import sys
import os

# For parent directory imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.project_functions import get_all_projects, send_join_request
from core.user_functions import get_user_by_id

st.markdown("""
    <style>
    .project-card {
        background: #f7fafc;
        border: 1px solid #e1e7ef;
        border-radius: 14px;
        box-shadow: 0 3px 12px rgba(80, 120, 200, 0.08);
        padding: 1.3em 1em 1em 1em;
        margin-bottom: 1.5em;
        transition: box-shadow 0.2s;
    }
    .project-card:hover {
        box-shadow: 0 8px 28px 0 rgba(2,136,209,0.12);
        border: 1.5px solid #03a9f4;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    if 'user_id' not in st.session_state:
        st.warning("Please login first.")
        return

    st.header("Explore Projects")
    projects = get_all_projects() or []
    current_user_id = st.session_state['user_id']

    # -------- FILTER & SEARCH SECTION --------
    # Gather all unique skills across projects for filter options
    all_skills = sorted({skill for proj in projects for skill in proj.get('required_skills', [])})

    st.subheader("Search & Filters")
    search_text = st.text_input("Search by title or description", key="search_text")
    selected_skills = st.multiselect("Filter by required skills", all_skills, key="skills_filter")
    sort_by = st.selectbox("Sort projects by", ["Newest First", "Oldest First"], key="sort_by")

    # Apply search filter
    filtered_projects = projects
    if search_text.strip():
        search = search_text.lower()
        filtered_projects = [
            p for p in filtered_projects
            if search in p['title'].lower() or search in p['desc'].lower()
        ]

    # Apply skill filter
    if selected_skills:
        filtered_projects = [
            p for p in filtered_projects
            if any(skill in p.get('required_skills', []) for skill in selected_skills)
        ]

    # Apply sorting
    if sort_by == "Newest First":
        filtered_projects = sorted(filtered_projects, key=lambda x: x['id'], reverse=True)
    else:
        filtered_projects = sorted(filtered_projects, key=lambda x: x['id'])

    st.markdown("---")

    # ----------- DISPLAY PROJECTS -----------
    if filtered_projects:
        for proj in filtered_projects:
            owner = get_user_by_id(proj['owner'])

            participant_names = []
            for pid in proj.get('participants', []):
                userp = get_user_by_id(pid)
                if userp:
                    participant_names.append(userp['full_name'])

            with st.container():
                st.markdown(f'''
                    <div class="project-card">
                        <h4 style="margin-bottom:0.3em; color:#296eb4;">{proj['title']}</h4>
                        <div style="color:#333;margin-bottom:0.4em;">{proj['desc']}</div>
                        <div><strong>Required Skills:</strong> {', '.join(proj.get('required_skills', []))}</div>
                        <div><strong>Timeline:</strong> {proj.get('timeline', 'N/A')}</div>
                        <div><strong>Owner:</strong> {owner['full_name']} ({owner['username']})</div>
                        <div><strong>Participants:</strong> {", ".join(participant_names) if participant_names else "None yet"}</div>
                    </div>
                ''', unsafe_allow_html=True)

                # View owner profile button
                if st.button(f"View Owner Profile", key=f"profile-{proj['id']}"):
                    st.session_state['see_user_id'] = owner['id']
                    st.session_state['sidebar_nav'] = "Profile"
                    st.rerun()

                # Send join request
                if (
                    current_user_id not in proj.get('participants', [])
                    and current_user_id not in proj.get('join_requests', [])
                    and current_user_id != owner['id']
                ):
                    if st.button(f"Send Join Request to '{proj['title']}'", key=f"join-{proj['id']}"):
                        send_join_request(current_user_id, proj['id'])
                        st.success("Join request sent!")
                        st.rerun()

                # Open dashboard button for participants
                if current_user_id in proj.get('participants', []):
                    if st.button(f"Open Dashboard ({proj['title']})", key=f"dash-{proj['id']}"):
                        st.session_state['view_project_id'] = proj['id']
                        st.session_state['sidebar_nav'] = "Project Dashboard"
                        st.rerun()

            st.markdown("---")
    else:
        st.info("No projects matching your search and filters.")

    st.write("Use the sidebar to navigate back to your Profile.")

if __name__ == "__main__":
    main()
