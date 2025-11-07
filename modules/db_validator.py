# modules/db_validator.py
from sqlalchemy import create_engine, text
from config.db_config import engine

# Daftar struktur minimal per tabel
TABLE_SCHEMAS = {
    "users": {
        "columns": {
            "user_id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "username": "VARCHAR(100)",
            "email": "VARCHAR(200)",
            "tier": "SMALLINT DEFAULT 1",
            "created_at": "TIMESTAMP DEFAULT NOW()"
        }
    },
    "request_queue": {
        "columns": {
            "request_id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "user_id": "UUID REFERENCES users(user_id)",
            "tier": "SMALLINT DEFAULT 1",
            "status": "VARCHAR(50) DEFAULT 'pending'",
            "payload": "TEXT",
            "created_at": "TIMESTAMP DEFAULT NOW()"
        }
    },
    "response_log": {
        "columns": {
            "response_id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "request_id": "UUID REFERENCES request_queue(request_id)",
            "result": "TEXT",
            "confidence": "NUMERIC(5,2)",
            "processed_at": "TIMESTAMP DEFAULT NOW()"
        }
    },
    "session_slots": {
        "columns": {
            "slot_id": "INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY",
            "tier": "SMALLINT NOT NULL CHECK (tier IN (1,2,3))",
            "is_active": "BOOLEAN DEFAULT TRUE",
            "current_user": "UUID REFERENCES users(user_id)",
            "started_at": "TIMESTAMP",
            "expires_at": "TIMESTAMP"
        }
    },
    "system_log": {
        "columns": {
            "log_id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
            "log_type": "VARCHAR(50)",
            "message": "TEXT",
            "created_at": "TIMESTAMP DEFAULT NOW()"
        }
    },
    "tier_config": {
        "columns": {
            "tier": "SMALLINT PRIMARY KEY",
            "max_requests": "INT DEFAULT 5",
            "max_batch": "INT DEFAULT 10",
            "wait_time": "INT DEFAULT 900",
            "description": "TEXT"
        }
    }
}


def validate_tables():
    with engine.connect() as conn:
        for table, info in TABLE_SCHEMAS.items():
            print(f"🔍 Checking table: {table}")

            # Cek apakah tabel ada
            result = conn.execute(
                text("SELECT to_regclass(:tname)"), {"tname": table}
            ).scalar()

            if not result:
                print(f"⚠️ Table {table} not found. Creating...")
                columns = ", ".join([f"{col} {dtype}" for col, dtype in info["columns"].items()])
                conn.execute(text(f"CREATE TABLE {table} ({columns});"))
                conn.commit()
                print(f"✅ Table {table} created.")
            else:
                # Cek kolom per kolom
                existing_cols = conn.execute(
                    text(f"""
                    SELECT column_name FROM information_schema.columns
                    WHERE table_name = :tname
                    """),
                    {"tname": table},
                ).fetchall()

                existing_cols = [r[0] for r in existing_cols]
                for col, dtype in info["columns"].items():
                    if col not in existing_cols:
                        print(f"➕ Adding missing column '{col}' to {table}")
                        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col} {dtype};"))
                        conn.commit()
                print(f"✅ Table {table} validated and up to date.")
        print("🎉 All tables validated successfully.")
