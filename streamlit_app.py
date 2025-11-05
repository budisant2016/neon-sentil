import streamlit as st
import pandas as pd

conn = st.connection("neon", type="sql")

# Untuk complex queries
with conn.session as session:
    result = session.execute("SELECT COUNT(*) FROM users")
    user_count = result.scalar()
    st.metric("Total Users", user_count)

# Untuk simple queries (recommended)
df = conn.query("SELECT * FROM active_sessions WHERE status = 'active'")
st.dataframe(df)
