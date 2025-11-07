from sqlalchemy import text
from config.db_config import engine

def acquire_session_slot(tier: int):
    """Ambil slot aktif untuk tier tertentu, jika tersedia."""
    with engine.connect() as conn:
        slot = conn.execute(text("""
            SELECT * FROM session_slots
            WHERE tier = :tier AND is_active = TRUE AND current_user IS NULL
            LIMIT 1
        """), {"tier": tier}).fetchone()

        if slot:
            conn.execute(text("""
                UPDATE session_slots
                SET current_user = gen_random_uuid(), started_at = NOW()
                WHERE slot_id = :sid
            """), {"sid": slot.slot_id})
            conn.commit()
            return dict(slot._mapping)
        return None


def release_session_slot(slot_id: int):
    """Lepas slot agar bisa dipakai lagi."""
    with engine.connect() as conn:
        conn.execute(text("""
            UPDATE session_slots
            SET current_user = NULL, started_at = NULL, expires_at = NULL
            WHERE slot_id = :sid
        """), {"sid": slot_id})
        conn.commit()
