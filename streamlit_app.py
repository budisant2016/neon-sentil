# streamlit_app.py
import streamlit as st
from modules.queue_manager import get_next_request, update_request_status
from modules.sentiment_processor import analyze_sentiment
from modules.result_writer import write_result

st.title("🚀 Sentil Backend Monitor")

tier = st.selectbox("Pilih Tier", [1, 2, 3])

if st.button("Proses Antrian Tier Ini"):
    req = get_next_request(tier)
    if not req:
        st.warning("Tidak ada antrian pending.")
    else:
        st.write(f"Memproses request ID: {req.request_id}")
        update_request_status(req.request_id, "processing")

        result = analyze_sentiment(req.text_data, req.method)
        write_result(req.request_id, result)

        update_request_status(req.request_id, "done")
        st.success(f"Selesai → Sentimen: {result['sentiment']} ({result['confidence']*100:.1f}%)")
