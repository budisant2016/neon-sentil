import streamlit as st
from sqlalchemy import text

# Database connection
conn = st.connection("neon", type="sql")

st.title("Neon Test — Read + Insert")
st.title("Neon DB Demo — Level 2 ✅")
st.write("Input data via form + validation")

if st.button("Insert New Row"):
    with conn.session as session:
        session.execute(
            text("INSERT INTO test_data (message) VALUES (:msg)"),
            {"msg": "Streamlit Cloud Insert Test"}
        )
        session.commit()
    st.success("✅ Row inserted")
# --- Form Input ---
with st.form("add_row_form"):
    new_msg = st.text_input("Message")
    submitted = st.form_submit_button("Add")

    if submitted:
        if not new_msg.strip():
            st.warning("Message cannot be empty.")
        else:
            try:
                with conn.session as session:
                    session.execute(
                        text("INSERT INTO test_data (message) VALUES (:msg)"),
                        {"msg": new_msg}
                    )
                    session.commit()
                st.success(f"✅ Inserted: {new_msg}")
            except Exception as e:
                st.error(f"❌ Database error: {e}")

# --- Display Latest Rows ---
df = conn.query("SELECT * FROM test_data ORDER BY id DESC;", ttl=0)
st.dataframe(df)
st.write("### 📋 Current Data")
st.dataframe(df, use_container_width=True)
