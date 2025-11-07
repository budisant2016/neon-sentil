# streamlit_app.py
import streamlit as st
from modules.db_validator import validate_tables
from modules.queue_manager import get_next_request
from config.db_config import get_connection

# 🧩 Jalankan validasi & seeding tabel
validate_tables()

st.title("🧠 Sentil.AI — Adaptive Tier Queue System")

tier = st.selectbox("Pilih Tier", [1, 2, 3])
conn = get_connection()
req = get_next_request(tier)

if req:
    st.success(f"🎯 Ditemukan request: {req}")
else:
    st.error("❌ Tidak ada slot aktif tersedia untuk tier ini.")
