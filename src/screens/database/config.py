import streamlit as st 
from supabase import create_client, Client

supabase: Client=create_client(
    st.secrets["project_url"],
    st.secrets["key"]
)