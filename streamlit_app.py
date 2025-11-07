from modules.queue_manager import get_next_request, update_request_status
from modules.session_manager import acquire_session_slot, release_session_slot
import streamlit as st

from modules.db_validator import validate_tables

st.title("🧠 Sentil.AI — Adaptive Tier Queue System")

tier = st.selectbox("Pilih Tier", [1, 2, 3], index=0)
slot = acquire_session_slot(tier)

if slot:
    st.success(f"Slot aktif ditemukan untuk tier {tier}")
    req = get_next_request(tier)
    if req:
        st.info(f"Processing request: {req['request_id']}")
        update_request_status(req["request_id"], "processing")
        st.write("✅ Request berhasil diproses.")
    else:
        st.warning("Tidak ada request pending.")
    release_session_slot(slot["slot_id"])
else:
    st.error("❌ Tidak ada slot aktif tersedia untuk tier ini.")
