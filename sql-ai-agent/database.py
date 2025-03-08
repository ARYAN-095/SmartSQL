import psycopg2
from config import Config
from typing import Dict, Any

class DatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(**Config.DB_CONFIG)
        
    def get_schema(self) -> str:
        """Fetch condensed schema information with optimal token usage"""
        schema = []
        with self.conn.cursor() as cursor:
            # Get tables and columns
            cursor.execute("""
                SELECT table_name, column_name, data_type 
                FROM information_schema.columns 
                WHERE table_schema = 'public'
            """)
            for table, column, dtype in cursor.fetchall():
                schema.append(f"Table {table}: {column} ({dtype})")
        
        return "\n".join(schema)[:3000]  # Limit schema to 3000 chars for token efficiency