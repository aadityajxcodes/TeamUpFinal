
import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.project_functions import get_project_by_id, edit_project
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
    .kanban-col {
        background: #f6fbff;
        border: 1.6px solid #e1e7ef;
        border-radius: 14px;
        min-height: 260px;
        padding: 1em 0.9em;
        margin-bottom: 1.5em;
        box-shadow: 0 4px 18px 0 rgba(2,136,209,0.02);
        display: flex;
        flex-direction: column;
        gap: 0.5em;
    }
    .kanban-task {
        background: #eaf6fd;
        border-radius: 9px;
        border: 1px solid #b9e0fc;
        padding: 0.9em 0.7em;
        margin-bottom: 0.55em;
        font-size: 1rem;
        color: #245980;
        box-shadow: 0 2px 6px 0 rgba(2,136,209,0.04);
        transition: box-shadow .2s;
    }
    .kanban-task:hover {
        box-shadow: 0 6px 22px 0 rgba(2,136,209,0.13);
        background: #d1eaff;
        border: 1.5px solid #03a9f4;
    }
    .kanban-task small {
        font-size: 0.98em;
        color: #3491b4;
        font-style: italic;
    }
    div[data-testid="stButton"] button {
        margin-right: 0.7em;
        margin-bottom: 0.35em;
        border-radius: 5px !important;
        border: 1.3px solid #03a9f4 !important;
        color: #03a9f4 !important;
        background: #fff !important;
        font-size: 0.97em;
        transition: background 0.2s, color 0.2s;
    }
    div[data-testid="stButton"] button:hover {
        background: #03a9f4 !important;
        color: #fff !important;
        border: 1.3px solid #03a9f4 !important;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    if 'user_id' not in st.session_state or 'view_project_id' not in st.session_state:
        st.warning("Access denied.")
        return

    project_id = st.session_state['view_project_id']
    user_id = st.session_state['user_id']
    proj = get_project_by_id(project_id)
    if not proj or user_id not in proj['participants']:
        st.error("You are not a participant in this project.")
        return

    part_names = [get_user_by_id(pid)['full_name'] for pid in proj['participants'] if get_user_by_id(pid)]

    # Project details card
    st.markdown(f'''
        <div class="project-card">
            <h2>{proj['title']}</h2>
            <p>{proj['desc']}</p>
            <p><strong>Timeline:</strong> {proj['timeline']}</p>
            <p><strong>Participants:</strong> {", ".join(part_names)}</p>
        </div>
    ''', unsafe_allow_html=True)

    st.subheader("Project Task DashBoard")

    statuses = ["To Do", "In Progress", "Done"]
    status_colors = {"To Do": "#296eb4", "In Progress": "#03a9f4", "Done": "#159e6c"}
    cols = st.columns(3)

    for idx, status in enumerate(statuses):
        with cols[idx]:
            st.markdown(
                f'<div style="font-size:1.14em; font-weight:600; margin-bottom:0.75em; color:{status_colors[status]};">{status}</div>',
                unsafe_allow_html=True
            )
            with st.container():
                st.markdown('<div class="kanban-col">', unsafe_allow_html=True)
                for task in [t for t in proj.get('tasks', []) if t['status'] == status]:
                    assigned_name = get_user_by_id(task['assigned_to'])['full_name']
                    st.markdown(
                        f'<div class="kanban-task">'
                        f'<span style="font-size:1.07em;">📝 {task["description"]}</span><br>'
                        f'<small>(Assigned to: {assigned_name})</small></div>',
                        unsafe_allow_html=True
                    )
                    if (task['assigned_to'] == user_id or user_id == proj['owner']):
                        next_status = statuses[(idx+1)%3]
                        col1, col2 = st.columns([1.2,1])
                        with col1:
                            if st.button(f"Move to {next_status}", key=f"move{task['id']}"):
                                task['status'] = next_status
                                edit_project(project_id, proj['title'], proj['desc'], proj['required_skills'], proj['timeline'], tasks=proj['tasks'])
                                st.rerun()
                        with col2:
                            if st.button("Delete task", key=f"del{task['id']}"):
                                proj['tasks'] = [t for t in proj['tasks'] if t['id'] != task['id']]
                                edit_project(project_id, proj['title'], proj['desc'], proj['required_skills'], proj['timeline'], tasks=proj['tasks'])
                                st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Add New Task")

    # Initialize session state for new_task_desc if not present
    if "new_task_desc" not in st.session_state:
        st.session_state["new_task_desc"] = ""

    new_task_text = st.text_input("Task description", key="new_task_desc", value=st.session_state["new_task_desc"])
    assignee = st.selectbox("Assign to", options=proj['participants'], format_func=lambda uid: get_user_by_id(uid)['full_name'], key="add_task_assignee")

    if st.button("Add Task"):
        if new_task_text.strip():
            next_id = max([t['id'] for t in proj.get('tasks', [])] or [0]) + 1
            proj['tasks'].append({"id": next_id, "description": new_task_text.strip(), "assigned_to": assignee, "status": "To Do"})
            edit_project(project_id, proj['title'], proj['desc'], proj['required_skills'], proj['timeline'], tasks=proj['tasks'])
            st.session_state["new_task_desc"] = ""
            st.rerun()
        else:
            st.warning("Task description cannot be empty.")

if __name__ == "__main__":
    main()
