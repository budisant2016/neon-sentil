import streamlit as st
from sqlalchemy import text

conn = st.connection("neon", type="sql")

st.title("Neon Test — Read + Insert")

if st.button("Insert New Row"):
    with conn.session as session:
        session.execute(
            text("INSERT INTO test_data (message) VALUES (:msg)"),
            {"msg": "Streamlit Cloud Insert Test"}
        )
        session.commit()
    st.success("✅ Row inserted")

df = conn.query("SELECT * FROM test_data ORDER BY id DESC;", ttl=0)
st.dataframe(df)
