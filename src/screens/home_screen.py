import streamlit as st 
from src.screens.components.footer import footer_home
from src.screens.components.header import header_home
from src.screens.ui.style_base_layout import style_base_layout,style_background_home

def home_screen():
   
    header_home()
    style_background_home()
    style_base_layout()
    col1,col2=st.columns(2,gap="xlarge")

    with col1:
        st.header("Teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)
        if st.button("Teachers Portal",type="primary",icon=":material/arrow_outward:",icon_position="right"):
           st.session_state["login_type"]="teacher"
           st.rerun()

    with col2:
        st.header("Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button("Student Portal",type="primary",icon=":material/arrow_outward:",icon_position="right"):
            st.session_state["login_type"]="student"
            st.rerun()
