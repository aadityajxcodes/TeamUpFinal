
import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.user_functions import register_user

def inject_css():
    st.markdown(
        """
        <style>
             body{
                background: linear-gradient(135deg, #4f8cfb 0%, #2351a2 100%) !important;
            }
            .register-heading {
                font-size: 3rem;
                font-weight: 700;
                color: rgb(33, 102, 193);
                margin-bottom: 0.4em;
                margin-top: 0px !important;
            }
            .tagline {
                font-size: 1.2rem;
                color: #2978b5;
                margin-bottom: 2em;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    inject_css()
    
    st.markdown('<div class="register-heading">Create Your Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Let\'s build your next project together</div>', unsafe_allow_html=True)

    # Remove st.header("Register") as the custom heading above replaces it

    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    full_name = st.text_input("Full Name")
    skills = st.text_input("Skills (comma separated)")
    contact = st.text_input("Contact Number")
    bio = st.text_area("Short Bio")

    if st.button("Register"):
        if not (username and password and full_name):
            st.error("Please fill in all required fields.")
            return

        skills_list = [s.strip() for s in skills.split(",")] if skills else []
        user = register_user(username, password, full_name, skills_list, contact, bio)
        if user:
            st.success("Registration successful! Please login via the sidebar.")
        else:
            st.error("Username already exists, please choose another.")

     # Link to Login page
    st.markdown(
        '<div class="link-text">Already have an account? <a href="?page=login">Login here</a></div>',
        unsafe_allow_html=True,
    )


        
if __name__ == "__main__":
    main()
