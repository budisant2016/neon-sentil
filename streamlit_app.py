import streamlit as st
from modules.db_validator import validate_tables

st.write("🔧 Validating database schema...")
validate_tables()
st.success("Database schema validated or auto-fixed!")
