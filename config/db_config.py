import os
from sqlalchemy import create_engine, text

# ✅ Gunakan environment variable di Streamlit Cloud (Settings → Secrets)
DB_URL = os.getenv("NEON_DB_URL")

if not DB_URL:
    raise ValueError("❌ Environment variable NEON_DB_URL belum diset!")

# Gunakan pooling (lebih stabil di Streamlit Cloud)
engine = create_engine(DB_URL, pool_pre_ping=True, pool_size=3, max_overflow=5)

def test_connection():
    """Cek koneksi Neon DB"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW()"))
        print("✅ Koneksi sukses:", result.scalar())

if __name__ == "__main__":
    test_connection()
