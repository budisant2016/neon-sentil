# modules/result_writer.py
from sqlalchemy import text
from config.db_config import engine

def write_result(request_id, result):
    query = text("""
        INSERT INTO response_log (request_id, method, sentiment, confidence)
        VALUES (:rid, :method, :sentiment, :confidence)
    """)
    with engine.begin() as conn:
        conn.execute(query, {
            "rid": request_id,
            "method": result["method"],
            "sentiment": result["sentiment"],
            "confidence": result["confidence"]
        })
