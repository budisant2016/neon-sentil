import streamlit as st
import pandas as pd

conn = st.connection("neon", type="sql")

st.title("Neon Test — Read + Insert")

if st.button("Insert New Row"):
    conn.query("INSERT INTO test_data (message) VALUES ('Streamlit Cloud Insert Test');", ttl=0)
    st.success("✅ Inserted!")

df = conn.query("SELECT * FROM test_data ORDER BY id DESC;", ttl=0)
st.dataframe(df)
