import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from streamlit_option_menu import option_menu


# Compute absolute image paths relative to the location of this script
hero_img_path = os.path.join(os.path.dirname(__file__), "images", "hero_image.jpg")
team_img_path = os.path.join(os.path.dirname(__file__), "images", "team_image.png")

from Login import main as login_page
from Register import main as register_page
from Profile import main as profile_page
from SubmitProject import main as submit_project_page
from EditProject import main as edit_project_page
from ExploreProjects import main as explore_projects_page
from Notifications import main as notifications_page
from ProjectDashboard import main as project_dashboard_page  # Add this import


#style button 
st.markdown(
    """
    <style>
    .stButton>button#get_started_button {
        background-color: #03a9f4 !important;
        color: white !important;
        border: none !important;
        font-weight: bold;
        font-size: 1.1rem;
        padding-top: 10px !important;
        padding-bottom: 10px !important;
        border-radius: 6px !important;
        width: 100% !important;
        transition: background 0.3s;
    }
    .stButton>button#get_started_button:hover {
        background-color: #0288d1 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.set_page_config(page_title="TeamUp", page_icon="🤝", layout="wide")

def main():
    # Sidebar (unchanged)
    if 'user_id' not in st.session_state:
        nav_options = ["Home", "Login", "Register"]
        default_nav = st.session_state.get('sidebar_nav', "Home")
    else:
        nav_options = [
            "Home", "Profile", "Submit Project", "Explore Projects", "Notifications", "Logout"
        ]
        default_nav = st.session_state.get('sidebar_nav', "Home")
        if default_nav == "Edit Project":
            nav_options.insert(4, "Edit Project")

        if default_nav == "Project Dashboard" and "Project Dashboard" not in nav_options:
            nav_options.insert(4, "Project Dashboard")
    if default_nav not in nav_options:
        default_nav = nav_options[0]
    icons_map = {
        "Home": "house", "Login": "box-arrow-in-right", "Register": "person-plus",
        "Profile": "person-circle", "Submit Project": "plus-circle", "Edit Project": "pencil-square",
        "Explore Projects": "compass", "Notifications": "bell", "Logout": "box-arrow-left"
    }
    icons = [icons_map.get(opt, "circle") for opt in nav_options]
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=nav_options,
            icons=icons,
            menu_icon="cast",
            default_index=nav_options.index(default_nav),
            orientation="vertical",
            styles={
                "container": {"padding": "5px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color":"#2166c1"},
                "icon": {"color": "orange", "font-size": "20px"},
            },
        )
    st.session_state['sidebar_nav'] = selected

    # --- MAIN HOME PAGE UI ---
    if selected == "Home":
        # Top columns: Text (left) and Hero Image (right)
        col_left, col_right = st.columns([1.2, 1])
        with col_left:
            st.markdown(
                "<h1 style='font-size:3rem;font-weight:800; color:#2166c1;'>Team<span style='color:#0288d1'>Up</span></h1>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<div style='font-size:1.3rem; color:#444; margin-bottom:1em;'>"
                "Collaborate smarter, deliver stronger, grow faster.<br>"
                "Uniting skills for projects <span style='color:#0288d1'>that matter.</span></div>",
                unsafe_allow_html=True
            )

            
            get_started_clicked = st.button("Get Started", key="get_started_button")
            if get_started_clicked:
                st.session_state['sidebar_nav'] = "Register"
                st.rerun()
        with col_right:
            st.image(hero_img_path, use_container_width=True)
       

        # Features section (Why choose TeamUp?)
        feature_col1, feature_col2 = st.columns([1, 1])
        with feature_col2:
            # Lower main illustration, right column
                st.image(team_img_path, use_container_width=True)

        with feature_col1:
            st.markdown(
                "<h4 style='margin-bottom:0.5rem;'>Why choose TeamUp?</h4>",
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <ul style='font-size:1.1rem;line-height:2;color:#222;'>
                  <li>💡 Discover and join projects matching your skills and interests</li>
                  <li>🤝 Collaborate effortlessly with teammates through join requests and approvals</li>
                  <li>📋 Manage projects with an intuitive dashboard and editable details</li>
                  <li>🔔 Stay informed with real-time notifications about your projects and requests</li>
                  <li>👤 Maintain a personalized profile showcasing your skills and contributions</li>
                  <li>🔒 Secure, session-based login and data privacy</li>
                </ul>
                """,
                unsafe_allow_html=True
            )
            st.markdown("<div style='margin-top:1em;font-size:1rem;color:#aaa;'>Made with Streamlit &amp; Python • © 2025</div>", unsafe_allow_html=True)

    elif selected == "Login":
        login_page()
    elif selected == "Register":
        register_page()
    elif selected == "Profile":
        profile_page()
    elif selected == "Submit Project":
        submit_project_page()
    elif selected == "Edit Project":
        edit_project_page()
    elif selected == "Explore Projects":
        explore_projects_page()
    elif selected == "Notifications":
        notifications_page()
    
    elif selected == "Project Dashboard":
        project_dashboard_page()
    elif selected == "Logout":
        if 'user_id' in st.session_state:
            del st.session_state['user_id']
        if 'sidebar_nav' in st.session_state:
            del st.session_state['sidebar_nav']
        st.success("You have been logged out.")
        st.rerun()

if __name__ == "__main__":
    main()
