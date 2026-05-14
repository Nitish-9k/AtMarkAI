import streamlit as st 
from src.screens.database.config import supabase
from src.screens.components.subject_card import subject_card

from src.screens.database.db import check_teacher_exists, create_teacher, get_teacher_subjects,create_subject,get_attendance_for_teacher
from src.screens.components.header import header_dashboard
from src.screens.ui.style_base_layout import style_background_dashboard,style_base_layout
from src.screens.database.db import teacher_login,check_teacher_exists,create_teacher
from src.screens.components.dialogue_create_subject import  create_subject_dialog
from src.screens.components.dialog_share_subject import share_subject_dialog as share_subject_dialogue
from src.screens.components.dialog_addphoto import add_photos_dialog
from src.screens.pipeline.face_pipeline import predict_attendance
import numpy as np
from src.screens.database.config import supabase
from src.screens.components.dialog_attendance_results import attendance_result_dialog
from datetime import datetime
import pandas as pd
from src.screens.components.dialog_voice_pipeline import voice_attendance_dialog 


def teachers_screen():
    style_background_dashboard()
    style_base_layout()
    if "teacher_data" in st.session_state:
        teacher_dashboard()
         
         
    
    elif "teacher_login_type"not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type=="register":
        teacher_screen_register()

def teacher_dashboard():
    
    teacher_data = st.session_state.teacher_data
    
   
    col1, col2, col3 = st.columns([2, 1, 1], vertical_alignment='center', gap='large')
    with col1:
        header_dashboard()
    with col2:
        st.markdown("")
    with col3:
        if st.button(" Logout", type='secondary', key='teacherbackbtn'):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()

   

    
    tab1, tab2, tab3 = st.columns(3, gap='large')

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "Take_attendance"
    
    with tab1:
        tab_type = "primary" if st.session_state.current_teacher_tab == "Take_attendance" else "tertiary"
        if st.button(" Take Attendance", type=tab_type,key="take_attendance", use_container_width=True):
            st.session_state.current_teacher_tab = "Take_attendance"
            st.rerun()
    
    with tab2:
        tab_type = "primary" if st.session_state.current_teacher_tab == "Manage_subjects" else "tertiary"
        if st.button(" Manage Subjects", type=tab_type,key="manage_subject", use_container_width=True):
            st.session_state.current_teacher_tab = "Manage_subjects"
            st.rerun()
    
    with tab3:
        tab_type = "primary" if st.session_state.current_teacher_tab == "Attendance_Record" else "tertiary"
        if st.button(" View Records", type=tab_type,key="view_record", use_container_width=True):
            st.session_state.current_teacher_tab = "Attendance_Record"
            st.rerun()

    st.divider()

   
    if st.session_state.current_teacher_tab == "Take_attendance":
        teacher_tab_take_attendace()
    elif st.session_state.current_teacher_tab == "Manage_subjects":
        teacher_tab_manage_subjects()
    elif st.session_state.current_teacher_tab == "Attendance_Record":
        teacher_tab_attendance_records()

          
          

def teacher_tab_take_attendace():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')


    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return
    
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3,1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch',key="addphotos"):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4 ]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos,key="clearphots"):
            st.session_state.attendance_images = []
            st.rerun()


    with c2:
        
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos,key="face_analysis"):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)
                    # st.write("Detected",detected)


                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(int(student_id), []).append(f"Photo {idx+1}")

                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id',selected_subject_id ).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:

                    results, attendance_to_log  = [], []

                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present= len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp':  current_timestamp,
                            'is_present': bool(is_present)
                        })

                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

        with c3:
            if st.button("Use Voice Attendance",type='primary',width="stretch",icon=":material/mic:"):
                voice_attendance_dialog(selected_subject_id)        



                                   








   


def  teacher_tab_manage_subjects():
    teacher_id=st.session_state.teacher_data["teacher_id"]
    col1,col2=st.columns(2)
    with col1:
        st.header("Manage subject",width="stretch")
    with col2:
        if st.button("Create new subject", width="stretch"):
            create_subject_dialog(teacher_id)


    #list all subjects
    subjects=get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats=[
                {"👥","Students",sub["total_students"]},
                {"🕐","Classes",sub["total_classes"]},
                
            ]

        def share_btn():
            if st.button(f"Share code: {sub['name']}",key=f"share_{sub['subject_code']}",icon=":material/share:"):
                share_subject_dialogue(sub['name'],sub['subject_code'])
            st.space()

        subject_card(
             name=sub["name"],
             code=sub["subject_code"],
             section=sub["section"],
             stats=stats,
             footer_callback=share_btn


        )

    else:
        st.info("No Subjects found,Create one Above")


