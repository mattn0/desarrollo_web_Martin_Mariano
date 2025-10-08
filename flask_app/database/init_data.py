from database.db import engine
from sqlalchemy import text

#para llenar con region-comuna.sql

def load_region_comuna_data():
    with engine.connect() as conn:
        with open("database/region-comuna.sql", "r", encoding="utf-8") as f:
            sql_commands = f.read()
            for command in sql_commands.split(";"):
                if command.strip():
                    conn.execute(text(command))
        conn.commit()
