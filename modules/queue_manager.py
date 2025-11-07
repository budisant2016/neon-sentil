# modules/queue_manager.py
from sqlalchemy import text
from config.db_config import engine

def get_next_request(tier: int):
    query = text("""
        SELECT * FROM request_queue
        WHERE status = 'pending' AND tier = :tier
        ORDER BY created_at ASC
        LIMIT 1;
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"tier": tier}).fetchone()
    return result

def update_request_status(request_id, status):
    query = text("UPDATE request_queue SET status = :status WHERE request_id = :id")
    with engine.begin() as conn:
        conn.execute(query, {"status": status, "id": request_id})
