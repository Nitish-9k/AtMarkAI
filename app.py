import streamlit as st 

import src.screens.home_screen
import src.screens.student_screen
import src.screens.teachers_screen
from src.screens.components.dialog_auto_enroll import auto_enroll_dialog


# Initialize session state FIRST
if 'login_type' not in st.session_state:
    st.session_state['login_type'] = None

if 'is_loggeed_in' not in st.session_state:
    st.session_state['is_logged_in'] = False

if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None


def main():
    st.set_page_config(
        page_title="AtMarkAi- Making Attendance faster using AI",
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png"
    )


    match st.session_state['login_type']:

        case 'teacher':
            src.screens.teachers_screen.teachers_screen()

        case 'student':
            src.screens.student_screen.student_screen()

        case None:
            src.screens.home_screen.home_screen()


    join_code = st.query_params.get('join-code')

    if join_code:

        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()

        if st.session_state.get("is_logged_in") and st.session_state.get("user_role") == "student":  
            auto_enroll_dialog(join_code)


main()