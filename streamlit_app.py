import streamlit as st
import pandas as pd

# Create connection
conn = st.connection("neon", type="sql")

st.title("Test Neon ↔ Streamlit Connection")

# Query simple data
df = conn.query("SELECT * FROM test_data;", ttl=0)

st.write("✅ Connected & Query Success")
st.dataframe(df)