def  teacher_tab_attendance_records():
    st.header("Attendance Records")
    teacher_id=st.session_state.teacher_data["teacher_id"]
    records=get_attendance_for_teacher(teacher_id)

    if not records:
        return
    data=[]
    for r in records:
        ts=r.get('timestamp')

        data.append({
            "ts_group":ts.split(".")[0] if ts else None,
            "Time":datetime.fromisoformat(ts).strftime("%Y-%m-%d  %I:%M %p")if  ts else "N'A",
            "Subject":r["subjects"]["name"],
            "Subject Code":r["subjects"]["subject_code"],
            "is_present":bool(r.get("is_present",False))

        })
    df=pd.DataFrame(data)

    summary=(
        df.groupby(['ts_group','Time','Subject','Subject Code','is_present'])
        .agg(
                Present_Count=('is_present','sum'),
                Total_Count=('is_present','count')

        ).reset_index()


    )
    summary["Attendance_Stats"]=(
        "✅" + summary["Present_Count"].astype(str)+"/"+
        summary["Total_Count"].astype(str)+"Students"


    )
    display_df=(summary.sort_values(by='ts_group',ascending=False)
                [['Time','Subject','Subject Code','Attendance_Stats']]
                )
    st.dataframe(display_df,width='stretch',hide_index=True)



    






 










def login_teacher(username,password):
     teacher=teacher_login(username,password)
     if teacher:
          st.session_state.user_role='teacher'
          st.session_state.teacher_data=teacher
          st.session_state.is_logged_in=True
          return True
     return False          
     
     
   
def teacher_screen_login():
        c1,c2=st.columns(2,vertical_alignment="center",gap="xxlarge")
        with c1:
            header_dashboard()
        with c2:
           if st.button("Go back to Home",type="secondary",key="teacherbackbtn",shortcut="control+backspace"):
                st.session_state["login_type"]=None
                st.rerun()

        st.header("Login using password", text_alignment="center")
        st.space()

        teacher_username=st.text_input("Username",placeholder="Enter username")
        teacher_password=st.text_input("Password",type="password",placeholder="Enter password")

        st.divider()
        btn1,btn2=st.columns(2,gap="large")
        with btn1:
            if st.button("Login",type="primary",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
                 if login_teacher(teacher_username,teacher_password):
                      st.toast("Welcome,"+teacher_username+"!")
                      import time 
                      time.sleep(2)
                      st.rerun()
                 else:
                      st.error("Invalid username or password!")
                
            
        with btn2:
            if st.button("Register",type="secondary",icon=":material/passkey:",width="stretch"):
                 st.session_state.teacher_login_type="register"
                 

def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False,"All fields are required!"
    if check_teacher_exists(teacher_username):
        return False,"Username already taken, try another one!"
    if teacher_pass!=teacher_pass_confirm:
        return False,"Passwords do not match!"
    
    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True,"Successfully Registered! Login Now"


    except Exception as e:
        return False,"Unexpeected error occurred"

     

     
     
     
                 

def teacher_screen_register():
        c1,c2=st.columns(2,vertical_alignment="center",gap="xxlarge")
        with c1:
            header_dashboard()
        with c2:
            if st.button("Go back to Home",type="secondary",key="teacherbackbtn",shortcut="control+backspace"):
                 st.session_state["login_type"]=None
                 st.rerun()

        st.header("Register your teacher profile")
        st.space()
        st.space()

        teacher_username=st.text_input("Enter username",placeholder="Enter username")
        teacher_name=st.text_input("Enter name",placeholder="Enter name")
        teacher_password=st.text_input(" Enter password",type="password",placeholder="Enter password")       
        teacher_password_confirm=st.text_input("Confirm password",type="password",placeholder="Enter password")        


        btn1,btn2=st.columns(2,gap="large")
        with btn1:
            if st.button("Register now",type="primary",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
                 success,message=register_teacher(teacher_username,teacher_name,teacher_password,teacher_password_confirm)
                 if success:
                      st.success(message)
                      import time 
                      time.sleep(2)
                      st.session_state.teacher_login_type="login"
                      st.rerun()
                 else:
                      st.error(message)


                 

        with btn2:
            if st.button("Login",type="secondary",icon=":material/passkey:",width="stretch"):
                    st.session_state.teacher_login_type="login"



