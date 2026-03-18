import os
import psycopg as _psycopg


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5433")),
    "dbname": os.getenv("DB_NAME", "geometry_db"),
    "user": os.getenv("DB_USER", "user"),
    "password": os.getenv("DB_PASSWORD", "password"),
}


def _connect():
    return _psycopg.connect(**DB_CONFIG)


def init_db():
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id       SERIAL PRIMARY KEY,
            shape    TEXT,
            material TEXT,
            volume   FLOAT,
            surface  FLOAT,
            mass     FLOAT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def save_to_db(result: dict):
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO results (shape, material, volume, surface, mass) "
        "VALUES (%s, %s, %s, %s, %s)",
        (result["shape"], result["material"],
         result["volume"], result["surface"], result["mass"])
    )
    conn.commit()
    cur.close()
    conn.close()
