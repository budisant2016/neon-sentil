# modules/db_validator.py
import sqlalchemy
from sqlalchemy import text
from config.db_config import get_connection

def validate_tables():
    print("🔧 Validating database schema...")

    expected_tables = {
        "users": {
            "user_id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "username": "VARCHAR(100) NOT NULL UNIQUE",
            "email": "VARCHAR(150)",
            "tier": "SMALLINT DEFAULT 1",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        },
        "request_queue": {
            "request_id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "user_id": "UUID REFERENCES users(user_id)",
            "text_input": "TEXT",
            "tier": "SMALLINT DEFAULT 1",
            "status": "VARCHAR(20) DEFAULT 'pending'",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        },
        "response_log": {
            "response_id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "request_id": "UUID REFERENCES request_queue(request_id)",
            "model_used": "VARCHAR(50)",
            "sentiment": "VARCHAR(20)",
            "confidence": "FLOAT",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        },
        "session_slots": {
            "slot_id": "INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY",
            "tier": "SMALLINT NOT NULL CHECK (tier IN (1,2,3))",
            "is_active": "BOOLEAN DEFAULT TRUE",
            "current_user": "UUID REFERENCES users(user_id)",
            "started_at": "TIMESTAMP",
            "expires_at": "TIMESTAMP"
        },
        "tier_config": {
            "tier_id": "SMALLINT PRIMARY KEY",
            "name": "VARCHAR(50)",
            "max_requests_per_day": "INT",
            "batch_limit": "INT",
            "wait_time_minutes": "INT"
        },
        "system_log": {
            "log_id": "BIGSERIAL PRIMARY KEY",
            "event": "TEXT",
            "details": "TEXT",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        }
    }

    conn = get_connection()
    for table, columns in expected_tables.items():
        cols_sql = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        conn.execute(text(f"CREATE TABLE IF NOT EXISTS {table} ({cols_sql});"))

    # --- AUTO-SEED SESSION SLOTS ---
    result = conn.execute(text("SELECT COUNT(*) FROM session_slots;")).scalar()
    if result == 0:
        conn.execute(text("""
            INSERT INTO session_slots (tier, is_active)
            VALUES (1, TRUE), (2, TRUE), (3, TRUE);
        """))
        print("🌱 Seeded session_slots successfully!")

    conn.commit()
    conn.close()
    print("✅ Database schema validated or auto-fixed!")
