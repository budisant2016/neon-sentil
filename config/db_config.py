import streamlit as st
from sqlalchemy import create_engine

try:
    DB_URL = st.secrets["connections"]["NEON_DB_URL"]
except KeyError:
    raise ValueError("❌ NEON_DB_URL belum diset di Streamlit Secrets!")

engine = create_engine(DB_URL)

