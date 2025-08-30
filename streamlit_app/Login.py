
import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.user_functions import authenticate_user

def inject_css():
    st.markdown("""
        <style>
            body {
                background: linear-gradient(135deg, #4f8cfb 0%, #2351a2 100%) !important;
            }
            .main {
                background: transparent !important;
            }
            .login-heading {
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
    """, unsafe_allow_html=True)


def main():
    inject_css()

    st.markdown('<div class="login-heading">Welcome Back</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Let\'s build your next project together</div>', unsafe_allow_html=True)

    st.header("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(username, password)
        if user:
            st.success(f"Welcome back, {user['full_name']}!")
            st.session_state['user_id'] = user['id']
            st.rerun()
        else:
            st.error("Invalid username or password.")

     # Link to Register page
    st.markdown(
        '<div class="link-text">Don\'t have an account? <a href="?page=register">Register here</a></div>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()


# import streamlit as st
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from core.user_functions import authenticate_user

# # --- CSS for blue gradient background and card styling (image removed) ---
# st.markdown(
#     """
#     <style>
#     .stApp {
#         background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 38%, #64b5f6 100%);
#         min-height: 100vh;
#         background-attachment: fixed;
#     }
#     .login-card {
#         background: rgba(255,255,255,0.93);
#         max-width: 410px;
#         margin: 7% auto 2em auto;
#         padding: 2.2em 2em 1.5em 2em;
#         border-radius: 18px;
#         box-shadow: 0 6px 32px 0 #044a8760;
#     }
#     .login-card h2 {
#         color: #2166c1;
#         margin-bottom: 0.9em;
#         font-weight: 700;
#         text-align: center;
#         font-size: 2.1em;
#         letter-spacing: -0.02em;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# def main():
#     st.markdown('<div class="login-card">', unsafe_allow_html=True)
#     st.markdown('<h2>Login</h2>', unsafe_allow_html=True)

#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         user = authenticate_user(username, password)
#         if user:
#             st.success(f"Welcome back, {user['full_name']}!")
#             st.session_state['user_id'] = user['id']
#             st.rerun()
#         else:
#             st.error("Invalid username or password.")

#     st.markdown('<div style="text-align:center; margin-top:1.6em; color:#124; font-size:1em;">'
#                 "Don\'t have an account? Please register using the sidebar."
#                 '</div>', unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()


