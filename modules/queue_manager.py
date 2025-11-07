from sqlalchemy import text
from config.db_config import engine

def get_next_request(tier: int):
    """Ambil request tertua yang status-nya 'pending' untuk tier tertentu."""
    with engine.connect() as conn:
        query = text("""
            SELECT * FROM request_queue
            WHERE status = 'pending' AND tier = :tier
            ORDER BY created_at ASC
            LIMIT 1
        """)
        result = conn.execute(query, {"tier": tier}).fetchone()
        if result:
            return dict(result._mapping)
        return None


def update_request_status(request_id: str, status: str):
    """Update status request."""
    with engine.connect() as conn:
        conn.execute(
            text("UPDATE request_queue SET status = :status WHERE request_id = :rid"),
            {"status": status, "rid": request_id}
        )
        conn.commit()
