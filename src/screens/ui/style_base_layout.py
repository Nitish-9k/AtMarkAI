import streamlit as st




def style_background_home():
    st.markdown("""
        <style>
                
                .stApp{
                background:#5865F2 !important;
                }
                .stApp div[data-testid="stColumn"]{
                    background:#E0E3FF !important;
                    padding: 2.5rem !important;
                    border-radius: 5rem !important;
                    }
                
        </style>
            


            """
                , unsafe_allow_html=True
    )

def style_background_dashboard():
    st.markdown("""
        <style>
                
                .stApp{
                     background:#E0E3FF !important;
                }
                
                
        </style>
            


            """
                , unsafe_allow_html=True
    )

def style_base_layout():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
         /* hide top main menu bar of streamlit */
                
                #MainMenu,footer,header{
                    visibility: hidden;
                }
                .block-container {
                    padding-top: 1.5rem !important;

                }
                h1{
                font-family: "Climate Crisis",sans-serif !important;
                font-size:2.9rem !important;
                line-hieght:2.1 !important;
                margin-bottom:0rem !important;
                


                }
                h2{
                font-family: "Climate Crisis",sans-serif !important;
                font-size:1.9rem !important;
                line-hieght:0.9!important;
                margin-bottom:0rem !important;
                
                
                

                }
                h3,h3,p {
                    font-family:"Outfit",sans-serif;
                }

                button{
                    border-radius:1.5rem !important;
                    background:#5865F2 !important;
                    color:white !important;
                    padding:10px 20px !important ;
                    border:none;
                    transition :transform 0.25 ease-in-out !important ;
                    }
                
                button[kind="secondary"]{
                    border-radius:1.5rem !important;
                    background:#EB459E !important;
                    color:white !important;
                    padding:10px 20px !important ;
                    border:none !important;
                    transition :transform 0.25 ease-in-out !important ;
                    }
                button[kind="tertiary"]{
                    border-radius:1.5rem !important;
                    background:#EB459E !important;
                    color:black!important;
                    padding:10px 20px !important ;
                    border:none !important ;
                    transition :transform 0.25 ease-in-out !important ;
                    }
                
                button:hover{
                    transform :scale(1.025)}



                
                

                
                
                
                
            </style>
            


            """
                , unsafe_allow_html=True
    )
