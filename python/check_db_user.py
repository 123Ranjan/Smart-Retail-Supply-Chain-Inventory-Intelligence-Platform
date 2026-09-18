from sqlalchemy import text
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_ROOT / "python" / "etl"))

from config.database import get_engine


engine = get_engine()

with engine.connect() as connection:

    result = connection.execute(
        text("""
            SELECT
                current_user,
                current_database(),
                current_schema();
        """)
    )

    print("Database connection:")
    print(result.fetchone())

    result = connection.execute(
        text("""
            SELECT
                schema_name,
                schema_owner
            FROM information_schema.schemata
            WHERE schema_name = 'retail_dw';
        """)
    )

    print("Schema:")
    print(result.fetchone())