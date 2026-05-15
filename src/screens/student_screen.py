import streamlit as st 
from src.screens.database.db import get_all_students,create_student,get_student_subjects,get_student_attendance,unenroll_student_to_subject
from src.screens.components.header import header_dashboard
from src.screens.ui.style_base_layout import style_background_dashboard,style_base_layout
from PIL import Image
import numpy as np 
from src.screens.pipeline.face_pipeline import get_face_embeddings,get_trained_model, predict_attendance,train_classifier
from src.screens.pipeline.voice_pipeline import get_voice_embedding,identify_speaker,process_bulk_audio
import time
from src.screens.components.dialog_enroll import enroll_dialog
from src.screens.components.subject_card import subject_card


def student_dashboard():
    """Professional student dashboard showing enrolled subjects and attendance stats"""
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    
    # Header with greeting and logout
    col1, col2, col3 = st.columns([2, 1, 1], vertical_alignment='center', gap='large')
    with col1:
        header_dashboard()
    with col2:
        st.markdown("")
    with col3:
        if st.button(" Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace", use_container_width=True):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data 
            st.rerun()

    # Welcome message
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f0f1ff 0%, #e0e3ff 100%);
            padding: 1.5rem;
            border-radius: 1rem;
            margin-bottom: 2rem;
            border-left: 4px solid #5865F2;
        ">
            <p style="
                margin: 0;
                font-size: 1.1rem;
                color: #2d3748;
                font-weight: 600;
            ">👋 Welcome, <span style="color: #5865F2; font-weight: 700;">{student_data['name']}</span></p>
            <p style="
                margin: 0.5rem 0 0 0;
                font-size: 0.9rem;
                color: #718096;
            ">Track your enrollment and attendance across all subjects</p>
        </div>
    """, unsafe_allow_html=True)

    # Subjects section header
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
            <h2 style="
                margin: 0;
                color: #2d3748;
                font-size: 1.5rem;
            "> Your Enrolled Subjects</h2>
        """, unsafe_allow_html=True)
    with col2:
        if st.button('Enroll in Subject', key ="enroll_sub",type='primary', use_container_width=True):
            enroll_dialog()

    st.divider()

   
    with st.spinner(' Loading your subjects...'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    # Build statistics map
    stats_map = {}
    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    # Display subject cards

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']
        
        
        
        
        stats = stats_map.get(sid, {"total": 0, "attended": 0})
            
            # Calculate attendance percentage
        attendance_pct = (stats['attended'] / stats['total'] * 100) if stats['total'] > 0 else 0
            
        def unenroll_button():
            if st.button(" Unenroll from this course", type='tertiary',key="unenroll", use_container_width=True):
                 unenroll_student_to_subject(student_id, sid)
                 st.toast(f'Unenrolled from {sub["name"]} successfully!')
                 st.rerun()

        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('📅', 'Total Classes', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                    ('📊', 'Attendance', f"{attendance_pct:.0f}%"),
                ],
                footer_callback=unenroll_button
            )
    else:
        st.info(" You haven't enrolled in any subjects yet. Click 'Enroll in Subject' to get started!")


