import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.user_functions import get_user_by_id
from core.project_functions import get_projects_by_owner, handle_join_request
from core.user_functions import get_user_by_id as fetch_user



def main():
    if 'user_id' not in st.session_state:
        st.warning("Please login first.")
        return

    user = get_user_by_id(st.session_state['user_id'])
    st.header("Notifications and Join Requests")

    projects = get_projects_by_owner(user['id'])

    any_requests = False
    for proj in projects:
        if proj.get('join_requests'):
            st.subheader(f"Join Requests for '{proj['title']}'")
            for req_id in proj['join_requests']:
                req_user = fetch_user(req_id)
                st.write(f"{req_user['full_name']} ({req_user['username']}) wants to join.")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Accept {req_user['username']} for {proj['title']}", key=f"accept-{proj['id']}-{req_id}"):
                        handle_join_request(user['id'], proj['id'], req_id, True)
                        st.success("Request accepted.")
                        st.rerun()
                with col2:
                    if st.button(f"Reject {req_user['username']} for {proj['title']}", key=f"reject-{proj['id']}-{req_id}"):
                        handle_join_request(user['id'], proj['id'], req_id, False)
                        st.success("Request rejected.")
                        st.rerun()
                any_requests = True

    if not any_requests:
        st.info("No pending join requests.")

    st.subheader("Other Notifications")
    if user.get('notifications'):
        for note in user['notifications']:
            read_status = "🔵" if not note.get('read', False) else "⚪"
            st.write(f"{read_status} {note['message']}")
        
    else:
        st.write("No notifications")

    st.write("Use the sidebar to navigate back to your Profile.")
