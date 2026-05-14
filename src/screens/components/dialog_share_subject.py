import streamlit as st

import segno
import io



@st.dialog("Share Class link")
def share_subject_dialog(subject_name,subject_code):
    app_domain="AtMarkAi-main.streamlit.app"
    join_url=f"{app_domain}?join-code={subject_code}"

    st.header("Scan to Join")
    qr=segno.make(join_url)
    out=io.BytesIO()
    qr.save(out,kind="png",scale=10,border=1)

    col1,col2=st.columns(2)
    with col1:
        st.markdown("### Copy link")
        st.code(join_url ,language="text")
        st.code(subject_code,language="text")
        st.info("Copy the above link or code and share with your students to join the class")

    with col2:
        st.markdown("###scan to Join")
        st.image(out.getvalue(),caption="Scan this QR code to join the class")