def student_screen():
    """Main student screen handler - shows login or dashboard"""
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return
    
    # Login Screen
    col1, col2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with col1:
        header_dashboard()
    
    with col2:
        if st.button("← Back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace", use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    # st.markdown("""
    #     <div style="
    #         text-align: center;
    #         margin: 2rem 0 1rem 0;
    #     ">
    #         <h2 style="
    #             color: #2d3748;
    #             font-size: 1.75rem;
    #             margin: 0;
    #         ">🔐 Face Recognition Login</h2>
    #         <p style="
    #             color: #718096;
    #             margin: 0.5rem 0 0 0;
    #         ">Position your face in the center and capture your image</p>
    #     </div>
    # """, unsafe_allow_html=True)

    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        photo_source = st.camera_input("📸 Capture Your Face", label_visibility="collapsed")

    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner('🤖 AI is analyzing your face...'):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.error('❌ No face detected. Please try again with good lighting.')
            elif num_faces > 1:
                st.error('❌ Multiple faces detected. Please ensure only your face is in the frame.')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id']==student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.success(f'✅ Welcome back, {student["name"]}!')
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('ℹ Face not recognized in our system. Let\'s create a new profile!')
                    
                    # Registration form
                    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                    
                    with st.container(border=True):
                        st.markdown("""
                            <h3 style="
                                margin-top: 0;
                                color: #2d3748;
                            "> Create New Student Profile</h3>
                        """, unsafe_allow_html=True)
                        
                        new_name = st.text_input(
                            "Full Name",
                            placeholder='E.g. Hamza Rizvi',
                            label_visibility="collapsed"
                        )

                        st.markdown("""
                            <p style="
                                color: #718096;
                                font-size: 0.9rem;
                                margin: 1rem 0 0.5rem 0;
                            "><b>Optional: Voice Enrollment</b></p>
                            <p style="
                                color: #a0aec0;
                                font-size: 0.85rem;
                                margin: 0;
                            ">Enhance your attendance by enrolling in voice recognition</p>
                        """, unsafe_allow_html=True)

                        audio_data = None
                        try:
                            audio_data = st.audio_input('🎤 Record a short phrase (e.g., "I am present")', label_visibility="collapsed")
                        except Exception as e:
                            st.error(' Audio recording failed. You can skip this step.')

                        if st.button('✅ Create Account', type='primary', use_container_width=True):
                            if new_name:
                                with st.spinner('🔄 Creating your profile...'):
                                    img = np.array(Image.open(photo_source))
                                    encodings = get_face_embeddings(img)
                                    
                                    if encodings:
                                        face_emb = encodings[0].tolist()
                                        voice_emb = None
                                        
                                        if audio_data:
                                            try:
                                                voice_emb = get_voice_embedding(audio_data.read())
                                            except Exception:
                                                st.warning('⚠️ Voice enrollment skipped due to audio issue.')

                                        response_data = create_student(new_name, face_embeddings=face_emb, voice_embeddings=voice_emb)

                                        if response_data:
                                            train_classifier()
                                            st.session_state.is_logged_in = True
                                            st.session_state.user_role = 'student'
                                            st.session_state.student_data = response_data[0]
                                            st.success(f'✅ Profile created successfully! Hi {new_name}!')
                                            time.sleep(1)
                                            st.rerun()
                                        else:
                                            st.error('❌ Failed to create account. Please try again.')
                                    else:
                                        st.error('❌ Could not capture your facial features. Please ensure good lighting and try again.')
                            else:
                                st.warning('⚠️ Please enter your full name to continue.')



def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {student_data['name']} """)
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data 
            st.rerun()


    st.space()

    c1, c2 =st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch'):
            enroll_dialog()


    st.divider()


    with st.spinner('Loading your enrolled subjects..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total":0, "attended": 0}

        stats_map[sid]['total'] +=1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1


    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']


        stats = stats_map.get(sid,{"total":0, "attended": 0} )
        def unenroll_button():
                if st.button("Unenroll from this course", type='tertiary', width='stretch', icon=':material/delete_forever:',key=f"unenroll {sub["name"]}"):
                    unenroll_student_to_subject(student_id, sid)
                    st.toast(f'Unenrolled from {sub['name']} successfully!')
                    st.rerun()

        with cols[i % 2]:

            subject_card(
                name = sub['name'],
                code =sub['subject_code'],
                section = sub['section'],
                stats = [
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )



def student_screen():


    style_background_dashboard()
    style_base_layout()


    if "student_data" in st.session_state:
        student_dashboard()
        return
    
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] =student_screen
            st.rerun()

    st.header('Login using FaceID', text_alignment='center')
    st.space()
    st.space()
    
    show_registration = False
    photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner('AI is scanning..'):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning('Face not found!')
            elif num_faces >1:
                st.warning('Multiple faces found')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id']==student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f'Welcome Back {student['name']}')
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized! You might be a new student!')
                    show_registration = True
    if show_registration:
        with st.container(border=True):
            st.header('Register new Profile')
            new_name = st.text_input("Enter your name", placeholder='E.g. Hamza Rizvi')

            st.subheader('Optional : Voice Enrollment')
            st.info("Enroll your for voice only attendance")


            audio_data = None

            try:
                audio_data = st.audio_input('Record a short phrase like I am present, My name is Akash.')
            except Exception:
                st.error('Audio Data failed!')

            if st.button('Create Account', type='primary'):
                if new_name:
                    with st.spinner('Creating profile..'):
                        img = np.array(Image.open(photo_source))
                        encodings= get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(new_name, face_embeddings=face_emb, voice_embeddings=voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f'Profile Created! Hi {new_name}!')
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error('Couldnt capture your facial features for registration')

                else:
                    st.warning('Please enter your name!')

                   


   






        





